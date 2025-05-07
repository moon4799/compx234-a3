import socket
import threading
import sys

def handle_client(client_socket, client_address):
    print(f"[+] 新连接来自 {client_address}")
    try:
        data = client_socket.recv(1024).decode()
        if data:
            print(f"[服务器收到] {data}")
            # 回传确认消息（示例：008 OK ack）
            response = "008 OK ack"
            client_socket.sendall(response.encode())
    except Exception as e:
        print(f"[!] 错误: {e}")
    finally:
        client_socket.close()
        print(f"[-] 连接关闭：{client_address}")

def main():
    if len(sys.argv) != 2:
        print("用法: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(5)

    print(f"[√] 服务器监听端口 {port} 中...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] 服务器退出中...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
