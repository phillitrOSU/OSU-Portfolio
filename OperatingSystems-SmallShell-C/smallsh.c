#define _POSIX_C_SOURCE 200809L
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#include <errno.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdint.h>
#include <fcntl.h>

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif

// Initialize built in commands.
static void exit_shell(int exit_status);
static void change_dir(char* path);

// Initialize status and process ID variables.
static int status = 0;
static int bgstatus;
int childStatus;
pid_t childPid = -5;
pid_t most_recent_bg_process = -5;

// Initialize input handling/word splitting functions.
char *words[MAX_WORDS];
size_t wordsplit(char const *line);
char * expand(char const *word);

//Initialize sig handling functions and default sigaction structs.
void handle_SIGINT(int signo){}
void handle_SIGTSTP(int signo){}
struct sigaction default_SIGINT = {0};
struct sigaction builtin_SIGINT = {0};
struct sigaction default_SIGTSTP = {0};
struct sigaction SIGINT_action = {0};
struct sigaction SIGTSTP_action = {0};

int main(int argc, char *argv[])
{
 
  //Define signal handling structures.

  // Special case SIGINT handler for getline function.
  SIGINT_action.sa_handler = handle_SIGINT;
  sigfillset(&SIGINT_action.sa_mask);
  SIGINT_action.sa_flags = 0;

  //Default handler for SIGINT.
  default_SIGINT.sa_handler = SIG_IGN;
  sigfillset(&default_SIGINT.sa_mask);
  default_SIGINT.sa_flags = 0;
  sigaction(SIGINT, &default_SIGINT, &builtin_SIGINT);

  //SIGTSTP handler.
  SIGTSTP_action.sa_handler = SIG_IGN; //Smallsh ignores SIGTSTP: ctrl+z
  sigfillset(&SIGTSTP_action.sa_mask);
  SIGTSTP_action.sa_flags = 0;
  sigaction(SIGTSTP, &SIGTSTP_action, &default_SIGTSTP);

  /*Default input = stdin. File if argument*/
  FILE *input = stdin;
  char *input_fn = "(stdin)";
  if (argc == 2) {
    input_fn = argv[1];
    input = fopen(input_fn, "re"); //open to read "r" with cloexec flag "e".
    if (!input) err(1, "%s", input_fn);    
  } else if (argc > 2) {
    errx(1, "too many arguments");
  }

  char *line = NULL;
  size_t n = 0;

  //Infinite shell loop.
  for (;;) {

prompt:;
    /* Manage background processes */

    //Handle completed background processes.
    pid_t completed_bgprocess = waitpid(-1, &childStatus, WNOHANG);
    if(completed_bgprocess > 0){
      if(WIFSIGNALED(childStatus)){ //Handle signaled background processes.
        fprintf(stderr, "Child process %jd done. Signaled %d.\n", (intmax_t) completed_bgprocess, WTERMSIG(childStatus));
      }
      else { //Handle normallly exited background proceesses.
	if(WIFSTOPPED(childStatus)) bgstatus = WSTOPSIG(childStatus);
	if(WIFSIGNALED(childStatus)) bgstatus = WTERMSIG(childStatus);
	if(WIFEXITED(childStatus)) bgstatus = WEXITSTATUS(childStatus);
	fprintf(stderr, "Child process %jd done. Exit status %d.\n", (intmax_t) completed_bgprocess, bgstatus);
      }
    }

    //Handle stopped background processes.
    pid_t stopped_bgprocess= waitpid(-1, &childStatus, WNOHANG | WUNTRACED);
    if(stopped_bgprocess > 0){
      if(WIFSTOPPED(childStatus)){
        fprintf(stderr, "Child process %jd stopped. Continuing.\n", (intmax_t) stopped_bgprocess);
	kill(stopped_bgprocess, SIGCONT); //continue process.
      }
    }
   

    /* print prompt */
    if (input == stdin) {
	char* PS1 = getenv("PS1");
	//char* PS1 = "$_";
	fprintf(stderr, "%s", PS1); //print prompt
    }
    
    
    sigaction(SIGINT, &SIGINT_action, NULL);
    ssize_t line_len = getline(&line, &n, input);
    if (line_len < 0) {
      if (feof(input)){ //exit if end of input file.
	exit(0);
      }
      else{
        fprintf(stderr,"\n"); //handle sigint
        clearerr(stdin);
        goto prompt;
      }
    }
    sigaction(SIGINT, &default_SIGINT, NULL);
    

    if (line[0] == '\n' && line_len == 1) goto prompt; // return to prompt if empty line.

    
    size_t nwords = wordsplit(line);

    //Expand words in words array.
    for (size_t i = 0; i < nwords; ++i) {
      char *exp_word = expand(words[i]);
      free(words[i]);
      words[i] = exp_word;
    }

    /*Parse words*/
    int end_index = (int)nwords;
    int bg_operator = 0;
    char* arg_array[512] = {NULL};
    char* outfile = {NULL};
    char* infile = {NULL};
    char* appendfile = {NULL};
    
    //Check for background operator.
    if (end_index > 0 && strcmp(words[end_index - 1], "&") == 0) {
      bg_operator = 1; // set background operator
      words[end_index - 1] = NULL; 
      end_index = end_index - 1; // Decrease end index if background operator found.
    }

    int fdout, fdin, result_in, result_out;
    //Copy commands into arg array. Handle redirection operators separately.
    for(int i = 0; i < end_index; i++){

      if(strcmp(words[i], "<") == 0){
        infile = words[i+1];
	fdin = open(infile, O_RDONLY);
	i++;
	continue;
      }

      if(strcmp(words[i], ">") == 0){
        outfile = words[i+1];	
	fdout = open(outfile, O_RDWR | O_CREAT | O_TRUNC, 0777);
	i++;
	continue;
      }

      if(strcmp(words[i], ">>") == 0){
	outfile = words[i+1];
	fdout = open(outfile, O_RDWR | O_CREAT | O_APPEND, 0777);
	i++;
	continue;
      }
 
      else{
	char* tmp = strdup(words[i]);
	arg_array[i] = tmp;
      }
    }

    /*//ARG ARRAY PRINTER FOR TESTING PURPOSES ONLY.
    printf("\nArgs array = {");
    for (int i = 0; i < nwords; ++i){
      printf("%s, ", arg_array[i]);
    }
    printf("}\n");
    fflush(stdout);*/



    // Check for built-in commands.
    if (strcmp(words[0], "exit") == 0){ 			//check for exit
      if (arg_array[1]){
        status = atoi(words[1]);
      }
      if (arg_array[2]){ 					//if more than one argument provided print error.
        fprintf(stderr, "exit: too many arguments\n");
	status = 1;
	goto prompt;
      }
      exit(status);
    }

    else if (strcmp(words[0], "cd") == 0){  			//check for cd
      if(arg_array[2]){
        fprintf(stderr, "cd: too many arguments\n");
	status = 1;
	goto prompt;
      }
      if(arg_array[1]){
        char* new_dir = arg_array[1];
	change_dir(new_dir);
      }
      else{
        char* new_dir = getenv("HOME");
	change_dir(new_dir);
      };
    }
    
    
    //Otherwise try to execute command in new child process
    else{
      childPid = fork();

      switch(childPid){
	case -1:
	  perror("fork() failed!\n");
	  status = 1;
	  exit(1);
	  goto prompt;

	case 0:
          // Reset child signals
	  sigaction(SIGINT, &builtin_SIGINT, NULL);
	  sigaction(SIGTSTP, &default_SIGTSTP, NULL);


	  // Set outfile if specified.
	  if(outfile){
           if((result_out = dup2(fdout, 1)) == -1){
	     perror("dup2 stdout");
	     exit(2);
	   }
	  }
         
	  // Set input file if specified.
          if(infile){
            if((result_in = dup2(fdin, 0)) == -1){
	      perror("dup2 stdin");
	      exit(2);
	    }
	  }
          
	  // Execute command.
	  execvp(arg_array[0], arg_array);

	  // Exit with error if command returns.
	  status = 1;
	  perror("execvp");
	  exit(127);
	  goto prompt;

        default:
	  //if background command set background pid and return to prompt immediately without waiting.
	  if(bg_operator) {
            most_recent_bg_process = childPid;
	    goto prompt;
	  }
	  
	  // Otherwise wait for child and update status.
	  childPid = waitpid(childPid, &childStatus, WUNTRACED);
	  
	  if(childPid == -1){ //If SIGINT...
	    childPid = waitpid(childPid, &childStatus, WUNTRACED);
	    goto prompt;
	  }
          
	  //Child exited normally.
	  else if (WIFEXITED(childStatus)){
	    status = WEXITSTATUS(childStatus);
	  }
          
	  //Child stopped.
	  else if (WIFSTOPPED(childStatus)){
	    most_recent_bg_process = childPid;
	    fprintf(stderr, "Child process %jd stopped. Continuing.\n", (intmax_t) most_recent_bg_process);
	    kill(childPid, SIGCONT);
	  }
         
	  //Child signalled.
	  else if (WIFSIGNALED(childStatus)){
            status = 128 + WTERMSIG(childStatus);
	  }

	  else {}
          break;
        }
    }

  //free args array
  for(int i = 0; i < nwords; ++i){
    free(arg_array[i]);
  }

  } 		// end for loop
}


