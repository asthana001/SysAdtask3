import socket
import select
import sys

# defining some constants
HEADER_LEN = 10
IP = '127.0.0.1'
PORT = 6060

# making socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

'''list of all sockets connected to the chat application.
 initially there is only one server socket but as the clients get connected, they will be added here '''
socket_list = [server_socket]

# creating a dictionary of clients with their username linked to their ip
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')


# defining a function to receive msg from any client socket

def receive_msg(c_socket):
    try:
        message_header = c_socket.recv(HEADER_LEN)  # receiving the header length from the client socket

        # if nothing is received or length of header = 0
        if not len(message_header):
            return False

        # length of message
        message_length = int(message_header.decode("utf-8").strip())

        # returning a dictionary with value as header and key as data
        return {"header": message_header, "data": c_socket.recv(message_length)}

    except:
        return False


while True:

    # select.select reads from socket_list, writes on empty list and error on socket_list
    read_sockets, _, exception_socket = select.select(socket_list, [], socket_list)

    # notified_socket is iterating variable in list : read_sockets
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # means someone connected and we need to accept the connection

            # accepting the connection

            client_socket, client_addr = server_socket.accept()

            # calling the receive message function
            user = receive_msg(client_socket)

            if user is False:
                continue
            else:
                # will add this socket to the socket_list
                socket_list.append(client_socket)

            clients[client_socket] = user  # user is a dictionary of data form the receive msg function

            print("Accepted new connection from username: ", user['data'].decode('utf-8'))

        else:
            message = receive_msg(notified_socket)

            if message is False:
                print("Connection closed from", clients[notified_socket]['data'].decode('utf-8'))

                # removing that socket
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print("Received message form", user['data'].decode('utf-8'), ":", message['data'].decode('utf-8'))


            # sharing message with everybody
            for client_socket in clients:
                if client_socket != notified_socket:
                    if message['data'] != 'quit' or message['data'] != 'chat-history':
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    if message['data'] == 'quit':
                        client_socket.send(user['header'] + user['data'] + "left the chat")


    # handling sockets in exception socket list
    for notified_socket in exception_socket:
        socket_list.remove(notified_socket)
        del clients[notified_socket]

