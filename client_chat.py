import socket, select, sys, errno
HEADER_LENGTH = 10
IP = socket.gethostname()#"192.168.31.169"
PORT = 12345
my_username = input("Username: ")
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
    username = my_username.encode("utf-8")
    username_header=f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(username_header+username)
    while True:
        # choose the one that is read to read
        read_ready, _, _ = select.select([sys.stdin, client_socket], [], [])
        for reader in read_ready:
            if reader is sys.stdin:
                print(f"{my_username} > ")
                message = sys.stdin.readline()
                if message:
                    message = message.encode("utf-8")
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                    client_socket.send(message_header+message)
            else:
                try:
                    while True:
                        username_header = client_socket.recv(HEADER_LENGTH)
                        if not len(username_header):
                            print("close")
                            sys.exit()
                        username_length = int(username_header.decode("utf-8").strip())
                        username = client_socket.recv(username_length).decode("utf-8")
                        message_header = client_socket.recv(HEADER_LENGTH)
                        message_length = int(message_header.decode("utf-8").strip())
                        message = client_socket.recv(message_length).decode("utf-8")
                        print(f"{username} > {message}")
                except IOError as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('reading error', str(e))
                        sys.exit()
                    continue
                except Exception as e:
                    print("error", str(e))
except KeyboardInterrupt:
    client_socket.close()
    sys.exit()