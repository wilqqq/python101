import socket, select, sys, errno, threading
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
    def msg_write(name):
        while True:
            try:
                print(f"{my_username} > ")
                message = sys.stdin.readline()
                if message:
                    message = message.encode("utf-8")
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                    client_socket.send(message_header+message)
            except KeyboardInterrupt:
                sys.exit()
    write_thread = threading.Thread(target=msg_write, args=(1,), daemon=True)
    def msg_read(name):
        while True:  
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
    read_thread = threading.Thread(target=msg_read, args=(1,), daemon=True)
    write_thread.start()
    read_thread.start()
    write_thread.join() # wait to end
except KeyboardInterrupt:
    client_socket.close()
    sys.exit()