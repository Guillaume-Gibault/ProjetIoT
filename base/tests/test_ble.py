# Objet du script : implémentation du protocole GATT Blue-ST pour un périphérique
# Définition d'un service _ST_APP_SERVICE avec deux caractéristiques :
# 1 - SWITCH : pour éteindre et allumer une LED du périphérique depuis un central
# 2 - TEMPERATURE : pour envoyer une mesure de température du périphérique à un central

import bluetooth  # Pour gérer le BLE
from struct import pack  # Pour agréger les octets dans la "payload" des caractéristiques
from micropython import const  # Pour la déclaration de constantes entières
import pyb  # Pour piloter les LED de la NUCLEO-WB55
from binascii import hexlify  # Convertit une donnée binaire en sa représentation hexadécimale
import struct

# Advertising frames are repeated packets with the following structure:
#   1 byte indicating the size of the data (N + 1)
#   1 byte indicating the type of data (see constants below)
#   N bytes of data of the indicated type
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)
_ADV_TYPE_MANUFACTURER = const(0xFF

# Constantes définies pour/par le protocole Blue-ST
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

# Pour les UUID et les codes, on se réfère à la documentation du SDK Blue-ST disponible ici :
# https://www.st.com/resource/en/user_manual/dm00550659-getting-started-with-the-bluest-protocol-and-sdk-stmicroelectronics.pdf.

# 1 - Définition du service personnalisé selon le SDK Blue-ST

# Indique que l'on va communiquer avec une application qui se conforme au protocole Blue-ST :
_ST_APP_UUID = bluetooth.UUID('00000000-0001-11E1-AC36-0002A5D5C51B')

# UUID d'une caractéristique de température :
_TEMPERATURE_UUID = (bluetooth.UUID('00040000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY)

# UUID d'une caractéristique d'interrupteur :
_SWITCH_UUID = (bluetooth.UUID('20000000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_WRITE | bluetooth.FLAG_NOTIFY)

# Le service contiendra ces deux caractéristiques
_ST_APP_SERVICE = (_ST_APP_UUID, (_TEMPERATURE_UUID, _SWITCH_UUID))

# 2 - Construction de la trame (contenu du message) d'avertising GAP :
_PROTOCOL_VERSION = const(0x01)  # Version du protocole
_DEVICE_ID = const(0x80)  # Carte Nucleo générique
_DEVICE_MAC = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]  # Adresse matérielle MAC fictive
_FEATURE_MASK = const(0x20040000)  # Services sélectionnés : température (2^18) et interrupteur LED (2^29)

# Explication du calcul du masque déterminant les caractéristiques du service actif (_FEATURE_MASK)
# A chaque caractéristique est associé un code binaire. On doit simplement sommer les codes de toutes les caractéristiques
# que l'on souhaite exposer avec GATT :

# Caractéristique SWITCH : code = 2^29 =      100000000000000000000000000000 (en binaire) = 20000000  (en hexadécimal)
# Caractéristique TEMPERATURE : code = 2^18 = 000000000001000000000000000000 (en binaire) = 40000     (en hexadécimal)
# _FEATURE_MASK = SWITCH + TEMPERATURE =      100000000001000000000000000000 (en binaire) = 20040000  (en hexadécimal)

# Trame d'avertising : concaténation des informations avec la fonction Micropython "pack"
# La chaîne '>BBI6B' désigne le format des arguments, voir la documentation de pack ici : https://docs.python.org/3/library/struct.html
_MANUFACTURER = pack('>BBI6B', _PROTOCOL_VERSION, _DEVICE_ID, _FEATURE_MASK, *_DEVICE_MAC)

# Initialisation des LED
led_bleu = pyb.LED(3)
led_rouge = pyb.LED(1)


# Generates a frame which will be passed to the gap_advertise(adv_data=...) method.
def adv_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0, manufacturer=0):
	payload = bytearray()

	def _append(adv_type, value):
		nonlocal payload
		payload += struct.pack('BB', len(value) + 1, adv_type) + value

	_append(_ADV_TYPE_FLAGS, struct.pack('B', (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)))

	if name:
		_append(_ADV_TYPE_NAME, name)

	if services:
		for uuid in services:
			b = bytes(uuid)
			if len(b) == 2:
				_append(_ADV_TYPE_UUID16_COMPLETE, b)
			elif len(b) == 4:
				_append(_ADV_TYPE_UUID32_COMPLETE, b)
			elif len(b) == 16:
				_append(_ADV_TYPE_UUID128_COMPLETE, b)

	if appearance:
		# See org.bluetooth.characteristic.gap.appearance.xml
		_append(_ADV_TYPE_APPEARANCE, struct.pack('<h', appearance))

	if manufacturer:
		_append(_ADV_TYPE_MANUFACTURER, manufacturer)

	return payload

def decode_field(payload, adv_type):
	i = 0
	result = []
	while i + 1 < len(payload):
		if payload[i + 1] == adv_type:
			result.append(payload[i + 2:i + payload[i] + 1])
		i += 1 + payload[i]
	return result

def decode_name(payload):
	n = decode_field(payload, _ADV_TYPE_NAME)
	return str(n[0], 'utf-8') if n else ''

def decode_services(payload):
	services = []
	for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
		services.append(bluetooth.UUID(struct.unpack('<h', u)[0]))
	for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
		services.append(bluetooth.UUID(struct.unpack('<d', u)[0]))
	for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
		services.append(bluetooth.UUID(u))
	return services


class BLESensor:
	# Initialisation, démarrage de GAP et broadcast des trames d'advertising
	def __init__(self, ble, name='WB55-GFD'):
		self._ble = ble
		self._ble.active(True)
		self._ble.irq(self._irq)
		((self._temperature_handle, self._switch_handle),) = self._ble.gatts_register_services((_ST_APP_SERVICE,))
		self._connections = set()
		self._payload = adv_payload(name=name, manufacturer=_MANUFACTURER)
		self._advertise()
		self._handler = None

		# Affiche l'adresse MAC de l'objet
		dummy, byte_mac = self._ble.config('mac')
		hex_mac = hexlify(byte_mac)
		print("Adresse MAC : %s" % hex_mac.decode("ascii"))

	# Gestion des évènements BLE...
	def _irq(self, event, data):

		# Si un central a envoyé une demande de connexion
		if event == _IRQ_CENTRAL_CONNECT:
			conn_handle, _, _, = data
			# Se connecte au central (et arrête automatiquement l'advertising)
			self._connections.add(conn_handle)
			print("Connecté à un central")
			led_bleu.on()  # Allume la LED bleue

		# Si le central a envoyé une demande de déconnexion
		elif event == _IRQ_CENTRAL_DISCONNECT:
			conn_handle, _, _, = data
			self._connections.remove(conn_handle)
			# Redémarre le mode advertising
			self._advertise()
			print("Déconnecté du central")

		# Si une écriture est détectée dans la caractéristique SWITCH (interrupteur) de la LED
		elif event == _IRQ_GATTS_WRITE:
			conn_handle, value_handle, = data
			if conn_handle in self._connections and value_handle == self._switch_handle:
				# Lecture de la valeur de la caractéristique
				data_received = self._ble.gatts_read(self._switch_handle)
				self._ble.gatts_write(self._switch_handle, pack('<HB', 1000, data_received[0]))
				self._ble.gatts_notify(conn_handle, self._switch_handle)
				# Selon la valeur écrite, on allume ou on éteint la LED rouge
				if data_received[0] == 1:
					led_rouge.on()  # Allume la LED rouge
				else:
					led_rouge.off()  # Eteint la LED rouge

	# On écrit la valeur de la température dans la caractéristique "temperature"
	# def set_data_temperature(self, temperature, notify):
	#     self._ble.gatts_write(self._temperature_handle, pack('<f', temperature))
	#     if notify:
	#         for conn_handle in self._connections:
	#             # Signale au Central que la valeur de la caractéristique vient d'être
	#             # rafraichie et qu'elle peut donc être lue.
	#             self._ble.gatts_notify(conn_handle, self._temperature_handle)

	# Pour démarrer l'advertising, avec une fréquence de 5 secondes.
	# Précise ("connectable=True") qu'un central pourra se connecter au périphérique.
	def _advertise(self, interval_us=500000):
		self._ble.gap_advertise(interval_us, adv_data=self._payload, connectable=True)
		led_bleu.off()  # Eteint la LED bleue