import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("用法: python client.py <hostname> <port> <request_file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]  # 这个阶段暂不使用

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((hostname, port))

            # 发送测试消息，例如：007 R test
            message = "PUT key1 value1"
            client_socket.sendall(message.encode())
            message = "PUT key2 value2"
            client_socket.sendall(message.encode())

            # 接收服务器响应
            response = client_socket.recv(1024).decode()
            print(f"[客户端收到] {response}")

            message = "READ key1"
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"[客户端收到] {response}")

    except Exception as e:
        print(f"[!] 连接失败：{e}")

if __name__ == "__main__":
    main()
