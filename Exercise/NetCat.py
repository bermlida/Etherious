
import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response)

            buffer = input("")
            buffer += "\n"

            client.send(buffer)

    except:
        print("[*] Exception! Exiting.")

        client.close()

def server_loop():
    global target

    if not len(target):
        target = '127.0.0.1'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target = client_socket, args=(client_socket,))

        client_thread.start()


def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "command execute error\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ''

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()
        except:
            client_socket.send('Failed to save file to {} \r\n' . format(upload_destination))

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send("<BHP:#")

            cmd_buffer = ''

            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer)

            client_socket.send(response)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hle:t:p:cu",
            ["help", "listen", "execute", "target", "port", "command", "upload"]
        )
    except getopt.GetoptError as err:
        print(str(err))

    for option, argument in opts:
        if option in ("-l", "--listen"):
            listen = True
        elif option in ("-e", "--execute"):
            execute = argument
        elif option in ("-c", "--command"):
            command = True
        elif option in ("-u", "--upload"):
            upload_destination = argument
        elif option in ("-t", "--target"):
            target = argument
        elif option in ("-p", "--port"):
            port = int(argument)

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()

        client_sender(buffer)

    if listen:
        server_loop()

main()

