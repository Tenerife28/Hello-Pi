import socket
import threading
import sys

def asculta_mesaje(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("\n[Client deconectat]")
                break
            # Parametrul errors='ignore' salveaza thread-ul de la crash
            print(f"\n[Surface]: {data.decode('utf-8', errors='ignore').strip()}")
    except Exception as e:
        # Daca apare o eroare, vrem sa o vedem pe ecran, nu sa inchidem mut!
        print(f"\n[Eroare thread citire]: {e}")

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((socket.BDADDR_ANY, 1))
s.listen(1)

print("Astept conexiune...")
client, addr = s.accept()
print("Conectat!")

thread_ascultare = threading.Thread(target=asculta_mesaje, args=(client,), daemon=True)
thread_ascultare.start()

try:
    while True:
        mesaj = input()
        if mesaj.lower() == 'exit':
            break
        client.sendall((mesaj + '\n').encode('utf-8'))
except KeyboardInterrupt:
    pass
finally:
    client.close()
    s.close()