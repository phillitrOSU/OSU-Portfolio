TITLE Program Template     (template.asm)

; Author: Trevor Phillips
; Last Modified: 05/22/2022
; OSU email address: phillitr@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number:  6               Due Date: 6/5/2022
; Description: Program that requests 10 signed decimal integers from the user using macros
; to process the user strings, store as SDWORDs and write the user input.
; Then the integers are stored in an array that is displayed to the user. 
; The sum and average value of the array are computed and displayed.


INCLUDE Irvine32.inc


; request input string from user
mGetString MACRO prompt, output1, count
  .code
    mov    EDX, prompt
    call   WriteString
    mov    EDX, output1
    mov    ECX, count
    call   ReadString
ENDM

; display string_offset
mDisplayString MACRO string_offset
  .code
    push    EDX
    mov     EDX, string_offset
    call    WriteString
    pop     EDX
ENDM

; constants
ARRAYSIZE = 10      ; must match length_real variable
INTEGERSIZE = 15
FLOATSIZE = 20

.data
title_1         BYTE    "PROGRAMMING ASSIGNMENT 6: Designing low-level I/0 procedures",13,10,0
author          BYTE    "Written by Trevor Phillips",13,10,0
inst_1          BYTE    "Please provide 10 signed decimal integers.",13,10,0
inst_2          BYTE    "Each number needs to be small enough to fit inside a 32 bit register. ",
                        "After you have finished inputting the row numbers I will display a list ",
                        "of the integers, their sum, and their average value.",13,10,0

request_prompt  BYTE    "Please enter a signed number: ",0
input_error     BYTE    "ERROR: You did not enter a signed number or your number was too big.",13,10,0
try_again       BYTE    "Please try again: ",0
int_string      BYTE    INTEGERSIZE DUP(0)       ; Max SDWORD 2147483647
int_count       SDWORD  INTEGERSIZE
float_count     SDWORD  FLOATSIZE
output_int      SDWORD  0
int_portion     SDWORD  0
output_float    REAL4   0.0
sign_change     REAL4   -1.0
float_arr       REAL4   ARRAYSIZE DUP(?)
length_real     REAL4   10.0                     ; THIS MUST MATCH ARRAYSIZE CONSTANT
float_divisor   SDWORD  10
float_mult      REAL4   10.0                    
char_arr        BYTE    INTEGERSIZE DUP(0)
test_int        DWORD   52
nums_prompt     BYTE    "You entered the following numbers: ",13,10,0
sum_prompt      BYTE    "The sum of these numbers is: ",0
avg_prompt      BYTE    "The truncated average is: ",0
sum_val         SDWORD  0
line_count      SDWORD  1
valid_total     SDWORD  0
goodbye         BYTE    "Thanks for playing!",0
subtotal_prompt BYTE    "Your current subtotal: ",0
extra_1         BYTE    "**EC1: Numbers each line of user input and displays a running subtotal of user's valid integers.",13,10,0
extra_2         BYTE    "**EC2: ReadFloatVal implemented. The user string is converted to a REAL4 float. ",
                        "Unfortunately I could not figure out the WriteFloatVal implementation, ",
                        "so I used the IrvineLibrary WriteFloat Procedure to complete the rest of the implementation. ",
                        "I included my work anyway in case I can receive partial credit. ",13,10,0
float_string    BYTE    FLOATSIZE DUP(0)
float_intro     BYTE    "Now let's try an array with floating point numbers!",13,10,0
float_prompt    BYTE    "Please enter a floating point number (must include decimal point): ",0
float_error     BYTE    "ERROR: You did not enter a valid number or your number was too big.",13,10,0
float_read      BYTE    "Your float array is: ",0
float_sum       BYTE    "The sum of your floats is: ",0
float_avg       BYTE    "The average of your floats is: ",0
output_arr      SDWORD  ARRAYSIZE DUP(?)    ;Dup unitialized array of 10 SDWORDS.
integer_conv    SDWORD  ?
store_ascii     BYTE    INTEGERSIZE DUP(?)  
store_float     BYTE    FLOATSIZE DUP(?)



