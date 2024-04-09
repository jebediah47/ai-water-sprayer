import socket
import time


def simulate_spray():
    start_time = time.time()
    while time.time() - start_time < 2.5:
        print("Spraying!")
        time.sleep(0.1)


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        if message == "spray":
            print("Received spray request.")
            simulate_spray()
        elif message == "terminate":
            print("Received termination request.")
            break

    client_socket.close()


def start_server():
    server_address = ('localhost', 12345)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen(5)

        print("Socket server started. Listening for connections...")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print("Connection from:", client_address)
                handle_client(client_socket)
        except KeyboardInterrupt:
            print("Server terminated by user.")


if __name__ == "__main__":
    start_server()
