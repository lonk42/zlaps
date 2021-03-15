import tkinter as tk

# zlaps libraries
from lib.report_generator import ReportGenerator

class SessionsTab():

	def __init__(self, ui):
		self.ui = ui

		# Container
		frame_title = tk.Frame(master = self.ui.frame_tab_content)
		frame_title.pack()

		# Sessions
		self.tick_boxes = []
		self.frame_sessions = None
		self.draw_sessions()

	def scheduler(self):
		pass

	def generate_report(self):
		sessions_to_report = []
		for counter, tickbox in enumerate(self.tick_boxes):
			if tickbox.get() == 1:
				sessions_to_report.append(self.ui.sessions[counter])

		ReportGenerator(sessions_to_report)

	def draw_sessions(self):

		try:
			self.frame_sessions.destroy()
			self.canvas_sessions.destroy()
			self.scroll_y_sesssions.destroy()
		except:
			pass

		# Create canvas and frames
		self.canvas_sessions = tk.Canvas(self.ui.frame_tab_content)
		self.scroll_y_sessions = tk.Scrollbar(self.ui.frame_tab_content, orient="vertical", command=self.canvas_sessions.yview)
		self.frame_sessions = tk.Frame(self.canvas_sessions)

		self.generate_report_button = tk.Button(
			master = self.frame_sessions, text = 'Generate Report', width = 20, height = 1, command = self.generate_report,
			font = self.ui.session_font
		)
		self.generate_report_button.pack()

		# Populate sessions
		for counter, session in enumerate(self.ui.sessions):
			session_frame = tk.Frame(master = self.frame_sessions, relief = tk.GROOVE, borderwidth = 3)
			session_frame.pack(side = tk.TOP, fill = tk.X)

			self.tick_boxes.append(tk.IntVar())
			session_tickbox = tk.Checkbutton(master = session_frame, text = session.session_name, font = self.ui.session_font, variable = self.tick_boxes[counter])
			session_tickbox.pack(side = tk.TOP)

			cars_frame = tk.Frame(master = session_frame)
			cars_frame.pack()

			# Lap times for each car
			laps = session.get_laps()
			for car_number in laps.keys():
				car_laps_frame = tk.Frame(master = cars_frame, relief = tk.RAISED, borderwidth = 2)
				car_laps_frame.pack(side = tk.LEFT)
				tk.Label(master = car_laps_frame, text = '#' + str(car_number)).pack()

				for index, lap in enumerate(laps[car_number]):
					tk.Label(master = car_laps_frame, text = str(index + 1) + ": " + self.ui.format_time_string(lap)).pack()


		# Populate everything
		self.canvas_sessions.create_window(0, 0, anchor='nw', window=self.frame_sessions)
		self.canvas_sessions.update_idletasks()

		self.canvas_sessions.configure(scrollregion=self.canvas_sessions.bbox('all'), yscrollcommand=self.scroll_y_sessions.set)

		self.canvas_sessions.pack(fill = tk.BOTH, expand = True, side = tk.LEFT)
		self.scroll_y_sessions.pack(fill = tk.Y, side = tk.RIGHT)