.code
main PROC
  finit
  ; introduce program to the user
  push  OFFSET extra_2
  push  OFFSET extra_1
  push  OFFSET title_1
  push  OFFSET author
  push  OFFSET inst_1
  push  OFFSET inst_2
  call  Introduction
  ; Set ECX counter to ARRAYSIZE and set EDI to output_arr for integer storage
  mov   ECX, ARRAYSIZE
  mov   EDI, OFFSET output_arr
  cld
  ; request integers from user and store as values in output_arr
_requestLoop:
  push  ECX
  push  OFFSET store_ascii
  push  OFFSET line_count
  push  OFFSET try_again
  push  OFFSET input_error
  push  int_count
  push  OFFSET int_string
  push  OFFSET request_prompt
  call  ReadVal
  STOSD             ; store integer in array
  pop   ECX
  ; display the current subtotal of the user's valid integers
  mov   EDX, OFFSET subtotal_prompt
  call  WriteString
  add   valid_total, EAX
  mov   EAX, valid_total
  push  OFFSET store_ascii
  call  WriteVal
  call  CrLf
  loop  _requestLoop
  ; Print user integers back to user
  call  CrLf
  mDisplayString OFFSET nums_prompt
  push  OFFSET store_ascii
  push  OFFSET output_arr
  call  ReadArray
  call  CrLf
  ; Compute and print sum of array
  mDisplayString OFFSET sum_prompt
  push  OFFSET output_arr
  call  SumArray
  push  OFFSET store_ascii
  call  WriteVal
  call  CrLf
  ; Compute and print truncated average
  mDisplayString OFFSET avg_prompt
  call  TruncatedAvg
  push  OFFSET store_ascii
  call  WriteVal
  call  CrLf
  call  CrLf
  ; Introduce floating point section

_floatingPoint:
  mov   ECX, ARRAYSIZE
  mDisplayString OFFSET float_intro
  call  CrLf
  mov   EDI, OFFSET float_arr
_floatRequestLoop:
  push  ECX
  push  OFFSET sign_change
  push  OFFSET float_divisor
  push  OFFSET int_portion
  push  OFFSET output_float
  push  OFFSET store_ascii
  push  OFFSET line_count
  push  OFFSET try_again
  push  OFFSET float_error
  push  float_count
  push  OFFSET float_string
  push  OFFSET float_prompt
  call  ReadFloatVal
  mov   EAX, output_float
  STOSD
  ; print current subtotal
   mDisplayString OFFSET subtotal_prompt
  push  OFFSET  float_arr
  call  SumFloats
  call  CrLf
  pop   ECX
  loop  _floatRequestLoop
  call  CrLf
  ; display the users floats
  mDisplayString OFFSET float_read
  push  OFFSET float_arr
  call  ReadFloatArray
  call  CrLf
  ; calculate and display the sum of the user floats
  mDisplayString OFFSET float_sum
  push  OFFSET  float_arr
  call  SumFloats
  call  CrLf
  ; calculate and display the average of the user's floats
  mDisplayString OFFSET float_avg
  push  OFFSET float_arr
  push  OFFSET length_real
  call  AvgFloats
  call  CrLf
  call  CrLf
  ; Say goodbye to the user
  mDisplayString OFFSET goodbye
  call  CrLf
  call  CrLf

	Invoke ExitProcess,0	; exit to operating system

main ENDP

;-----------------------------------------------------------------
;Name: Introduction
;
;Prints program title and gives instructions to user.
;
;Preconditions: Title and prompt strings in .code
;
;Postconditions: Introductory messages printed to user.
;
;Receives: inst_2 [EBP + 8], inst_1 [EBP + 12], author [EBP + 16],  title_1 [EBP + 20]
; extra_1 [EBP + 24] extra_2 [EBP + 28]
;
;Returns: None
;-----------------------------------------------------------------
Introduction    PROC
  push  EBP
  mov   EBP, ESP
  ; print Title and Author strings
  mDisplayString    [EBP + 20]
  mDisplayString    [EBP + 16]
  call  CrLF
  ; print user instructions
  mDisplayString    [EBP + 12]
  mDisplayString    [EBP + 8]
  call  CrLf
  mDisplayString    [EBP + 24]
  mDisplayString    [EBP + 28]
  call  CrLf
  pop   EBP
  ret   24

