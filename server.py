
# ========================
# use command `python server.py <port>` to start the server
# ========================

import socket
import sys
import threading

if(len(sys.argv) != 2):
    print("Usage: python server.py <port>")
    sys.exit(1)

HOST = "0.0.0.0"    # accept connections from any IP address
PORT = int(sys.argv[1])

Subscribers = []
Subscribers_lock = threading.Lock() # to avoid race conditions when adding/removing subscribers as we have multiple threads

def broadcast_message(message):
    for sub in Subscribers:
        sub.sendall(message.encode("utf-8"))

def handle_client(conn, addr):
    mode = None
    try:
        data = conn.recv(1024)
        if not data:
            return
        mode = data.decode("utf-8").strip().upper()
        if mode not in ["PUBLISHER", "SUBSCRIBER"]:
            return
        print(f"mode: {mode}")
        if mode == "SUBSCRIBER":
            with Subscribers_lock:      # acquire the lock to avoid race conditions when adding/removing subscribers
                Subscribers.append(conn)
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
                broadcast_message(msg)
    except ConnectionError as e:
        print(f"connection error: {e}")
    finally:
        print("closing connection...")
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a TCP socket where AF_INET is IPv4 and SOCK_STREAM is TCP
    server.bind((HOST, PORT))
    server.listen()
    try:
        while True:
            conn, addr = server.accept()  # accept a new connection from a client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        print("shutting down server...")
        server.shutdown(socket.SHUT_RDWR)
        server.close()


if __name__ == "__main__":
    start_server();
