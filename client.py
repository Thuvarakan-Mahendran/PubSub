import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python client.py <host> <port>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
try:
    while True:
        msg = input()   #input() will always return a string, we need to convert according to the need. For example, age should be an integer
        client.sendall(msg.encode())
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