Introduction    ENDP
;-----------------------------------------------------------------
;Name: ReadVal
;
;Takes as input a user entered number (string), converts to an SDWORD integer and places in the EAX regsiter
; Number cannot exceed 32 bit regsiter size.
;
;Preconditions: Placeholder array in .code
;
;Postconditions: Introductory messages printed to user.
;
;Receives: request_prompt [EBP + 8], int_string (array of bytes representing ascii characters) [EBP + 12]
; integer_count [EBP + 16], input_error (message to user) [EBP + 20], try_again (message to user) [EBP + 24], 
; line_count [EBP + 28], store_ascii [EBP + 32] 
; 
;
;Returns: EAX (value entered by user), ECX (length of integer, not including sign).
;-----------------------------------------------------------------
ReadVal         PROC
  push  EBP
  mov   EBP, ESP
  ; save registers
  push  ESI
  push  EDI
  push  EBX

  ; prompt user for integer and save output as ASCII string at the EDX register
_getString:
  ; display and increment the lines of valid user input
  mov   EDI, [EBP + 28]     ; move line count to EDI
  mov   EAX, [EDI]
  push  [EBP + 32]          ; push store_ascii
  call  WriteVal
  inc   DWORD PTR [EDI]     ; increment line counter
  mov   EAX, "  "
  call  WriteChar
  ; Get user string
  mGetString    [EBP + 8], [EBP + 12], [EBP + 16]       ;prompt, output, count

  push  EAX             ; Save string length for later use
  ; if user input larger than INTEGERSIZE, jump to overflow
  cmp   EAX, INTEGERSIZE
  jg   _invalidInput

; move string address to ESI register
_prepareString:  
  mov   ESI, EDX
  mov   ECX, EAX        ; set ECX to string length
  CLD
  LODSB
; Check if first character is a sign
  cmp   AL, 43      ; + sign
  je    _nextChar
  cmp   AL, 45      ; - sign
  je    _nextChar

; Check if character is an integer (ASCII 48 - 57), if not integer jump to invalidInput
_intCheck:
  cmp   AL, 48
  jb    _invalidInput
  cmp   AL, 57
  ja    _invalidInput
; Check the next character until all characters checked
_nextChar:
  LODSB
  loop  _intCheck
  jmp   _store

; If the input is invalid or too large, request a new integer.
_invalidInput:
  pop   ECX
  ; display and increment the lines of valid user input
  mov   EDI, [EBP + 28]     ; move line count to ESI
  mov   EAX, [EDI]
  push  [EBP + 32]          ; push store_ascii
  call  WriteVal
  inc   DWORD PTR [EDI]     ; increment line counter
  mov   EAX, "  "
  call  WriteChar
  mDisplayString [EBP + 20]
  mGetString     [EBP + 24], [EBP + 12], [EBP + 16]
  push  EAX ; store string length
  jmp   _prepareString

; If all characters valid input, store the string as an integer.
_store:
  mov   ESI, [EBP + 12] ; mov string into ESI
  pop   ECX             ; pop string length into ECX
  mov   EAX, 0  
  mov   EDI, 0         
    
  LODSB
  cmp   AL, 45      ; if sign is negative, jump to negative processing
  je    _negNum
  cmp   AL, 43      
  jne   _posNum     ; if no positive sign jump to Convert Character Loop
  LODSB             ; if positive sign, move to the next byte
  dec   ECX         ; Decrease byte counter to account for sign byte and continue with positive loop.


; convert positive number string
_posNum:
  push  ECX         ; save ECX register as length counter
_posNumLoop:
  push  ECX
  sub   AL, 48      ; subtract 48 from each ASCII character to convert to integer equivalent
  cmp   ECX, 1
  je    _nextInt
  dec   ECX
  _tensPlace:               
    mov   EBX, 10   ; multiply each integer by its cooresponding place
    mul   EBX  
    loop  _tensPlace
; prepare for the nex integer
_nextInt:
  pop   ECX
  add   EDI, EAX            ; sum each digit tens value in EDI
  jo    _invalidInput       ; if overflow, request new integer from user
  mov   EAX, 0          
  LODSB                
  loop  _posNumLoop
  jmp   _storeNums

; if negative number
_negNum:
  LODSB
  dec   ECX         
  push  ECX         ; Save number of digits
_negUnpack:
  push  ECX         ; save ECX register
  sub   AL, 48      ; convert ASCII to integer (subtracting 48)
  cmp   ECX, 1
  je    _nextNegInt
  dec   ECX
; multiply digit into cooresponding tens place
  _negTensPlace:               
    mov   EBX, 10   
    mul   EBX
    loop  _negTensPlace
