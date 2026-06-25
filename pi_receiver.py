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
            print(f"\n[Surface]: {data.decode('utf-8').strip()}")
    except Exception as e:
        sys.exit()

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