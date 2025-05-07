# server.py
from tuplespace import TupleSpace
import socket
import threading


def handle_client(client_socket, tuple_space):
    while True:
        request = client_socket.recv(1024).decode().strip()
        if not request:
            break

        parts = request.split()  # 分割请求
        print(f"Received parts: {parts}")  # 调试打印

        command = parts[0]  # 提取命令

        if command == 'PUT':
            if len(parts) != 3:  # 确保 PUT 命令格式正确
                result = "ERR Invalid PUT command format"
            else:
                k = parts[1]  # 提取 key
                v = parts[2]  # 提取 value
                result = tuple_space.put(k, v)  # 调用 PUT 操作

        elif command == 'READ':
            if len(parts) != 2:  # 确保 READ 命令格式正确
                result = "ERR Invalid READ command format"
            else:
                k = parts[1]  # 提取 key
                result = tuple_space.read(k)  # 调用 READ 操作

        elif command == 'GET':
            if len(parts) != 2:  # 确保 GET 命令格式正确
                result = "ERR Invalid GET command format"
            else:
                k = parts[1]  # 提取 key
                result = tuple_space.get(k)  # 调用 GET 操作

        else:
            result = "ERR Unknown command"  # 未知命令

        client_socket.send(result.encode())  # 发送响应给客户端


def start_server(host, port):
    tuple_space = TupleSpace()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, tuple_space))
        client_thread.start()

if __name__ == "__main__":
    start_server("localhost", 51234)
