import socket
import sys
import os

# 读取请求文件
def read_requests_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"[!] 请求文件不存在: {file_path}")
        return []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    valid_requests = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) > 970:
            print(f"[!] 请求过长，跳过: {line[:50]}...")
            continue
        if line.startswith(("PUT", "READ", "GET")):
            valid_requests.append(line)
        else:
            print(f"[!] 非法请求格式: {line}")

    return valid_requests

# 向服务器发送请求
def send_request_to_server(request, server_address):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)
            s.sendall(request.encode())
            response = s.recv(1024).decode()
            print(f"Request: {request} → Response: {response}")
    except Exception as e:
        print(f"[!] 请求发送失败: {e}")

# 主函数
def main():
    if len(sys.argv) != 4:
        print("用法: python client.py <hostname> <port> <request_file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    server_address = (hostname, port)

    valid_requests = read_requests_from_file(file_path)

    for request in valid_requests:
        send_request_to_server(request, server_address)

if __name__ == "__main__":
    main()