; prepare the next integer
_nextNegInt:
  pop   ECX
  sub   EDI, EAX        ; subtract each digit tens value in EDI
  jo    _invalidInput       ; if overflow, request new user from integer
  mov   EAX, 0        
  LODSB               
  loop  _negUnpack

; Store the number in EAX and put length of integer into ECX
_storeNums:
  mov   EAX, EDI        ; put value in EAX
  mov   ESI, [EBP + 12] ; mov string into ESI
  pop   ECX

; restore registers
  pop   EBX
  pop   EDI
  pop   ESI
  pop   EBP
  ret   28
ReadVal         ENDP
;-----------------------------------------------------------------
;Name: ReadFloatVal
;
;Takes as input a user entered number (string), converts to a REAL4 float value and pops the value from the FPU stack into the output_variable.
;
;Preconditions: None
;
;Postconditions: Float value in output array.
;
;Receives: float_prompt [EBP + 8], float_string (array of bytes representing ascii characters) [EBP + 12]
; float_count [EBP + 16], float_error (message to user) [EBP + 20], try_again (message to user) [EBP + 24], 
; line_count [EBP + 28], store_ascii [EBP + 32], output_float [EBP + 36], int_portion [EBP + 40], float_divisor [EBP + 44}
; sign_change [EBP + 48]
; 
;
;Returns: output_float
;-----------------------------------------------------------------
ReadFloatVal    PROC
  push  EBP
  mov   EBP, ESP
 
 ; save registers
  push  ESI
  push  EDI
  push  EBX

; prompt user for integer and save output as ASCII string at the EDX register
_getFloatString:
  ; display and increment the lines of valid user input
  mov   EDI, [EBP + 28]     ; move line count to EDI
  mov   EAX, [EDI]
  push  [EBP + 32]          ; push store_ascii
  call  WriteVal
  inc   DWORD PTR [EDI]     ; increment line counter
  mov   EAX, "  "
  call  WriteChar
  ; Get user string
  mGetString    [EBP + 8], [EBP + 12], [EBP + 16]       ;prompt, output, count
  push  EAX                                             ;save string length for later use

  ; if user input too large, jump to invalidInput
  cmp   EAX, 15
  jge   _invalidInput

; move string address to ESI register
_prepareString:  
  mov   ESI, EDX
  mov   ECX, EAX        ; set ECX to string length
  CLD
  LODSB

; Check if first character is a sign or radix
  cmp   AL, 43      ; + sign
  je    _nextChar
  cmp   AL, 45      ; - sign
  je    _nextChar
  cmp   AL, 46      ; .
  je    _nextChar

; Check if character is an integer (ASCII 48 - 57), if not integer jump to invalidInput
_intCheck:
  cmp   AL, 46
  je    _postRadix
  cmp   AL, 48
  jb    _invalidInput
  cmp   AL, 57
  ja    _invalidInput

; Check the next character until all characters checked
_nextChar:
  LODSB
  loop  _intCheck
  jmp   _floatStore

; Once the radix has been placed it cannot be placed again.
_postRadix:
  dec   ECX
  _postRadixLoop:
  LODSB
  cmp   AL, 48
  jb    _invalidInput
  cmp   AL, 57
  ja    _invalidInput
  loop  _postRadixLoop
  jmp   _floatStore

; If the input is invalid or too large, request a new integer.
_invalidInput:
  pop   ECX
  ; display and increment the lines of valid user input
  mov   EDI, [EBP + 28]     ; move line count to ESI
  mov   EAX, [EDI]
  push  [EBP + 32]          ; push store_ascii
  call  WriteVal
  inc   DWORD PTR [EDI]     ; increment line counter
  mov   EAX, "  "
  call  WriteChar
  mDisplayString [EBP + 20]
  mGetString     [EBP + 24], [EBP + 12], [EBP + 16]
  push  EAX ; store string length
  jmp   _prepareString

; store string as floating point integer
_floatStore:
  mov   ESI, [EBP + 12] ; mov string into ESI
  pop   ECX             ; pop string length into ECX
  mov   EAX, 0  
  mov   EDI, 0  
  mov   EDX, 0
    
