from tuplespace import TupleSpace
import socket
import threading

# 线程锁，确保操作的线程安全
lock = threading.Lock()

def handle_client(client_socket, tuple_space):
    while True:
        request = client_socket.recv(1024).decode().strip()

        if not request:
            break

        parts = request.split()  # 分割请求
        print(f"Received parts: {parts}")  # 调试打印

        command = parts[0]  # 提取命令
        result = ""  # 初始化响应

        # 对不同命令进行处理
        with lock:  # 使用锁确保线程安全
            if command == 'PUT':
                if len(parts) != 3:  # 确保 PUT 命令格式正确
                    result = "024 ERR Invalid PUT command format"
                else:
                    k = parts[1]  # 提取 key
                    v = parts[2]  # 提取 value
                    # 判断是否已经存在该 key
                    if tuple_space.exists(k):
                        result = f"024 ERR {k} already exists"
                    else:
                        tuple_space.put(k, v)  # 调用 PUT 操作
                        result = f"021 OK ({k}, {v}) added"

            elif command == 'READ':
                if len(parts) != 2:  # 确保 READ 命令格式正确
                    result = "024 ERR Invalid READ command format"
                else:
                    k = parts[1]  # 提取 key
                    value = tuple_space.read(k)  # 调用 READ 操作
                    if value is None:
                        result = f"024 ERR {k} not found"
                    else:
                        result = f"021 OK ({k}, {value}) retrieved"

            elif command == 'GET':
                if len(parts) != 2:  # 确保 GET 命令格式正确
                    result = "024 ERR Invalid GET command format"
                else:
                    k = parts[1]  # 提取 key
                    value = tuple_space.get(k)  # 调用 GET 操作
                    if value is None:
                        result = f"024 ERR {k} not found"
                    else:
                        result = f"021 OK ({k}, {value}) removed"

            else:
                result = "024 ERR Unknown command"  # 未知命令

        client_socket.send(result.encode())  # 发送响应给客户端


def start_server(host, port):
    tuple_space = TupleSpace()  # 初始化 tuple_space
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



