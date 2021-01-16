
# zlaps libraries
from lib.stopwatch import StopWatch

class Session():

	def __init__(self, ui, session_name, stopwatch):
		self.session_name = session_name
		self.stopwatch = stopwatch
		self.ui = ui
		self.splits = []

	def add_split(self):
		self.splits.append(self.Split(self.stopwatch.get_duration()))
		self.ui.draw_splits()

	def remove_split(self, split):
		self.splits.remove(split)
		self.ui.draw_splits()

	class Split():

		def __init__(self, split_time):
			self.split_time = split_time
			self.car_number_form = None
			self.car_number = ''
