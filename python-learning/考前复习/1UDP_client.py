import socket
ADDR=("127.0.0.1",9000)
c=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    msg=input(">>")
    c.sendto(msg.encode("UTF-8"),ADDR)
    data,addr=c.recvfrom(1024)
    print(data.decode("UTF-8"))

c.close()
