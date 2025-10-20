import socket
import threading
import sys

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                print(msg)
            else:
                print("Server memutus koneksi.")
                break
        except:
            print("Terjadi kesalahan koneksi.")
            sock.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("127.0.0.1", 5555))
    except:
        print("Gagal terhubung ke server.")
        sys.exit()

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input("")
        if msg.lower() in ("exit", "keluar"):
            client.close()
            break
        try:
            client.send(msg.encode('utf-8'))
        except:
            print("Koneksi terputus.")
            break

if __name__ == "__main__":
    main()
