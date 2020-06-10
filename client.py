import socket
import select
import errno
import sys

# defining some constants
HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 6060

history = []

# creating username
my_username = input("Enter your username: ")

# creating the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# start sending username to server
username = my_username.encode('utf-8')
username_header = f"{len(username):< {HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)



# send and receive messages
while True:
    message = input(f"{my_username} > ")

    if message:

        # if this a real message and not a blank one, we send it to the server
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

        # user can download their chat history by typing "chat-history"
        if message.decode('utf-8') == "chat-history":
            with open(my_username + ".txt", "w") as file:
                for line in history:
                    file.write(line)
                    file.write("\n")
        else:
            history.append(f"{my_username} > {message.decode('utf-8')}")

        # user can quit the chat by typing "quit"
        if message.decode('utf-8') == "quit":
            print("You have ended the chat")
            sys.exit()



    try:
        # receiving the chats
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by server")
                sys.exit()

            username_length = int(username_header.decode('utf-8'))
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')

            print(username, ">", message)

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
