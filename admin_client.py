import socket

HOST = '127.0.0.1'
ADMIN_PORT = 12346

admin_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
admin_socket.connect((HOST, ADMIN_PORT))

print("Administratorski klijent je povezan sa middleware-om.")
print("Cekanje OOB logova...")

while True:
    try:
        regularni_deo = admin_socket.recv(4096)

        if not regularni_deo:
            break

        oob_deo = admin_socket.recv(1, socket.MSG_OOB)

        log_poruka = (regularni_deo + oob_deo).decode()

        print("\n--- OOB LOG ---")
        print(log_poruka)
        print("---------------")

        admin_socket.sendall(b"ACK")

    except Exception as e:
        print(f"Greska: {e}")
        break

admin_socket.close()
