
import socket

target_host = "127.0.0.1"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto('AAAAAA'.encode(encoding='utf-8'), (target_host, target_port))

print(client.recvfrom(1024))