import socket
from _thread import *
server_socket = socket.socket()

host = "0.0.0.0"
port = 5000
ThreadCount = 0
sender_ip = '192.168.1.5'
connection_pool = dict()
thread_ident_index = dict()
client_mapping = {
    "0" : "1",
    "1" : "0"
}

try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))
print("wating for connection")
server_socket.listen(5)


def create_sender_connection(sender_ip_address, sender_port=port):
    # set port of sender IP address
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.bind((sender_ip_address, 4567))
    conn, address = sender_socket.accept()
    # print('sender address : ', address[0], address[1])
    return conn


def alternate_connection(index):
    pass
    return connection_pool[index]


def client_thread(connection):
    thread_ident = get_ident()
    print("thread indent : ", thread_ident)
    connection_pool[str(ThreadCount-1)] = connection
    thread_ident_index[thread_ident] = str(ThreadCount-1)

    # connection.send(b"welcome to the server")

    for i in range(0,10000):
        print('Loop iteration : ', i)
        if i == 0: 
            data = connection.recv(1024)
            print('Data from client : ', data)
            connection.send(data)
            continue
        sender_index = client_mapping[thread_ident_index[thread_ident]]
        sending_connection = connection_pool[sender_index]
        print('Current Index : ', thread_ident_index[thread_ident])
        print('sender_index : ', sender_index)
        print('Thread Id : ', thread_ident)
        data = connection.recv(1024)
        print('Data from client : ', data)
        if not data:
            break
        sending_connection.send(data)

    sending_connection.close()


while True:
    client, address = server_socket.accept()
    print('client : ', client)
    print("connected to " + address[0] + str(address[1]))
    start_new_thread(client_thread, (client, ))
    ThreadCount += 1
    print("Thread Count : " + str(ThreadCount))
    # server_socket.close()
