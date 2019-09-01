import socket as s
import sys
soc = s.socket(s.AF_INET, s.SOCK_STREAM)
soc.bind((s.gethostname(), 1234))
soc.listen(5)
try:
    while True:
        cs, addr=soc.accept()
        cs.send(bytes("Welkommen {}".format(addr),"utf-8"))
except KeyboardInterrupt:
    sys.exit()
