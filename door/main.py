from machine import UART, I2C
import ustruct
import time

# Constantes pour l'UART
DELAY_TIMEOUT = 1000
BAUDRATE = 9600
UART_NUMBER = 2
RX_BUFF = 512
EOL = "\r\n"

# Configuration de l'UART pour LoRa
uart = UART(UART_NUMBER, baudrate=BAUDRATE, timeout=DELAY_TIMEOUT, rxbuf=RX_BUFF)

# Configuration de l'I2C pour le VL53L0X
i2c = I2C(1)

# Importation de la classe VL53L0X complète
from VL53L0X import VL53L0X  # Assurez-vous que ce fichier est dans le bon répertoire

# Initialisation du capteur VL53L0X
tof = VL53L0X(i2c)

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

# Configuration du module LoRa
def config_lora():
    send_command("AT+MODE=TEST")
    send_command("AT+DR=SF12BW125")
    send_command("AT+FREQ=868125000")
    send_command("AT+POWER=22")

# Envoi des données via LoRa
def send_lora_message(data):
    hex_data = "{:04x}".format(data)  # Convertir la distance en hexadécimal
    send_command("AT+MSGHEX=" + hex_data, expected_response="Done")

# Programme principal
print("Configuration LoRa...")
config_lora()
print("Prêt à envoyer des messages.")

while True:
    try:
        distance = tof.read()  # Obtenez la distance en utilisant la méthode `read` de la classe complète
        print("Distance mesurée :", distance, "mm")
        send_lora_message(distance)  # Envoyer la distance via LoRa
        time.sleep_ms(100)  # Pause entre les envois
    except KeyboardInterrupt:
        print("Arrêt du programme.")
        break
