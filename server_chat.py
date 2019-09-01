import socket, select, sys
HEADER_LENGTH = 10
IP = socket.gethostname()#"192.168.31.169"
PORT = 12345
try:
    serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allow reconnect
    serv_soc.bind((IP, PORT))
    serv_soc.listen()
    soc_list = [serv_soc]
    cli = {}
    def receive_message(cli_soc):
        try:
            message_header = cli_soc.recv(HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode("utf-8").strip())
            return {"header": message_header, "data": cli_soc.recv(message_length)} #dictionary
        except:
            return False
    while True:
        read_sockets, _, exception_sockets=select.select(soc_list, [], soc_list)
        for notified_socket in read_sockets:
            if notified_socket == serv_soc:
                client_socket, client_addres = serv_soc.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                soc_list.append(client_socket)
                cli[client_socket]=user
                print("Accepted new from {}:{} username:{}".format(client_addres[0] ,client_addres[1] ,user['data'].decode("utf-8")))
            else:
                message = receive_message(notified_socket)
                if message is False:
                    print("Closed {}".format(cli[notified_socket]['data'].decode("utf-8")))
                    soc_list.remove(notified_socket)
                    del cli[notified_socket]
                    continue
                user = cli[notified_socket]
                print("MSG {} >> {}".format(user['data'].decode("utf-8"), message['data'].decode("utf-8")))
                for cli_soc in cli:
                    if cli_soc != notified_socket:
                        cli_soc.send(user['header']+user['data']+message['header']+message['data'])
        for notified_socket in exception_sockets:
            soc_list.remove(notified_socket)
            del cli[notified_socket]
except KeyboardInterrupt:
    serv_soc.close()
    pass