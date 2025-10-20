import socket
import threading
import datetime

# Menyimpan semua client yang terhubung: {socket: username}
connected_clients = {}

def broadcast(message, sender_socket=None):
    for client_sock in connected_clients.keys():
        if client_sock != sender_socket:
            try:
                client_sock.send(message.encode('utf-8'))
            except:
                client_sock.close()
                del connected_clients[client_sock]

def handle_client(client_socket, address):
    try:
        client_socket.send("Masukkan username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        connected_clients[client_socket] = username

        join_msg = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {username} bergabung ke chat!"
        print(join_msg)
        broadcast(join_msg, client_socket)

        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break

            # Pesan pribadi
            if msg.startswith("@"):
                try:
                    target_name, private_msg = msg.split(" ", 1)
                    target_name = target_name[1:]
                    for sock, user in connected_clients.items():
                        if user == target_name:
                            waktu = datetime.datetime.now().strftime("%H:%M")
                            sock.send(f"[PM {waktu}] {username}: {private_msg}".encode('utf-8'))
                            break
                except ValueError:
                    client_socket.send("Format salah! Gunakan: @username pesan".encode('utf-8'))
            else:
                waktu = datetime.datetime.now().strftime("%H:%M")
                formatted_msg = f"[{waktu}] {username}: {msg}"
                broadcast(formatted_msg, client_socket)

    except Exception as e:
        print(f"Error dengan {address}: {e}")
    finally:
        if client_socket in connected_clients:
            left_user = connected_clients[client_socket]
            del connected_clients[client_socket]
            broadcast(f"{left_user} keluar dari chat.")
            client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5555))
    server_socket.listen(10)
    print("Server berjalan di port 5555...")

    while True:
        client_sock, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()

if __name__ == "__main__":
    main()
