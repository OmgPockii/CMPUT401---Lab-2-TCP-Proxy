#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(addr, conn):
    print("Connected by", addr)
    
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
    #setup 
    extern_host = 'www.google.com'
    port = 80

    #create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print ("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            #connect proxy_start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(extern_host)

                #connect proxy_end
                proxy_end.connect((remote_ip, port))

                #multiprocessing
                #accept connections and start a Process daemon for handling multiple connections
                conn, addr = proxy_start.accept()
                p = Process(target=handle_request, args=(addr,conn))
                p.daemon = True
                p.start()
                print("Started process ", p)
            
            conn.close()



if __name__ == "__main__":
    main()