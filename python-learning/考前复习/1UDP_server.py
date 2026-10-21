import socket
ADDR=("127.0.0.1",9000)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(ADDR)
while True:
    data,addr=s.recvfrom(1024)
    msg=data.decode("UTF-8")
    res=msg.upper()
    print(res)
    s.sendto(res.encode("UTF-8"),addr)

s.close()