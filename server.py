from threading import Thread
import socket
        
threads = []

def client_listener(conn, addr):
    """
    Listens to a specific client

    Args:
        conn (socket.socket object): socket to listen to
        addr (tuple): Where the connection is coming from
    """
    print(f"connection from {addr}")
    while 1:
        data = conn.recv(4096).decode("utf-8")
        print(data)

def main():
    """
    The main function
    """
    while 1:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 5000))
            sock.listen()
            conn, addr = sock.accept()
            thread = Thread(target=client_listener, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()