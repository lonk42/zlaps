
# zlaps libraries
from lib.stopwatch import StopWatch

class Session():

	def __init__(self, ui, session_name, stopwatch):
		self.session_name = session_name
		self.stopwatch = stopwatch
		self.ui = ui
		self.splits = []
		self.best_laps = dict()

	def add_split(self, split_time = None, car_number = ''):

		if split_time is not None:
			self.splits.append(self.Split(split_time, car_number = car_number))
		else:
			self.splits.append(self.Split(self.stopwatch.get_duration()))
			self.ui.current_tab.draw_splits()

	def remove_split(self, split):
		self.splits.remove(split)
		self.ui.current_tab.draw_splits()

	# Make a list of unqiue car numbers in this session
	def car_list(self):

		car_numbers = []
		for split in self.splits:
			if split.car_number != '' and split.car_number not in car_numbers:
				car_numbers.append(split.car_number)

		return car_numbers

	def calculate_laps(self):

		# Itterate over each unique car
		for car_number in self.car_list():

			# Find all the splits for this car
			car_splits = []
			for split in self.splits:
				if split.car_number == car_number:
					car_splits.append(split)

			# Now calculate the laps
			for index, split in enumerate(car_splits):
				if index == 0:
					continue
				split.lap_time = split.split_time - car_splits[index - 1].split_time

	# Return a dict of each cars laps
	def get_laps(self):

		laps_dict = dict()
		for split in self.splits:
			if split.lap_time != -1 and split.car_number is not '':

				if split.car_number not in laps_dict.keys():
					laps_dict[split.car_number] = []
					
				laps_dict[split.car_number].append(split.lap_time)

				# See if its our best lap
				if self.best_laps.get(split.car_number) is None:
					self.best_laps[split.car_number] = 0

				try:
					if split.lap_time < laps_dict[split.car_number][self.best_laps[split.car_number]]:
						self.best_laps[split.car_number] = len(laps_dict[split.car_number]) - 1
				except:
					pass

		return laps_dict

	class Split():

		def __init__(self, split_time, car_number = ''):
			self.lap_time = -1
			self.split_time = split_time
			self.car_number_form = None
			self.car_number = car_number
