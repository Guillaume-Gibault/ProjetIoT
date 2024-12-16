# Imports
from machine import UART, Pin
import pyb
import time
import re
import bluetooth
from ble_advertising import advertising_payload
from binascii import hexlify

# Définition des broches
A0 = Pin.cpu.C0
A1 = Pin.cpu.C1
A2 = Pin.cpu.A1
A3 = Pin.cpu.A0
A4 = Pin.cpu.A4
A5 = Pin.cpu.A5
D0 = Pin.cpu.A3
D1 = Pin.cpu.A2
D2 = Pin.cpu.C6
D3 = Pin.cpu.A10
D4 = Pin.cpu.C10
D5 = Pin.cpu.A15
D6 = Pin.cpu.A8
D7 = Pin.cpu.C13
D8 = Pin.cpu.C12
D9 = Pin.cpu.A9
D10 = Pin.cpu.A4
D11 = Pin.cpu.A7
D12 = Pin.cpu.A6
D13 = Pin.cpu.A5
D14 = Pin.cpu.B9
D15 = Pin.cpu.B8

# D6 génère une PWM avec TIM1, CH1 pour le buzzer/speaker
d6 = pyb.Pin('D6', pyb.Pin.OUT_PP)
tim1 = pyb.Timer(1, freq=262)
pwm = tim1.channel(1, pyb.Timer.PWM, pin=d6)
pwm.pulse_width_percent(0)

# Constantes pour l'UART
DELAY_TIMEOUT = 1000
BAUDRATE = 9600
UART_NUMBER = 2
RX_BUFF = 512
EOL = "\r\n"

# Constantes pour construire les services BLE
_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_INDICATE_DONE = 20
_FLAG_READ = 0x0002
_FLAG_NOTIFY = 0x0010
_FLAG_INDICATE = 0x0020

# Pin de sortie pour signalisation
output_pin = Pin(D0, Pin.OUT)
output_pin.value(0)

# Pin d'entrée pour la validité du code de désactivation
input_pin_valid_code = Pin(D1, Pin.IN)

# Pin d'entrée pour la non-validité du code de désactivation
input_pin_invalid_code = Pin(D2, Pin.IN)

# Construction d'un service BLE pour l'envoi de messages
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_MSG_CHAR = (
	bluetooth.UUID(0x2A6E),
	# La caratéristique peut être lue, se notifier et "s'indiquer"
	_FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (
	_ENV_SENSE_UUID,
	(_MSG_CHAR,),
)
_ADV_APPEARANCE_GENERIC_ENVSENSOR = 5696  # Icône associée à un advertiser (GAP) de données environnementales. Voir org.bluetooth.characteristic.gap.appearance.xml


class BLEenvironment:  # Classe pour l'envoi de messages BLE
    def __init__(self, ble, name="Nucleo-WB55-VerySure"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._msg_handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_GENERIC_ENVSENSOR
        )
        self._advertise()
        self._handler = None
        dummy, byte_mac = self._ble.config('mac')
        hex_mac = hexlify(byte_mac)
        print("Adresse MAC : %s" % hex_mac.decode("ascii"))

    # Gestion des évènements BLE
    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:  # Lorsqu'un central se connecte...
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Connecté")

        elif event == _IRQ_CENTRAL_DISCONNECT:  # Lorsqu'un central se déconnecte...
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            print("Déconnecté")
            self._advertise()  # Relance l'advertising pour de futures connexions

        elif event == _IRQ_GATTS_INDICATE_DONE:  # Lorsqu'un évènement "indicate" est validé, renvoie un accusé de réception
            conn_handle, value_handle, status = data

    # Pour envoyer la température ...
    def set_msg(self, msg, notify=False, indicate=False):
        self._ble.gatts_write(self._msg_handle, msg)
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:  # Notifie les centraux connectés du rafraichissement de la valeur de la température
                    self._ble.gatts_notify(conn_handle, self._msg_handle)
                if indicate:  # "Indicate" les centraux connectés (comme Notify, mais requiert un accusé de réception)
                    self._ble.gatts_indicate(conn_handle, self._msg_handle)

    def _advertise(self, interval_us=500000):  # Envoie des trames d'advertising toutes les 5 secondes, précise que l'on pourra se connecter au device
        self._ble.gap_advertise(interval_us, adv_data=self._payload, connectable=True)


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
print("Initialisation en cours...")
ble = bluetooth.BLE()  # Initialisation du BLE
ble_env = BLEenvironment(ble)  # Initialisation de l'envoi de messages BLE
ble_env.set_msg("Alarme initialisée", notify=True, indicate=True)
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
                            ble_env.set_msg(b"Alarme en cours d'activation", notify=True, indicate=True)
                        else:
                            pwm.pulse_width_percent(0)
                            output_pin.value(0)
                            print("Porte fermée.", end="\n\n")
                    else:
                        print("Données non valides dans le message.")
                except (ValueError, TypeError) as e:
                    print("Erreur dans le traitement :", e)
        else:
            if input_pin_valid_code.value() == 1:  # Handler pour la désactivation de l'alarme
                pwm.pulse_width_percent(0)
                output_pin.value(0)
                triggered = False
                print("Bon code. Désactivation...", end="\n\n")
            if input_pin_invalid_code.value() == 1:  # Handler pour la non-désactivation de l'alarme
                pwm.pulse_width_percent(15)
                output_pin.value(1)
                ble_env.set_msg(b"Alarme activée", notify=True, indicate=True)
                print("Mauvais code. Continuation de l'alarme...", end="\n\n")
    except KeyboardInterrupt:
        print("Arrêt du programme.")
        break
