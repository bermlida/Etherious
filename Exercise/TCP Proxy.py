
import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("except in server_loop")
        sys.exit(0)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if (receive_first):
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if (len(local_buffer)):
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            break

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
def hexdump(src, length=8):
    N=0; result=''
    while src:
       s,src = src[:length],src[length:]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       s = s.translate(FILTER)
       result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
       N+=length
    return result

def receive_from(connection):
    buffer = ""
    connection.settimeout(2)

    try:
        while True:
            data = connection.recv(4096)

            if not data:
                break

            buffer += data
    except:
        pass
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

if len(sys.argv[1:]) != 5:
    sys.exit(0)

local_host = sys.argv[1]
local_port = len(sys.argv[2])

remote_host = sys.argv[3]
remote_port = len(sys.argv[4])

receive_first = sys.argv[5]

if "True" in receive_first:
    receive_first = True
else:
    receive_first = False

server_loop(local_host,local_port, remote_host, remote_port, receive_first)