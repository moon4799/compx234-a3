import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 51234))
server_socket.listen(1)
print("Server is listening on port 51234...")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")
data = conn.recv(1024).decode()
print(f"Received from client: {data}")
conn.sendall("Hello from server".encode())
conn.close()
