# Example to generate advertising frames for BLE

from micropython import const
import struct
import bluetooth

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
_ADV_TYPE_MANUFACTURER = const(0xFF)

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

def demo():
	payload = adv_payload(name='micropython', services=[bluetooth.UUID(0x181A), bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')])
	print(payload)
	print(decode_name(payload))
	print(decode_services(payload))

if __name__ == '__main__':
	demo()