import socket
import threading
import functools
import logging
from datetime import datetime

HOST = '127.0.0.1'

MIDDLEWARE_PORT = 12345
SERVER_PORT = 50007
ADMIN_PORT = 12346

admin_socket = None

logging.basicConfig(level=logging.INFO)


def prihvati_administratora():
    global admin_socket

    admin_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    admin_server.bind((HOST, ADMIN_PORT))
    admin_server.listen(1)

    print(f"Middleware ceka administratorskog klijenta na {HOST}:{ADMIN_PORT}")

    admin_socket, address = admin_server.accept()
    print(f"Administratorski klijent povezan: {address}")


def posalji_oob_log(log_poruka):
    global admin_socket

    if admin_socket is None:
        print("Administratorski klijent nije povezan.")
        return

    try:
        admin_socket.sendall(log_poruka.encode(), socket.MSG_OOB)

        # Administrator vraca potvrdu da je log primljen.
        admin_socket.recv(1024)
    except Exception as e:
        print(f"Greska pri slanju OOB loga: {e}")


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        vreme_ulaza = datetime.now()

        ko = args[0] if len(args) > 0 else "nepoznato"
        sta = args[1] if len(args) > 1 else "nepoznato"

        ulaz_log = (
            f"ULAZ | funkcija: {func.__name__} | "
            f"KO: {ko} | KAD: {vreme_ulaza} | STA: {sta} | "
            f"args: {args} | kwargs: {kwargs}"
        )

        logging.info(ulaz_log)

        rezultat = func(*args, **kwargs)

        vreme_izlaza = datetime.now()

        izlaz_log = (
            f"IZLAZ | funkcija: {func.__name__} | "
            f"KAD: {vreme_izlaza} | "
            f"args: {args} | kwargs: {kwargs} | "
            f"povratna vrednost: {rezultat}"
        )

        logging.info(izlaz_log)

        kompletan_log = ulaz_log + "\n" + izlaz_log

        oob_thread = threading.Thread(
            target=posalji_oob_log,
            args=(kompletan_log,)
        )
        oob_thread.start()

        return rezultat

    return wrapper


@log_execution
def prosledi_serveru(klijent_adresa, zahtev):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((HOST, SERVER_PORT))

    server_socket.sendall(zahtev.encode())

    odgovor = server_socket.recv(1024).decode()

    server_socket.close()

    return odgovor


admin_thread = threading.Thread(target=prihvati_administratora)
admin_thread.start()

middleware_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
middleware_socket.bind((HOST, MIDDLEWARE_PORT))
middleware_socket.listen(5)

print(f"Middleware radi na {HOST}:{MIDDLEWARE_PORT}")

while True:
    client_socket, address = middleware_socket.accept()
    print(f"Obican klijent povezan: {address}")

    try:
        data = client_socket.recv(1024)

        if data:
            zahtev = data.decode()
            print(f"Middleware je primio zahtev: {zahtev}")

            odgovor = prosledi_serveru(address, zahtev)

            client_socket.sendall(odgovor.encode())
    finally:
        client_socket.close()
