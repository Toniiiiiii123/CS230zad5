import socket

HOST = '127.0.0.1'
MIDDLEWARE_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, MIDDLEWARE_PORT))

zahtev = input("Unesite zahtev: ")

client_socket.sendall(zahtev.encode())

odgovor = client_socket.recv(1024).decode()

print("Odgovor:", odgovor)

client_socket.close()
