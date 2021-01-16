import time

class StopWatch():

	def __init__(self):
		self.running = False
		self.start_time = 0
		self.stop_time = 0

	def toggle(self):

		if self.running: 
			self.stop_time = time.time()
		else:
			self.start_time = time.time()

		self.running = not self.running

	def get_duration(self):

		if self.running:
			return time.time() - self.start_time
		else:
			return  self.stop_time

