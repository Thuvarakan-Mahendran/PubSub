
# ========================
# use command `python client.py <host> <port> <PUBLISHER/SUBSCRIBER>` to start the client
# ========================

import socket
import sys

if len(sys.argv) != 4:
    print("Usage: python client.py <host> <port> <PUBLISHER/SUBSCRIBER>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
MODE = sys.argv[3].strip().upper()

if MODE not in ["PUBLISHER", "SUBSCRIBER"]:
    print("Invalid mode. Use PUBLISHER or SUBSCRIBER")
    sys.exit(1)

def listen_msgs(client):
    while True:
        msg = client.recv(1024).decode("utf-8")
        if not msg:
            break
        print(f"msg published by publisher: {msg}")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(MODE.encode("utf-8"))    # Sending the mode to the server as it has to be registered on the server side
    if MODE == "SUBSCRIBER":
        try:
            listen_msgs(client)
        except KeyboardInterrupt:
            print("Interrupted by user")
        except ConnectionError as e:
            print(f"Connection error: {e}")
        finally:
            print("Connection closed")
            client.shutdown(socket.SHUT_RDWR)
            client.close()
    # Publisher will be default and also we checking whether the mode have to be one of PUBLISHER or SUBSCRIBER
    try:
        while True:
            msg = input()   #input() will always return a string, we need to convert according to the need. For example, age should be an integer
            client.sendall(msg.encode("utf-8"))
            if msg.lower() == "terminate":
                break
    except KeyboardInterrupt:
        print("Interrupted by user")
    except ConnectionError as e:
        print(f"Connection error: {e}")
    finally:
        print("Connection closed")
        client.shutdown(socket.SHUT_RDWR)
        client.close()

if __name__ == "__main__":
    start_client()
