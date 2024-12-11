from machine import UART, Pin
import ubinascii
import time

# Définition des broches
A0=Pin.cpu.C0
A1=Pin.cpu.C1
A2=Pin.cpu.A1
A3=Pin.cpu.A0
A4=Pin.cpu.A4
A5=Pin.cpu.A5
D0=Pin.cpu.A3
D1=Pin.cpu.A2
D2=Pin.cpu.C6
D3=Pin.cpu.A10
D4=Pin.cpu.C10
D5=Pin.cpu.A15
D6=Pin.cpu.A8
D7=Pin.cpu.C13
D8=Pin.cpu.C12
D9=Pin.cpu.A9
D10=Pin.cpu.A4
D11=Pin.cpu.A7
D12=Pin.cpu.A6
D13=Pin.cpu.A5
D14=Pin.cpu.B9
D15=Pin.cpu.B8

# Constantes pour l'UART
DELAY_TIMEOUT = 1000
BAUDRATE = 9600
UART_NUMBER = 2
RX_BUFF = 512
EOL = "\r\n"

# Seuil de distance (en mm)
DISTANCE_THRESHOLD = 500

# Pin de sortie pour signalisation
output_pin = Pin(D0, Pin.OUT)
output_pin.value(0)

# Configuration de l'UART pour LoRa
uart = UART(UART_NUMBER, baudrate=BAUDRATE, timeout=DELAY_TIMEOUT, rxbuf=RX_BUFF)

# Fonction pour envoyer des commandes AT à LoRa
def send_command(cmd, expected_response="OK", timeout=2000):
    print("Envoi :", cmd)
    uart.write(cmd + EOL)
    start_time = time.ticks_ms()
    response = b""
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        if uart.any():
            response += uart.read()
        if expected_response.encode() in response:
            print("Réponse :", response.decode("utf-8"))
            return True
    print("Erreur ou timeout :", response.decode("utf-8") if response else "Aucune réponse")
    return False

# Fonction pour lire les messages reçus via UART
def receive_message():
    if uart.any():
        data = uart.read()
        try:
            msg = data.decode("utf-8").strip()
            print("Message reçu :", msg)
            return msg
        except UnicodeDecodeError:
            print("Erreur de décodage du message reçu.")
            return None
    return None

# Boucle principale
send_command("AT+RESET")
time.sleep(2)
send_command("AT")
send_command("AT+VER")
send_command("AT+MODE=TEST")
print("initialisation terminee")

send_command("AT+TEST=RXLRPKT")

while True:
    try:
        message = receive_message()
        if "RX" in message:
            try:
                print("Message brut reçu :", message)
                splitted_message = message.split('"')
                distance = int(ubinascii.unhexlify(splitted_message[1]))
                print("Distance reçue :", distance, "mm")

                if distance > DISTANCE_THRESHOLD:  # Seuil de distance
                    output_pin.value(1)
                    print("Seuil dépassé : activation.")
                else:
                    output_pin.value(0)
                    print("Seuil non dépassé : désactivation.")
            except (ValueError, TypeError) as e:
                print("Erreur dans le traitement :", e)
    except KeyboardInterrupt:
        print("Arrêt du programme.")
        break
