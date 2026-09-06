import socket
import sys

if(len(sys.argv) != 2):
    print("Usage: python server.py <port>")
    sys.exit(1)

HOST = "0.0.0.0"    # accept connections from any IP address
PORT = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a TCP socket where AF_INET is IPv4 and SOCK_STREAM is TCP
server.bind((HOST, PORT))
server.listen()
try:
    while True:
        conn, addr = server.accept()  # accept a new connection from a client
        with conn:
            print(f"connected by {addr}")
            while True:
                data = conn.recv(1024)  # receive data from the client with a limit of 1024 bytes
                if not data:
                    break
                msg = data.decode("utf-8")  # decode the received data as UTF-8
                if msg.strip().lower() == "terminate":  # strip to remove whitespaces, tabs, and convert to lowercase for comparison
                    print("terminate command received. closing connection...")
                    conn.close()
                    break
                print(f"received: {msg}")
except KeyboardInterrupt:
    print("Interrupted by user")
