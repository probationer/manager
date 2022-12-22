import socket


host = ('0.0.0.0', 5000)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with soc as s:
    s.bind(host)
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        # 
        while True:
            data = conn.recv(1024)
            print('data:', data)
            conn.sendall(data)
            if not data:
                break