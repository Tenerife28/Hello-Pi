import serial
import threading
import sys

port_bluetooth = 'COM3'
baud_rate = 115200

def asculta_mesaje(serial_conn):
    try:
        while True:
            data = serial_conn.readline()
            if data:
                print(f"\n[Pi4B]: {data.decode('utf-8').strip()}")
    except Exception as e:
        sys.exit()

try:
    s = serial.Serial(port_bluetooth, baud_rate)
    print("Conectat la Pi!")

    thread_ascultare = threading.Thread(target=asculta_mesaje, args=(s,), daemon=True)
    thread_ascultare.start()

    while True:
        mesaj = input()
        if mesaj.lower() == 'exit':
            break
        s.write((mesaj + '\n').encode('utf-8'))

except KeyboardInterrupt:
    pass
finally:
    if 's' in locals() and s.is_open:
        s.close()