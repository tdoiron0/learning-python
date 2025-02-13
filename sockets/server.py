import socket
import threading

THREADS_STOP = threading.Event()

host = '127.0.0.1'  # Default server IP address **Might not need** 
port = 60000          # Default port used by the server
clients: list[tuple[str, socket.socket]] = []
data_buffer: list[str] = []

def setup() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print(f"Server started on port {port}. Accepting connections.")
    return s

def handle_client(client_socket: socket.socket):
    data = client_socket.recv(1024).decode('utf-8')
    print(f"New client: {data}")
    client_socket.sendall("Hello from server.".encode('utf-8'))
    clients.append((data, client_socket)) 

def client_listener(server_socket: socket.socket): 
    threads: list[threading.Thread] = []
    try:
        while not THREADS_STOP.is_set():
            client_socket, client_addr = server_socket.accept()
            threads.append(threading.Thread(target=handle_client, args=(client_socket,)))
            threads[-1].start()
    except OSError as e:
        print(f"Warning: {e}")

def data_listener():
    while not THREADS_STOP.is_set():
        for name, socket in clients:
            data = socket.recv(1024)
            if not data:
                print(f"{name} has disconnected")
                socket.close()
                clients.remove((name, socket))
            else:
                print(f"{name}: {data.decode('utf-8')}")

def main():
    server_socket = setup()
    client_listener_thread = threading.Thread(target=client_listener, args=(server_socket,))
    data_listener_thread = threading.Thread(target=data_listener)
    client_listener_thread.start()
    data_listener_thread.start()

    try:
        while True:
            None
    except KeyboardInterrupt:
        print("Stopping main for keyboard interrupt")
    finally:
        THREADS_STOP.set()
        server_socket.close()

main()