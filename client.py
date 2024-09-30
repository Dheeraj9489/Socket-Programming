import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                # If the server connection is closed
                print("Connection closed by the server.")
                client_socket.close()
                break
        except:
            # If an error occurs, close the connection
            # print("An error occurred.")
            client_socket.close()
            break
    

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        # <code here>
        # <print all communications>
        if message == "/quit":
            client_socket.send("/quit".encode('utf-8'))
            print("You have exited the chat.")
            client_socket.close()
            break
        else:
            client_socket.send(message.encode('utf-8'))

def start_client(server_ip, server_port):
    # Create a TCP socket: client_socket
    # <code here>
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    client_socket.send(username.encode('utf-8'))
    # Start a thread to listen for messages from the server
    # <code here>
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_messages(client_socket)


if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"  # Change as needed
    SERVER_PORT = 8080  # Change as needed

    print("Enter your username: ", end="")
    username = input()
    
    start_client(SERVER_IP, SERVER_PORT)
