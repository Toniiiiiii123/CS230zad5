import socket

HOST = '127.0.0.1'
PORT = 50007


def obradi_zahtev(zahtev):
    return "Server je obradio zahtev: " + zahtev


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server radi na {HOST}:{PORT}")

while True:
    client_socket, address = server_socket.accept()
    print(f"Povezan klijent: {address}")

    try:
        data = client_socket.recv(1024)

        if data:
            zahtev = data.decode()
            print(f"Primljen zahtev: {zahtev}")

            odgovor = obradi_zahtev(zahtev)
            client_socket.sendall(odgovor.encode())
    finally:
        client_socket.close()
