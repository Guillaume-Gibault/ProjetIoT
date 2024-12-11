from machine import UART, Pin
import time

# Constantes pour l'UART
DELAY_TIMEOUT = 1000
BAUDRATE = 9600
UART_NUMBER = 2
RX_BUFF = 512

# Seuil de distance (en mm)
DISTANCE_THRESHOLD = 500

# Pin de sortie pour signalisation
output_pin = Pin(2, Pin.OUT)
output_pin.value(0)

# Configuration de l'UART pour LoRa
uart = UART(UART_NUMBER, baudrate=BAUDRATE, timeout=DELAY_TIMEOUT, rxbuf=RX_BUFF)


# Fonction pour lire les messages reçus via UART
def receive_message():
    if uart.any():
        data = uart.read()
        try:
            # Analyse du message
            msg = data.decode("utf-8").strip()
            print("Message reçu :", msg)
            return msg
        except UnicodeDecodeError:
            print("Erreur de décodage du message reçu.")
            return None
    return None


# Boucle principale
print("Station réceptrice LoRa prête.")

while True:
    try:
        message = receive_message()
        if message:
            if "MSGHEX=" in message:
                try:
                    hex_value = message.split("=")[1]  # Obtenir la valeur hexadécimale
                    distance = int(hex_value, 16)  # Convertir en entier
                    print("Distance reçue :", distance, "mm")

                    # Vérifier si la distance dépasse le seuil
                    if distance > DISTANCE_THRESHOLD:
                        output_pin.value(1)  # Activer le pin
                        print("Seuil dépassé : pin activé.")
                    else:
                        output_pin.value(0)  # Désactiver le pin
                        print("Seuil non dépassé : pin désactivé.")
                except (IndexError, ValueError) as e:
                    print("Erreur dans le traitement du message :", e)
    except KeyboardInterrupt:
        print("Arrêt de la station réceptrice.")
        break
