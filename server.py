
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

Subscribers = {}  # Dictionary to store subscribers by topic: {topic: [list of connections]}
Subscribers_lock = threading.Lock() # to avoid race conditions when adding/removing subscribers as we have multiple threads

def broadcast_message(topic, message):
    """Send message to all subscribers of a specific topic"""
    with Subscribers_lock:
        if topic in Subscribers:
            # Create formatted message with topic
            formatted_msg = f"{topic}|{message}"
            for sub in Subscribers[topic]:
                try:
                    sub.sendall(formatted_msg.encode("utf-8"))
                except Exception as e:
                    print(f"Error sending message to subscriber: {e}")

def handle_client(conn, addr):
    mode = None
    topic = None
    try:
        data = conn.recv(1024)
        if not data:
            return
        registration = data.decode("utf-8").strip().upper()
        # Parse MODE|TOPIC format
        if "|" in registration:
            mode, topic = registration.split("|", 1)
            topic = topic.strip()
        else:
            mode = registration
        
        if mode not in ["PUBLISHER", "SUBSCRIBER"]:
            return
        
        print(f"mode: {mode}, topic: {topic}")
        
        if mode == "SUBSCRIBER":
            with Subscribers_lock:
                # Add subscriber to the topic list
                if topic not in Subscribers:
                    Subscribers[topic] = []
                Subscribers[topic].append(conn)
                print(f"Subscriber added to topic '{topic}'. Total subscribers for '{topic}': {len(Subscribers[topic])}")
        
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
                if mode == "PUBLISHER":
                    broadcast_message(topic, msg)
    except ConnectionError as e:
        print(f"connection error: {e}")
    finally:
        # Remove subscriber from the list when disconnecting
        if mode == "SUBSCRIBER" and topic:
            with Subscribers_lock:
                if topic in Subscribers and conn in Subscribers[topic]:
                    Subscribers[topic].remove(conn)
                    print(f"Subscriber removed from topic '{topic}'. Remaining subscribers: {len(Subscribers[topic]) if topic in Subscribers else 0}")
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
