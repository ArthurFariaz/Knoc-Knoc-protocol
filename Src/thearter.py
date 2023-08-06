import sys
import socket
import selectors
import types
import time


def main():
    sel = selectors.DefaultSelector()
    host, port = "127.0.0.1", 30000
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    lsock.bind((host, port))
    lsock.listen()
    seats = 3
    audience = 0 
    print(f"Listening on {(host, port)}")
    #lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
    try:
        while (True):
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    audience = accept_wrapper(key,sel,audience,seats)
                else:
                    audience = service_connection(key, mask,sel,audience)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

def accept_wrapper(key,sel,audience,seats):
    while(audience < seats):
        sock = key.fileobj
        conn, addr = sock.accept()  # Should be ready to read    
        print(f"Accepted connection from {addr}")
        #lsock.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"",state="waiting_for_quem")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
        conn.send(b"Teatro aberto ... bem vindo\n")
        conn.send(b"Toc Toc\n")
        audience += 1
        print(f"The number of the audience is {audience}")
        return audience
    time.sleep(0.01)
    return audience

def service_connection(key, mask, sel,audience):
    sock = key.fileobj
    data = key.data
    addr = data.addr[1]
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        msg = recv_data.decode('utf-8').strip().lower()
        if recv_data:
            if  msg == "quem eh?":
                if data.state == "waiting_for_quem":
                    print(f"Received: {msg}, Sending: hulk, from: {addr}")
                    data.state = "waiting_for_hulk"
                    data.outb += b"hulk\n"  
                else:
                    print(f"Received: {msg}, Sending: Unknown command, from: {addr}")
                    data.state = "waiting_for_quem"
                    data.outb += b"Unknown command\n" 
            elif msg == "hulk quem?":
                if  data.state == "waiting_for_hulk":
                    print(f"Received: {msg}, Sending: SMASH, from: {addr}")
                    data.state = "finish"
                    data.outb += b"SMASH\n"
                    data.outb+= b"Bye bye\n"
            elif data.state == "finish":
                print(f"Closing connection to {data.addr}")
                audience = audience - 1
                print(f"The number of the audience is {audience}")
                sel.unregister(sock)
                sock.close()
            else:
                print(f"Received: {msg}, Sending: Unknown command, from: {addr}")
                data.state = "waiting_for_quem"
                data.outb += b"Unknown command\n" 
        else:
            print(f"Closing connection to {data.addr}")
            audience = audience - 1
            print(f"The number of the audience is {audience}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

    return audience
main()
