import socket
from tictactoe import Tictactoe

def respondTictactoe():
    if input() == "yes":
        print("Match accepted! Waiting for move...")
        msg = "yes"
    else:
        print("Match rejected. Continue chat...")
        msg = "Match rejected."
    return msg

def requestMatch():
    size = int(input("Enter board size (integer: 3 - 9): "))
    win_length = int(input("Enter win length (integer: 3 - Board Size): "))
    game = Tictactoe("x", size, win_length)
    msg = f"Incoming tictactoe request size: {size} by {size}, win length: {win_length}. Type yes to accept."
    conn.sendall(bytes(msg, "utf-8"))
    print("Waiting for response...")

    clientMessage = conn.recv(1024).decode("utf-8")

    if clientMessage == "yes":
        print("Match accepted!")
        print()
        return game
    else:
        print("Match rejected. Waiting for client message...")
        return False


def makeMove(game, conn):
    game.printBoard()
    mark = (input("Enter a row-column coordinate pair to mark (e.g.: \"A3\", \"D4\"): "))
    game.placeMarker(mark)
    game.printBoard()

    if game.checkWin():
        print("Game over! Waiting for message...")
        conn.sendall(bytes("Game over!", "utf-8"))
        conn.sendall(bytes(mark, "utf-8"))
        return None

    conn.sendall(bytes(mark, "utf-8"))
    print("Waiting for opponent's move...")
    return game

def receiveMove(coordinates):
    game.placeOpponent(coordinates)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Make port reusable
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set socket to listen for connections.
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on: {HOST} on port: {PORT}")
    print("Type /q to quit")
    print("Enter message to send. Please wait for input prompt before entering message...")
    print("Note: Type \"play tictactoe\" to start a game of tictactoe")

    # Accept connection
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    print("Waiting for message...\n")

    with conn:
        while True:

            # Receive and print client message.
            clientMessage = conn.recv(1024).decode("utf-8")
            print(clientMessage)

            # Client requested shut down.
            if clientMessage == "/q":
                print("Client has requested shut down. Shutting down!")
                conn.close()
                break

            # Respond to tictactoe request.
            if clientMessage[:18] == "Incoming tictactoe":
                size, win_length = int(clientMessage[33]), int(clientMessage[53])
                msg = respondTictactoe()
                conn.sendall(bytes(msg, "utf-8"))

                if msg == "yes":
                    game = Tictactoe("o", size, win_length)
                    while game:
                        clientMessage = conn.recv(1024).decode("utf-8")
                        if clientMessage == "Game over!":
                            lastMark = conn.recv(1024).decode("utf-8")
                            receiveMove(lastMark)
                            game.printBoard()
                            game = False
                            print("Game over!")
                            break
                        receiveMove(clientMessage)
                        makeMove(game, conn)
                    continue


            # Prompt server user for input and send to client
            msg = input("Enter Input >")

            # Server requests shut down.
            if msg == "/q":
                conn.sendall(bytes(msg, "utf-8"))
                print("Shutting Down!")
                conn.close()
                break

            if msg == "play tictactoe":
                game = requestMatch()
                while game:
                    game = makeMove(game, conn)
                    if not game:
                        break
                    clientMessage = conn.recv(1024).decode("utf-8")
                    receiveMove(clientMessage)
                continue

            conn.sendall(bytes(msg, "utf-8"))
