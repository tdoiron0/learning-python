import socket
import threading

THREADS_STOP = threading.Event()

host = '127.0.0.1'  # Default server IP address **Might not need** 
port = 60000        # Default port used by the server
username = "user1"

def setup() -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(f"{username}".encode('utf-8'))
    data = None
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"{data}")
    return client_socket

def data_listener(client_socket: socket.socket):
    threads: list[threading.Thread] = []
    while not THREADS_STOP.is_set():
        data = client_socket.recv(1024)
        if data != None:
            print(f"Server has disconnected")
            client_socket.close()
        else:
            threads.append(threading.Thread(target=handle_data, args=(data,)))
            threads[-1].start()

def handle_data(data: str):
    data_parsed = data.split(",")
    if data_parsed[0] == "MESSAGE":
        handle_message(data_parsed[1], data_parsed[2])

def handle_message(name: str, msg: str): 
    print(f"{name}: {msg}")

def main():
    client_socket = setup()
    data_listener_thread = threading.Thread(target=data_listener, args=(client_socket,))
    data_listener_thread.start()

    try:
        while True:
            msg = input("Enter your message: ")
            if msg == "Quit":
                break
            client_socket.sendall(msg.encode('utf-8'))
    except KeyboardInterrupt:
        print("Stopping main for keyboard interrupt")
    finally:
        try:
            client_socket.close()
        except Exception as e:
            print(f"Exception: {e}")
        THREADS_STOP.set()
        data_listener_thread.join()

main()