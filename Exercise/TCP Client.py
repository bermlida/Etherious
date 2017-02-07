
import socket

target_host = "www.google.com"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

send_data = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
client.send(send_data.encode(encoding='utf_8'))

response = client.recv(4096)

print(response.decode(encoding='utf_8'))