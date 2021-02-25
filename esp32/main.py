from machine import UART, freq
import uasyncio as asyncio
import binascii
import network
import webrepl
import usocket
import utime

class LapTimer():

	def __init__(self):

		# Initalize
		freq(240000000)

		# Network
		ap = network.WLAN(network.AP_IF)
		ap.active(True)
		ap.config(essid='zlaps_sensor')
		ap.config(authmode=3, password='zlaps_sensor_123')

		while ap.active() == False:
		  print('Waiting for connection...')

		print('Connection successful')
		print(ap.ifconfig())

		webrepl.start()

		# LapTimer
		self.uart = UART(2, 115200)
		self.uart.init(115200, bits = 8, parity = None, stop = 1)
		self.distance = 0
		self.strength = 0
		self.subscriber_ip = None
		loop = asyncio.get_event_loop()

		# Setings
		self.trigger_distance = 140
		self.trigger_lockout = False

		# Sockets
		self.ip_address = ap.ifconfig()[0]
		self.listening_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
		self.listening_socket.bind(usocket.getaddrinfo(self.ip_address, 3500)[0][-1])
		self.listening_socket.settimeout(0)

		# Setup scheduled jobs
		loop.create_task(self.send_distance())
		loop.create_task(self.check_sensor())
		loop.create_task(self.check_socket())

		# LESH GO
		try:
			loop.run_forever()
		finally:
			loop.close()

	def send_distance(self):
		while True:
			await asyncio.sleep_ms(200)

			if self.subscriber_ip is not None:
				#print("Sending distance: " + str(self.distance))
				try:
					s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
					s.connect(usocket.getaddrinfo(self.subscriber_ip, 3500)[0][-1])
					s.send(bytearray([0x35, 0x35, 0x03, 0x10]) + bytearray(self.distance.to_bytes(2, 'big')))
					s.close()
				except Exception as e:
					print(e)

	def check_socket(self):
		while True:
			await asyncio.sleep_ms(200)

			expire_time = utime.ticks_ms() + 50
			data_buffer = bytearray()

			# Try find a data packet
			while len(data_buffer) < 24:
				await asyncio.sleep_ms(5)

				if utime.ticks_ms() >= expire_time:
					#print('Expire!!!!')
					break

				try:
					data = self.listening_socket.recv(64)
					#print('Data recv')
					#print(binascii.hexlify(data))

					data_buffer += data
					#print('Updated buffer')
					#print(binascii.hexlify(data_buffer))

					# Extend expire
					expire_time = utime.ticks_ms() + 20
				except:
					continue
	
				if len(data_buffer) == 0:
					#print('Buffer empty. quitting')
					break
				elif len(data_buffer) < 3:
					#print('Buffer too small (' + str(len(data_buffer)) + '), trying again')
					continue

				# If our data buffer doesn't have start bits trim one away
				if data_buffer[0] != 0x35 and data_buffer[1] != 0x35:
					#print('ERROR: Start bits incorrect, trimming')
					data_buffer = data_buffer[1:]
					continue

				#print('Start bits found!')

				# The next byte is the payload size
				payload_size = int(data_buffer[2])
				#print('Payload size: ' + str(payload_size))

				# Wait till we have a full payload
				if len(data_buffer[3:(3 + payload_size)]) != payload_size:
					#print('Data missing')
					continue

				# VALID DATA
				payload = data_buffer[3:(3 + payload_size)]
				#print('Valid Data: ' + str(binascii.hexlify(payload)))

				# First byte is the mode selector

				# 0x01 is ip registering
				if payload[0] == 0x01:
					ip_bin = payload[1:]
					ip_hex = binascii.hexlify(ip_bin).decode("utf-8")
					ip_string = '.'.join(str(int(i, 16)) for i in [ip_hex[i:i+2] for i in range(0, len(ip_hex), 2)])
					print('Registering subscriber: ' + ip_string)
					self.subscriber_ip = ip_string
				else:
					print('ERROR: Unknown mode ' + str(payload[0]))

				# Extra data is moved on for another cycle
				data_buffer = data_buffer[(3 + payload_size):]
				break


	def check_sensor(self):
		while True:
			await asyncio.sleep_ms(1)

			data = self.uart.read(9)
			if data:

				# Ensure we got a full frame
				if len(data) != 9:
					print('ERROR: Data incorrect size')
					continue

				# Make sure the start bits are correct
				if data[0] != 0x59 and data[1] != 0x59:
#					print('ERROR: Start bits incorrect')
					self.uart.read()
					continue

				# Read the frame
				checksum = 0
				for i in range(0, 8):
					checksum = checksum + data[i]
					checksum = checksum % 256

				if checksum == data[8]:
					self.distance = data[2] + (data[3] * 256)
					self.strength = data[4] + (data[5] * 256)
#				print(str(self.distance) + ', ' + str(self.strength))

				# Send a ping if needed
				self.check_trigger()

	def check_trigger(self):

		# Reset the lock if nothing is there
		if self.distance > self.trigger_distance:
			self.trigger_lockout = False

		# If its lower trigger a ping
		if self.distance < self.trigger_distance:

			# Only send if we have a subscriber
			if self.subscriber_ip is not None and not self.trigger_lockout:
				print("PING: " + str(self.distance))
				try:
					s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
					s.connect(usocket.getaddrinfo(self.subscriber_ip, 3500)[0][-1])
					s.send(bytearray([0x35, 0x35, 0x01, 0x20]))
					s.close()
				except Exception as e:
					print(e)

			# Lock out the trigger
			self.trigger_lockout = True


# LESH GO
LapTimer()

