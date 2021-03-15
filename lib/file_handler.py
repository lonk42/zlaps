import datetime
import csv
import re
import os

# zlaps libraries
from lib.session import Session

class FileHandler():

	def __init__(self):
		self.session_directory = os.path.dirname(os.path.realpath(__file__)) + '/../saved_sessions/'
		#self.current_files os.listdir(self.session_directory)

	def load_saved_sessions(self, ui):

		# Check all files in the session dir
		for session_file in os.listdir(self.session_directory):

			# Skip any non csv
			if not re.match('.*\.csv$', session_file):
				continue

			session = self.create_session(session_file, ui)
			if session is not False:
				session.calculate_laps()
				ui.sessions.append(session)

	def create_session(self, file_path, ui):

		session_file = open(self.session_directory + file_path, "r")
		session_csv_data = csv.reader(session_file, delimiter=',')

		session = None
		for index, row in enumerate(session_csv_data):
			if index == 0:
				session = Session(ui, row[0], ui.stopwatch)
			else:
				session.add_split(split_time = float(row[0]), car_number = row[1])

		return session

	def save_session(self, session):

		# Create file and write headers
		file_path = self.session_directory + str(datetime.datetime.now()) + ' - ' + session.session_name + '.csv'
		if os.name == 'nt':
			file_path = self.session_directory.replace('\\lib\\..') + str(datetime.datetime.now()).replace(':', '') + ' - ' + session.session_name + '.csv'
			file_path = file_path.replace('/', '\\')

		session_file = open(file_path, 'w+')
		session_file.write('"' + session.session_name + '","' + str(datetime.datetime.now()) + '"\n') 

		# Write the splits
		for split in session.splits:
			session_file.write(str(split.split_time) + ',' + str(split.car_number) + ',' + str(split.lap_time) + '\n')

		session_file.close()
