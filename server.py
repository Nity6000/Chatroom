import socket
import threading

#Network port that will be used.
PORT = 6000
#Returns LOCAL IP of server.
SERVER_IP = socket.gethostbyname(socket.gethostname())
print("Server IPv4: " + SERVER_IP)
#Creates the address of the server.
SERVER_ADDRESS = (SERVER_IP, PORT)

#This the maximum bytes possible for a message
MESSAGE_HEADER = 64
#The messages will be encoded and decoded with utf-8
MESSAGE_FORMAT = 'utf-8'
#This message will signify that the client is closing
MESSAGE_DISCONNECT = "/DISCONNECT"

#Init Server Socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(SERVER_ADDRESS)

client_list = []

#Starts listening for and handles new connections.
def server_start():
    server_sock.listen()
    while True:
        #Gets data from the client, and creates a new thread to interact with the client.
        connection, address = server_sock.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        client_list.append(connection)
        print(f"Active Connections: {threading.activeCount() - 5}")

#Handle data from client being sent through sockets
def handle_client(connection, address):
    print(f"New Connection from [{address}]")

    client_connected = True
    #Listens for the client to send data.
    while client_connected:
        #The client always sends a protocol message with the length of the incoming message.
        #This message will tell the server exactly how many bytes it needs to recieve.
        #For now the server can only get a set number of bytes, the HEADER.
        message_length = connection.recv(MESSAGE_HEADER).decode(MESSAGE_FORMAT)
        if message_length:
            message_length = int(message_length)
            message = connection.recv(message_length).decode(MESSAGE_FORMAT)
            #Checks for a special client message that signifies a disconnection.
            if message == MESSAGE_DISCONNECT:
                client_connected = False
                client_list.remove(connection)
            else:
                print(f"[{address}]: {message} ({message_length})")
                broadcast_message(message, connection)

    connection.close

def broadcast_message(message, connection):
    for clients in client_list:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                client_list.remove(connection)

print("Server Online")
server_start()