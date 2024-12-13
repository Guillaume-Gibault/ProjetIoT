# Imports
from machine import UART, I2C
import time

# Constantes pour l'UART
DELAY_TIMEOUT = 1000
BAUDRATE = 9600
UART_NUMBER = 2
RX_BUFF = 512
EOL = "\r\n"

# Seuil de distance (en mm)
DISTANCE_THRESHOLD = 500

# Configuration de l'UART pour LoRa
uart = UART(UART_NUMBER, baudrate=BAUDRATE, timeout=DELAY_TIMEOUT, rxbuf=RX_BUFF)

# Configuration de l'I2C pour le VL53L0X
i2c = I2C(1)

# Importation de la classe VL53L0X complète
from VL53L0X import VL53L0X

# Initialisation du capteur tof VL53L0X
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

# Programme principal
send_command("AT+RESET", expected_response="+RESET: OK")  # Reset LoRa
time.sleep(2)  # Pause pour laisser le temps au module de redémarrer
send_command("AT", expected_response="+AT: OK")  # Vérifier la communication
send_command("AT+VER", expected_response="+VER:")  # Obtenir la version du firmware
send_command("AT+MODE=TEST", expected_response="+MODE: TEST")  # Changer en mode P2P
print("Initialisation terminée.\n\n")

while True:
    try:
        distance = tof.read()
        print("Distance mesurée :", distance, "mm")
        if distance < DISTANCE_THRESHOLD:
            print("Porte ouverte.")
            send_command('AT+TEST=TXLRPKT, "1"', expected_response='+TEST: TXLRPKT "')
        else:
            print("Porte fermée.")
            send_command('AT+TEST=TXLRPKT, "0"', expected_response='+TEST: TXLRPKT "')
        time.sleep_ms(100)  # Pause entre les envois
    except KeyboardInterrupt:
        print("Arrêt du programme.")
        break