//change directory
void change_dir(char* path){
  if(chdir(path) != 0) {
    status = 1;
    perror("cd error");
  }
  else status = 0;
}


char *words[MAX_WORDS] = {0};

/* Splits a string into words delimited by whitespace. Recognizes
 * comments as '#' at the beginning of a word, and backslash escapes.
 *
 * Returns number of words parsed, and updates the words[] array
 * with pointers to the words, each as an allocated string.
 */
size_t wordsplit(char const *line) {
  size_t wlen = 0;
  size_t wind = 0;

  char const *c = line;
  for (;*c && isspace(*c); ++c); /* discard leading space */

  for (; *c;) {
    if (wind == MAX_WORDS) break;
    /* read a word */
    if (*c == '#') break;
    for (;*c && !isspace(*c); ++c) {
      if (*c == '\\') ++c;
      void *tmp = realloc(words[wind], sizeof **words * (wlen + 2));
      if (!tmp) err(1, "realloc");
      words[wind] = tmp;
      words[wind][wlen++] = *c; 
      words[wind][wlen] = '\0';
    }
    ++wind;
    wlen = 0;
    for (;*c && isspace(*c); ++c);
  }
  return wind;
}


/* Find next instance of a parameter within a word. Sets
 * start and end pointers to the start and end of the parameter
 * token.
 */