; check the first character for sign or radix
  LODSB
  cmp   AL, 45      ; if sign is negative, jump to negative processing
  je    _negSign
  cmp   AL, 46      ; if first character radix, jmp to decimal processing
  je    _justDecimal
  cmp   AL, 43      
  jne   _posNum     ; if no positive sign jump to Convert Character Loop
  LODSB             ; if positive sign, move to the next byte
  dec   ECX         ; Decrease byte counter to account for sign byte and continue with positive loop.
  jmp   _posNum

; if only a decimal is entered decrease ECX counter
_justDecimal:
  dec   ECX
  mov   EDI, [EBP + 40]
  FILD  SDWORD PTR [EDI]
  jmp   _addDecimals

; if a negative sign entered decrease ECX and calculate remaining pre radix digits.
_negSign:
  LODSB
  dec   ECX
  push  ECX
  mov   EBX, 0
  _preRadixNeg:
  cmp   AL, 46
  je    _finishNeg
  inc   EBX
  LODSB
  loop  _preRadixNeg
  LODSB
  _finishNeg:
  mov   ESI, [EBP + 12] ; reload string into ESI
  mov   EDI, 0
  LODSB
  LODSB                 ; skip negative sign
  mov   ECX, EBX        ; place pre-radix integer counter into ECX
  mov   EBX, 10
  jmp   _intSumLoop

; convert positive number string
_posNum:
  push  ECX         ; save ECX register as length counter
  mov   EBX, 0
; determine how many digits come before the radix
_preRadix:
  cmp   AL, 46
  je    _addInts
  inc   EBX
  LODSB
  loop  _preRadix
  LODSB
; sum the preradix portion in EDI and add to the FPU stack
_addInts:
  mov   ESI, [EBP + 12] ; reload string into ESI
  mov   EDI, 0
  LODSB
  mov   ECX, EBX        ; place pre-radix integer counter into ECX
  mov   EBX, 10
_intSumLoop:
  sub   AL, 48
  push  ECX
  dec   ECX
  cmp   ECX, 0
  je    _nextInt
  mov   EBX, 10
  _tensPlace:               
    mul   EBX
    loop  _tensPlace
; prepare for the next integer
_nextInt:
  pop   ECX
  add   EDI, EAX        ; sum each digit tens value in EDI
  jo    _invalidInput       ; if overflow, request new integer from user
  mov   EAX, 0          
  LODSB                
  loop  _intSumLoop
  mov   EAX, EDI
  mov   EDI, [EBP + 40]     ; move int_portion address into EDI
  mov   [EDI], EAX
  FILD  DWORD PTR [EDI]

;add decimals using the FPU stack
_decimalAddition:
  pop   ECX
  dec   ECX                     ; to account for radix
  mov   EAX, 0
  mov   ESI, [EBP + 12]         ; move string address into ESI
  mov   EDI, [EBP + 40]         ; move int_portion addresss into EDI
  mov   SDWORD PTR [EDI], 0     ; reset int_portion to 0
  LODSB
  cmp   AL, 45
  jne   _numDecimals
  inc   ECX
  ; determine the number of decimals to be converted
  _numDecimals:
  cmp   AL, 46
  je    _addDecimals
  LODSB
  loop  _numDecimals

  ; add each decimal, using division by 10 to convert into proper place
_addDecimals:
  LODSB
  mov   EBX, 1
  _decimalLoop:
  sub   AL, 48
  mov   EDI, [EBP + 40]                 ; set EDI to integer
  mov   [EDI], EAX
  FILD  SDWORD PTR [EDI]                ; push first decimal onto stack
  push  EBX
  _decimalPlace:
    mov     EDI, [EBP + 44]
    FILD    SDWORD PTR [EDI]            ; push divisor of 10 onto the stack
    FDIV
    dec     EBX   
    cmp     EBX, 0
    jne     _decimalPlace
  pop   EBX
  inc   EBX
  FADD
  LODSB
  cmp   ECX, 0                    ; ECX will equal 0 when finished for negative inputs.
  je    _loadFloat
  loop  _decimalLoop

; Load float into output_float
_loadFloat:
  mov   EDI, [EBP + 40]
  mov   SDWORD PTR [EDI], 0       ; reset int_portion to 0
  mov   EDI, [EBP + 36]
  mov   EAX, 0
  mov   ESI, [EBP + 12]           ; check string for negative sign
  LODSB
  cmp   AL, 45
  jne   _enterFloat
  mov   ESI, [EBP + 48]          ; load negative one into FPU stack
  FLD   REAL4 PTR [ESI]
  FMUL
