import socket
import threading

host = '127.0.0.1'  # Default server IP address **Might not need** 
port = 60000        # Default port used by the server
username = "user1"

def setup() -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def main():
    client_socket = setup()
    client_socket.sendall(f"{username}".encode('utf-8'))
    data = None
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"{data}")

    while True:
        msg = input("Enter your message: ")
        if msg == "Quit":
            break
        client_socket.sendall(msg.encode('utf-8'))

    client_socket.close()

main()