char
param_scan(char const *word, char const **start, char const **end)
{
  static char const *prev;
  if (!word) word = prev;
  
  char ret = 0;
  *start = 0;
  *end = 0;
  for (char const *s = word; *s && !ret; ++s) {
    s = strchr(s, '$');
    if (!s) break;
    switch (s[1]) {
    case '$':
    case '!':
    case '?':
      ret = s[1];
      *start = s;
      *end = s + 2;
      break;
    case '{':
      char *e = strchr(s + 2, '}');
      if (e) {
        ret = s[1];
        *start = s;
        *end = e + 1;
      }
      break;
    default:
     continue;
    }
    break;
  }
  prev = *end;
  return ret;
}

/* Simple string-builder function. Builds up a base
 * string by appending supplied strings/character ranges
 * to it.
 */
char *
build_str(char const *start, char const *end)
{
  static size_t base_len = 0;
  static char *base = 0;

  if (!start) {
    /* Reset; new base string, return old one */
    char *ret = base;
    base = NULL;
    base_len = 0;
    return ret;
  }
  /* Append [start, end) to base string 
   * If end is NULL, append whole start string to base string.
   * Returns a newly allocated string that the caller must free.
   */
  size_t n = end ? end - start : strlen(start);
  size_t newsize = sizeof *base *(base_len + n + 1);
  void *tmp = realloc(base, newsize);
  if (!tmp) err(1, "realloc");
  base = tmp;
  memcpy(base + base_len, start, n);
  base_len += n;
  base[base_len] = '\0';
  return base;
}

/*Return a string from a pid_t value*/
char *
stringify_pid(pid_t pid_num, char* pid_string)
{
  pid_string += sprintf(pid_string, "%jd", (intmax_t)pid_num);
}


/* Expands all instances of $! $$ $? and ${param} in a string 
 * Returns a newly allocated string that the caller must free
 */
char *
expand(char const *word)
{
  char const *pos = word;
  char const *start, *end;
  char c = param_scan(pos, &start, &end); //Set c to character after '$'. Param start/end pointers.
  build_str(NULL, NULL);
  build_str(pos, start); //Replicate non-paramater beginning of string.
  while (c) {

    //Expand background process pid.
    if (c == '!'){
      char* pid_string = malloc(20);
      stringify_pid(most_recent_bg_process, pid_string);
      if(most_recent_bg_process > 0) build_str(pid_string, NULL);
      else build_str("",NULL);
      free(pid_string);
    }

    //Expand pid of smallsh.
    else if (c == '$'){
      char* pid_string = malloc(20);
      pid_t pid_num = getpid();
      stringify_pid(pid_num, pid_string);
      build_str(pid_string, NULL);
      free(pid_string);
    }

    //Expand exit status of most recent foreground command.
    else if (c == '?'){
      char* status_string = malloc(20);
      sprintf(status_string, "%d", status);
      build_str(status_string, NULL);
      free(status_string);
    }
   
    //Expand parameter
    else if (c == '{') {
      char param_token[256] = {'\0'};
      int token_len = end - start - 3;
      strncpy(param_token, start + 2, token_len);
      char env_string[256] = {'\0'};
      if(param_token){
        if(getenv(param_token))strcpy(env_string, getenv(param_token));
      }   
      build_str(env_string, NULL);
    }

    //Check for additional paramters to expand.
    pos = end;
    c = param_scan(pos, &start, &end); 					//If paramater, while loop re-executes.
    build_str(pos, start);
  }

  return build_str(start, NULL);
}

