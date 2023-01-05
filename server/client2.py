import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = input("Client two enter your message: ")
    s.send(data.encode('utf-8'))
    data = s.recv(1024)
    print(f"Received {data!r}")