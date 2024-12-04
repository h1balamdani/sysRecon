import socket,sys
from getParameter import update_parameters


def connecter(): #Etablir la Connextion de la cible avec l'interrogateur

    try:
        host,port = update_parameters()
        root_socket.connect((host, port))
        print("Connection established successfully.")
    except socket.gaierror as e:
        print(f"Address-related error connecting to server: {e}")
        fermer()
        sys.exit(0)
    except socket.error as e:
        print(f"General socket error: {e}")
        fermer()
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred while connecting: {e}")
        fermer()
        sys.exit(0)

def fermer(): #fermer la connexion
    try:
        root_socket.close()
        print("Socket closed successfully.")
    except socket.error as e:
        print(f"Error closing the socket: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while closing the socket: {e}")

def envoyer(message): #envoyer les resultats d'interrogation
    try:
        if root_socket.fileno() == -1:
            raise socket.error("Socket is not connected.")
        root_socket.send(message.encode())
        print("Message sent successfully.")
    except socket.error as e:
        print(f"Socket error while sending message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending the message: {e}")

# creer la connection socket
root_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