_enterFloat:
  FSTP  REAL4 PTR [EDI]           ; store in output float and pop off float stack

  ; restore registers
  pop   EBX
  pop   EDI
  pop   ESI

  pop   EBP
  ret   44
ReadFloatVal    ENDP
;-----------------------------------------------------------------
;Name: WriteVal
;
;Takes the integer stored in the EAX register and prints the number to the console as a string in decimal form.
;
;Preconditions: Number in EAX register
;
;Postconditions: EAX register printed as a decimal on the console.
;
;Receives: store_ascii (storage location for each integer in the number to be represented as an ASCII byte) [EBP+8] 
;
;Returns: None
;-----------------------------------------------------------------
WriteVal        PROC
  push  EBP
  mov   EBP, ESP
  ; Save registers
  push  EDI
  push  ECX
  push  EAX
  ; Move ASCII storage to EDI and set EDI pointer to the end of the array.
  mov   EDI, [EBP + 8]
  add   EDI, INTEGERSIZE
  ; Initialize EBX to 10 and clear EDX registers
  mov   EDX, 0
  mov   EBX, 10     
  std
  ; If integer is negative, jump to _convertNegative
  cmp   EAX, 0
  jl    _convertNegative

  ; Store each integer as an ASCII value
_PositiveWrite:
  div   EBX
  push  EAX         ; save quotient
  mov   EAX, EDX    ; store remainder in EDI
  add   EAX, 48
  STOSB
  mov   EDX, 0      ; reset EDX to 0
  pop   EAX         ; restore quotient
  cmp   EAX, 0      ; if quotient 0, done and time to print
  je    _print   
  jmp   _PositiveWrite

; Convert negative number to positive for writing
_convertNegative:
  mov   EBX, -1
  CDQ
  idiv  EBX
  mov   EBX, 10
  jmp   _PositiveWrite

; print ASCII storage register (EDI)
_print:
  pop   EAX
  push  EAX  
  cmp   EAX, 0
  jl    _addSign
  inc   EDI
  jmp   _printEDI
; add negative sign if negative number
_addSign:
  mov   EAX, 45
  STOSB
  inc   EDI
; print ASCII representation of number
  _printEDI:
  mDisplayString    EDI

; restore all ASCII storage values
  mov   ECX, ARRAYSIZE 
  mov   EAX, 0
  REP   STOSB
; restore registers
  pop   EAX
  pop   ECX
  pop   EDI
  pop   EBP
  ret   4
  
WriteVal        ENDP
;-----------------------------------------------------------------
;Name: ReadArray
;
; Prints a stored array to the console.
;
;Preconditions: Array exists in memory.
;
;Postconditions: Array printed to the screen with formatting.
;
;Receives: output_arr (the array to be printed) [EBP + 8], 
;store_ascii (storage for the ASCII string representation of each integer to be printed) [EBP + 12]
; 
;
;Returns: None
;-----------------------------------------------------------------
ReadArray       PROC  
  push  EBP
  mov   EBP, ESP
  mov   ECX, ARRAYSIZE  ; set counter equal to ARRAYSIZE
  mov   ESI, [EBP + 8]  ; move array to ESI

; write each value from the array and add formating (tab and ",")
_arrayPrint:
  mov   EAX, [ESI]
  push  [EBP + 12]      ; give ASCII storage to WriteVal
  call  WriteVal
  cmp   ECX, 1          ; if last integer in array, skip formatting
  je    _lastNum
  mov   EAX, ","
  call  WriteChar
  mov   EAX, "   "
  call  WriteChar
  add   ESI, 4
  loop  _arrayPrint

_lastNum:
  pop   EBP
  ret   8

ReadArray       ENDP
;-----------------------------------------------------------------
;Name: SumArray
;
;Takes as input an array of SDWORD integers and returns the sum of all the numbers in the array.
;
;Preconditions: Array in memory
;
;Postconditions: Array sum stored in EAX
;
;Receives: ouput_arr (the array to be stored) [EBP + 8]
; 
;Returns: EAX (the sum of the array)
;-----------------------------------------------------------------
SumArray        PROC
 push   EBP
 mov    EBP, ESP
 ; save registers
 push   ESI
 push   ECX

 mov    ESI, [EBP+8]        ; mov output_arr to ESI
 mov    EAX, 0
 mov    ECX, ARRAYSIZE      ; set counter equal to ARRAYSIZE
 _sumLoop:
 add    EAX, [ESI]          ; Add each value in output_arr (ESI) to EAX
 add    ESI, 4
 loop   _sumLoop
 ; restore registers
 pop    ECX
 pop    ESI

 pop    EBP

 ret    4

