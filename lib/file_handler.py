import datetime
import os

class FileHandler():

	def __init__(self):
		self.session_directory = os.path.dirname(os.path.realpath(__file__)) + '/../saved_sessions/'
		#self.current_files os.listdir(self.session_directory)

	def save_session(self, session):

		# Create file and write headers
		session_file = open(self.session_directory + str(datetime.datetime.now()) + ' - ' + session.session_name + '.csv', 'w+')
		session_file.write('"' + session.session_name + '","' + str(datetime.datetime.now()) + '"\n') 

		# Write the splits
		for split in session.splits:
			session_file.write(str(split.split_time) + ',' + str(split.car_number) + ',' + str(split.lap_time) + '\n')
