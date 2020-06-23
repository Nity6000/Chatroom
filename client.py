import socket

#Network port that will be used.
PORT = 6000
#This IP is of the server which is on the SAME network.
SERVER_IP = "192.168.1.200"
#Creates the address of the server.
SERVER_ADDRESS = (SERVER_IP, PORT)

#This the maximum bytes possible for a message
MESSAGE_HEADER = 64
#The messages will be encoded and decoded with utf-8
MESSAGE_FORMAT = 'utf-8'
#This message will signify that the client is closing
MESSAGE_DISCONNECT = "/DISCONNECT"

#Intiilizes a socket from the client's end.
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(SERVER_ADDRESS)

def send_message(message):

    message = message.encode(MESSAGE_FORMAT)

    #Finds the length of the message in characters.
    message_length = len(message)
    #Finds the length of the message in bytes.
    message_length_bytes = str(message_length).encode(MESSAGE_FORMAT)
    #This pads the message so that it takes up exactly the HEADER number of bytes
    message_length_bytes += b' ' * (MESSAGE_HEADER - len(message_length_bytes))

    #The message_length must be sent first, or else the server won't know how many bytes to recieve.
    client_sock.send(message_length_bytes)
    client_sock.send(message)
    
    print(client_sock.recv(2048).decode(MESSAGE_FORMAT))

send_message("Hello World!!!")

