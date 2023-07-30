import socket
from _thread import *
import struct
import time
server_socket = socket.socket()

host = "0.0.0.0"
port = 5000
ThreadCount = 0
connection_pool = dict()
thread_ident_index = dict()
client_mapping = {
    "0" : "1",
    "1" : "0"
}
HeaderSize = 10
bufferSize = 10240
max_size =  0

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

def proxy_data(sender_index, thread_ident, connection):
    sending_connection = connection_pool[sender_index]
    print('---------------------------')
    print('1. Current Index : ', thread_ident_index[thread_ident])
    print('2. Sender_index : ', sender_index)
    print('3. Thread Id : ', thread_ident)
    meta_values = connection.recv(5)
    print('3.1 Meta value recieved ', meta_values)
    if (len(meta_values)) >= 5 :

        print('3.2 got len of data : ', meta_values)
        imtype, le = struct.unpack("<BI", meta_values)
        print('4. data len from client : ',imtype, le)
        imb = b''
        while le > bufferSize:
            t = connection.recv(bufferSize)
            print(' Receving buffer ...')
            imb += t
            le -= len(t)
        while le > 0:
            t = connection.recv(le)
            print(' Receving remaining buffer ...')
            imb += t
            le -= len(t)

        print('5. length of recv data : ', len(imb))
        
        sending_connection.sendall(meta_values)
        sending_connection.sendall(imb)
    else:
        print('5.1. value less than 5 : ', meta_values , ' | ',  len(meta_values))
        time.sleep(2)
        sending_connection.sendall(meta_values)

def client_thread(connection):
    global max_size
    thread_ident = get_ident()
    print("thread indent : ", thread_ident)
    connection_pool[str(ThreadCount-1)] = connection
    thread_ident_index[thread_ident] = str(ThreadCount-1)

    while True:
        sender_index = client_mapping[thread_ident_index[thread_ident]]
        try:   
            proxy_data(sender_index, thread_ident, connection)
        except Exception as err:
            print('6. Error! I guess no Sender ', err)
            time.sleep(2)
            proxy_data(sender_index, thread_ident, connection)


while True:
    client, address = server_socket.accept()
    # client.setblocking(0)
    print('client : ', client)
    print("connected to " + address[0] + str(address[1]))
    start_new_thread(client_thread, (client, ))
    ThreadCount += 1
    print("Thread Count : " + str(ThreadCount))
    # server_socket.close()
