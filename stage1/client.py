import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 51234))
client_socket.sendall("Hello from client".encode())
data = client_socket.recv(1024).decode()
print(f"Received from server: {data}")
client_socket.close()
