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
    s.sendall(bytes(msg, "utf-8"))
    print("Waiting for response...")

    serverMessage = s.recv(1024).decode("utf-8")

    if serverMessage == "yes":
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
        s.sendall(bytes("Game over!", "utf-8"))
        s.sendall(bytes(mark, "utf-8"))
        return None

    s.sendall(bytes(mark, "utf-8"))
    print("Waiting for opponent's move...")
    return game


def receiveMove(coordinates):
    game.placeOpponent(coordinates)



import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to: {HOST} on port: {PORT}")
    print("Type /q to quit")
    print("Enter message to send. Please wait for input prompt before entering message...")
    print("Note: Type \"play tictactoe\" to start a game of tictactoe\n")

    while True:
        # Prompt client user for input and send to server.
        msg = input("Enter Input >")

        # Client requests shut down.
        if msg == "/q":
            s.sendall(bytes(msg, "utf-8"))
            print("Shutting Down!")
            s.close()
            break

        if msg == "play tictactoe":
            game = requestMatch()
            while game:
                game = makeMove(game, s)
                if not game:
                    break
                serverMessage = s.recv(1024).decode("utf-8")
                receiveMove(serverMessage)
            continue

        s.sendall(bytes(msg, "utf-8"))

        # Wait for and print response from server.
        serverMessage = s.recv(1024).decode("utf-8")
        print(serverMessage)

        # Server requested shut down.
        if serverMessage == "/q":
            print("Server has requested shut down. Shutting down!")
            s.close()
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

        # Respond to tictactoe request.
        if serverMessage[:18] == "Incoming tictactoe":
            size, win_length = int(serverMessage[33]), int(serverMessage[53])
            msg = respondTictactoe()
            s.sendall(bytes(msg, "utf-8"))

            if msg == "yes":
                game = Tictactoe("o", size, win_length)
                while game:
                    serverMessage = s.recv(1024).decode("utf-8")
                    if serverMessage == "Game over!":
                        lastMark = s.recv(1024).decode("utf-8")
                        receiveMove(lastMark)
                        game.printBoard()
                        game = False
                        print("Game over!")
                        break
                    receiveMove(serverMessage)
                    makeMove(game, s)
                continue
