import tkinter as tk
import socket,json

# l'aquise  d'adresse up  
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address 

# trouver le premier port dynamique ferme
def find_first_available_port(start_port=49152, end_port=65535):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                
                s.bind(("localhost", port))
                return port
            except OSError:
                
                continue
    return None

# creer le socket et se connecter et mettre a l'ecoute
def connecter(port):
    try:
        
        global root_socket
        root_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        host = get_ip_address()
        print(f"Server's IP address is: {host}")
        
        root_socket.bind((host, port))
        
        root_socket.listen(1)
        print(f"Server listening on {host}:{port}...")
        
        global conn
        conn, address = root_socket.accept()
        print(f"Connection from {address}")
    except socket.error as err:
        print(f"Socket error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        
        if 'root_socket' in globals():
            root_socket.close()
            print("Socket closed.")

# arreter la connextion
def fermer():

    
    global conn
    conn.close()
    print("Connection closed")

# recevoirle message
def recevoir():

    global conn

    
    data = conn.recv(1024).decode()  
    dict = json.loads(data)
    return dict