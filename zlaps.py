#!/usr/bin/python3

# System libraries
from threading import Thread
import tkinter as tk
import socket

# zlaps libraries
from lib.ui import UI
from lib.stopwatch import StopWatch
from lib.listener import Listener

class zlaps():

	def __init__(self):
		print('Starting zlaps...')
		self.window = tk.Tk()
		self.stopwatch = StopWatch()
		self.sessions = []
		self.ui = UI(self.window, self.stopwatch, self.sessions)
		self.listener = Listener(self.ui)

		# Threaded classes
		listener_thread = Thread(target=self.listener.listen, daemon=True)
		listener_thread.start()

		self.register_sensor()
		self.update_stopwatch()
		self.ui_scheduler()
		self.window.mainloop()
		print('Exiting.')

	def register_sensor(self):

		# Read the sensor ip form
		self.ui.sensor_ip = self.ui.entry_sensor_ip.get()

		# Send the registration packet
		local_ip = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
		byte_message = bytearray([0x35, 0x35, 0x05, 0x01]) + local_ip
		try:
			socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(byte_message, (self.ui.sensor_ip, 3500))
		except:
			pass

		self.window.after(5000, self.register_sensor)

	def update_stopwatch(self):
		if self.stopwatch.running:
			self.ui.update_timer(self.stopwatch.get_duration())
		self.window.after(10, self.update_stopwatch)

	def ui_scheduler(self):
		try:
			self.ui.current_tab.scheduler()
		except:
			pass
		self.window.after(200, self.ui_scheduler)

# Launch Application
if __name__ == "__main__":
	zlaps()

