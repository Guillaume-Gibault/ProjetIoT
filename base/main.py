# Imports
from machine import UART, Pin
import pyb
import time
import re

# D6 génère une PWM avec TIM1, CH1 pour le buzzer/speaker
d6 = pyb.Pin('D6', pyb.Pin.OUT_PP)
tim1 = pyb.Timer(1, freq=262)
pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)

# Constantes pour l'UART
DELAY_TIMEOUT = 1000
BAUDRATE = 9600
UART_NUMBER = 2
RX_BUFF = 512
EOL = "\r\n"

# Pin de sortie pour signalisation
output_pin = Pin('A5', Pin.OUT)
output_pin.value(0)

# Pin d'entrée pour la validité du code de désactivation
input_pin_valid_code = Pin('A4', Pin.IN)

# Pin d'entrée pour la non-validité du code de désactivation
input_pin_invalid_code = Pin('A3', Pin.IN)

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
        msg = uart.read()
        try:
            msg = msg.decode("utf-8").strip()
            print("Message reçu :", msg)
            return msg
        except UnicodeDecodeError:
            print("Erreur de décodage du message reçu.")
            return None
    return None

# Programme principal
send_command("AT+RESET", expected_response="+RESET: OK")  # Reset LoRa
time.sleep(2)  # Pause pour laisser le temps au module de redémarrer
send_command("AT", expected_response="+AT: OK")  # Vérifier la communication
send_command("AT+VER", expected_response="+VER:")  # Obtenir la version du firmware
send_command("AT+MODE=TEST", expected_response="+MODE: TEST")  # Changer en mode P2P
print("Initialisation terminée.\n\n")
send_command("AT+TEST=RXLRPKT", expected_response="")  # Activer la réception continue
triggered = False  # Initialisation
pwm.pulse_width_percent(0)  # Initialisation
output_pin.value(0)  # Initialisation
while True:
    try:
        if not triggered:  # Handler pour la réception de messages
            message = receive_message()
            if message and "RX" in message:  # Handler pour les messages reçus
                try:
                    match = re.search(r'RX\s+"([0-9A-Fa-f]+)"', message)
                    if match:
                        data = match.group(1)
                        activation = bool(int(data))
                        if activation:
                            pwm.pulse_width_percent(15)
                            output_pin.value(1)
                            triggered = True
                            print("Porte ouverte. Activation...", end="\n\n")
                        else:
                            pwm.pulse_width_percent(0)
                            output_pin.value(0)
                            print("Porte fermée.", end="\n\n")
                    else:
                        print("Données non valides dans le message.")
                except (ValueError, TypeError) as e:
                    print("Erreur dans le traitement :", e)
        else:  # Handler pour la désactivation de l'alarme
            if input_pin_valid_code.value() == 1 and input_pin_invalid_code.value() == 0:  # Handler pour la désactivation de l'alarme
                pwm.pulse_width_percent(0)
                output_pin.value(0)
                triggered = False
                print("Bon code. Désactivation...", end="\n\n")
            elif input_pin_invalid_code.value() == 1 and input_pin_valid_code.value() == 0:  # Handler pour la non-désactivation de l'alarme
                pwm.pulse_width_percent(15)
                output_pin.value(1)
                # Placeholder pour l'envoi d'un message d'alerte
                print("Mauvais code. Continuation de l'alarme...", end="\n\n")
    except KeyboardInterrupt:
        print("Arrêt du programme.")
        pwm.pulse_width_percent(0)
        tim1.deinit()
        output_pin.value(0)
        send_command("AT+RESET", expected_response="+RESET: OK")  # Reset LoRa
        time.sleep(2)  # Pause pour laisser le temps au module de redémarrer
        break
