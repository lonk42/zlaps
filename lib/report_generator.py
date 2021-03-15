import os
from datetime import datetime
from fpdf import FPDF

# zlaps libraries
from lib.session import Session

class ReportGenerator():

	def __init__(self, sessions):
		self.report_directory = os.path.dirname(os.path.realpath(__file__)) + '/../reports/'
		file_path = self.report_directory + str(datetime.now()) + ' - report.pdf'
		if os.name == 'nt':
			file_path = self.report_directory.replace('\\lib\\..') + str(datetime.now()).replace(':', '') + '-report.pdf'
			file_path = file_path.replace('/', '\\')

		pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
		pdf.add_page()

		# Control variables
		pdf.set_font('Arial','',10.0) 
		pdf_width = 210
		pdf_height = 297
		table_width = 180
		table_cell_height = 7

		# Title
		pdf.set_font('Arial','B',25.0) 
		pdf.cell(pdf_width, 0.0, 'Z Club NZ - ' + str(datetime.now().strftime("%Y-%m-%d %H:%M")), align='C')
		pdf.set_font('Arial','',14.0) 
		pdf.ln(10)

		# Sessions
		for session in sessions:

			# Session title
			pdf.cell(table_width, table_cell_height, session.session_name, border = 1)
			pdf.ln(table_cell_height)

			# Car numbers
			max_laps = 0
			lap_times = session.get_laps()
			for car_number in lap_times.keys():
				pdf.cell(table_width / len(lap_times.keys()), table_cell_height, str(car_number), border = 1)

				# Find highest lap value
				if len(lap_times[car_number]) > max_laps:
					max_laps = len(lap_times[car_number])

			pdf.ln(table_cell_height)
	
			# Lap times
			for lap_number in range(0, max_laps):
				for car_number in lap_times.keys():
					try:
						if session.best_laps[car_number] == lap_number:
							pdf.set_font('Arial','B',14.0)
						pdf.cell(table_width / len(lap_times.keys()), table_cell_height, str(self.format_time_string(lap_times[car_number][lap_number])), border = 1)
						pdf.set_font('Arial','',14.0)
					except:
						pdf.cell(table_width / len(lap_times.keys()), table_cell_height, "", border = 1)

				pdf.ln(table_cell_height)

			pdf.ln(table_cell_height)

		pdf.output(file_path, 'F')

	def format_time_string(self, time_string):
		return datetime.strftime(datetime.utcfromtimestamp(time_string), "%M:%S:%f")[:-4]
