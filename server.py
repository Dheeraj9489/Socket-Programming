import socket
import threading

# Global list for connected clients
clients = []
usernames = {}

# Function to handle communication with each client
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    username = client_socket.recv(1024).decode('utf-8')
    usernames[client_socket] = username
    print(f"[NEW USER] {username} has joined the chat.")
    print(f"Total clients: {threading.active_count() - 1}")

    broadcast(f"{username} has joined the chat!\n".encode('utf-8'), client_socket)

    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024)
            if message:
                # Broadcast the message to all other clients
                if message.decode('utf-8') != "/quit":
                    broadcast(f"{username}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
                    print(f"[{username}]: {message.decode('utf-8')}")
            else:
                # If no message, the client has disconnected
                remove_client(client_socket)
                break
        except:
            # Handle exceptions
            remove_client(client_socket)
            break

# Function to broadcast messages to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)


# Function to remove a client from the list and close the connection
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        username = usernames[client_socket]
        del usernames[client_socket]
        print(f"[DISCONNECT] {username} has left the chat.")
        broadcast(f"{username} has left the chat.\n".encode('utf-8'), None)
        client_socket.close()


def start_server(server_ip, server_port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))

    # Handle multiple clients simultaneously
    # <code here>
    server_socket.listen(5)

    print(f"[SERVER STARTED] Listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        
        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # Change as needed

    print("Specify a port number to listen on: ", end="")
    SERVER_PORT = int(input())  # Change as needed
    start_server(SERVER_IP, SERVER_PORT)
