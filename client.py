import socket as s
soc = s.socket(s.AF_INET, s.SOCK_STREAM)
soc.connect((s.gethostname(), 1234))
msg = soc.recv(1023)
print(msg)