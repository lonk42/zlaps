import socket
import time
import binascii

class Listener():

	def __init__(self, ui):
		self.ui = ui
		self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.listening_socket.bind(('', 3500))

	def time_ms(self):
		return round(time.time() * 1000)

	def listen(self):

		expire_time = self.time_ms() + 5
		data_buffer = bytearray()

		while True:

			if self.time_ms() >= expire_time:
				data_buffer = bytearray()
				expire_time = self.time_ms() + 5
				continue

			try:
				data, addr = self.listening_socket.recvfrom(1024)
				data_buffer += data

				# Extend expire
				expire_time = self.time_ms() + 2

			except:
				continue

			if len(data_buffer) == 0:
				continue
			elif len(data_buffer) < 3:
				continue

			# If our data buffer doesn't have start bits trim one away
			if data_buffer[0] != 0x35 and data_buffer[1] != 0x35:
				data_buffer = data_buffer[1:]
				continue

			# The next byte is the payload size
			payload_size = int(data_buffer[2])

			# Wait till we have a full payload
			if len(data_buffer[3:(3 + payload_size)]) != payload_size:
				continue

			# VALID DATA
			payload = data_buffer[3:(3 + payload_size)]

			# 0x10 is a distance measurement
			if payload[0] == 0x10:
				distance = int.from_bytes(payload[1:], "big")
				print('Distance recieved: ' + str(distance))
				self.ui.update_sensor(distance)
			else:
				print('ERROR: Unknown mode ' + str(payload[0]))

			# Extra data is moved on for another cycle
			data_buffer = data_buffer[(3 + payload_size):]


