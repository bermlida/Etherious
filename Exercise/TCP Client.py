
import socket

target_host = "0.0.0.0"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

send_data = "GET / HTTP/1.1\r\nHost: 0.0.0.0\r\n\r\n"
client.send(send_data.encode(encoding='utf_8'))

response = client.recv(4096)

print(response.decode(encoding='utf_8'))