SumArray         ENDP
;-----------------------------------------------------------------
;Name: TruncatedAvg
;
;Takes as input the sum of the array and returns the average (truncated 
; so that  all numbers after the decimal place are removed).
;
;Preconditions: Sum of the array stored in EAX, ARRAYSIZE stored as constant
;
;Postconditions: Stores Truncated Average in EAX register.
;
;Receives: EAX (sum of array)
;
;Returns: EAX (Truncated Average)
;-----------------------------------------------------------------
TruncatedAvg    PROC
  push  EBP
  mov   EBP, ESP
  mov   EBX, ARRAYSIZE      ; Divide sum by the array size.
  mov   EDX, 0
  CDQ
  idiv  EBX

  pop   EBP
  ret

TruncatedAvg    ENDP
;-----------------------------------------------------------------
;Name: ReadFloatArray
;
;Takes as input an array of REAL4 floats and prints each float in the array to the console.
;
;Preconditions: Array stored in memory
;
;Postconditions: Prints each float to console.
;
;Receives: float_arr [EBP +8]
;
;Returns: None
;-----------------------------------------------------------------
ReadFloatArray  PROC
  push  EBP
  mov   EBP, ESP

  ; load array in ESI
  mov   ESI, [EBP + 8]
  mov   ECX, ARRAYSIZE

  ; read each float using irvine WriteFloat
_floatReadLoop:
  fstp  ST(0)       ; clear top of stack
  FLD   REAL4 PTR [ESI]
  call  WriteFloat
  cmp   ECX, 1
  je    _skipFormatting
  mov   EAX, ","
  call  WriteChar
  mov   EAX, "   "
  call  WriteChar
  add   ESI, 4
  _skipFormatting:
  loop  _floatReadLoop
  fstp  ST(0)       ; clear top of stack

  pop   EBP
  ret   4

ReadFloatArray  ENDP
;-----------------------------------------------------------------
;Name: SumFloats
;
;Takes as input an array of REAL4 floats, computes the sum and prints to console.
;
;Preconditions: Array stored in memory
;
;Postconditions: Prints sum of array to console.
;
;Receives: float_arr [EBP +8]
;
;Returns: None
;-----------------------------------------------------------------
SumFloats       PROC
  push  EBP
  mov   EBP, ESP

  ; load array into ESI
  mov   ESI, [EBP + 8]
  mov   ECX, ARRAYSIZE
  dec   ECX

  FLD   REAL4 PTR   [ESI]
  ; sum each float in array
  _floatSumLoop:
  add   ESI, 4
  FLD   REAL4 PTR [ESI]
  FADD
  loop  _floatSumLoop

  ; write sum stored at top of the stack
  call  WriteFloat
  mov   ECX, 0
  fstp  ST(0)       ; clear top of stack

  pop   EBP
  ret   4

SumFloats       ENDP
;-----------------------------------------------------------------
;Name: AvgFloats
;
;Takes as input an array of REAL4 floats, computes and prints the average of the array to the console.
;
;Preconditions: Array stored in memory.
;
;Postconditions: Prints array average to console.
;
;Receives: float_arr [EBP +8]
;
;Returns: None
;-----------------------------------------------------------------
AvgFloats       PROC
  push  EBP
  mov   EBP, ESP

  ; load array into ESI
  mov   ESI, [EBP + 12]
  mov   ECX, ARRAYSIZE
  dec   ECX

  FLD   REAL4 PTR   [ESI]
  ; sum each float in array
  _floatSumLoop:
  add   ESI, 4
  FLD   REAL4 PTR [ESI]
  FADD
  loop  _floatSumLoop

  ; load floating point length of array into ESI
  mov   ESI, [EBP + 8]
  FLD   REAL4 PTR [ESI]
  ; Divide sum by Arraysize
  FDIV
  call  WriteFloat


  pop   EBP
  ret   8  

AvgFloats       ENDP

END main
