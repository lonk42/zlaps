import tkinter as tk
import tkinter.font
from datetime import datetime

# zlaps libraries
from lib.stopwatch import StopWatch
from lib.session import Session
from lib.tabs.timing import TimingTab

class UI():

	def __init__(self, window, stopwatch, sessions):

		self.session_started = True

		print('Initializing GUI...')
		self.stopwatch = stopwatch
		self.window = window
		self.sessions = sessions
		self.session_count = 0
		self.current_tab = ''
		self.sensor_ip = '10.1.1.145'

		# Fonts
		self.title_font = tk.font.Font(family = 'Helvetica', name = 'title_font', size = 24)
		self.split_font = tk.font.Font(family = 'Helvetica', name = 'split_font', size = 18)
		self.sensor_font = tk.font.Font(family = 'Helvetica', name = 'sensor_font', size = 20)
		self.sensor_ip_font = tk.font.Font(family = 'Helvetica', name = 'sensor_ip_font', size = 10)
		self.session_font = tk.font.Font(family = 'Helvetica', name = 'session_font', size = 24)

		# Title
		title = tk.Label(text = 'Zlaps 0.1', font = 'title_font')
		title.pack()

		# Top Bar
		frame_top_bar = tk.Frame(master = self.window, relief = tk.SUNKEN, borderwidth = 3)
		frame_top_bar.pack(fill = tk.X)

		# Clock Frame
		frame_clock = tk.Frame(master = frame_top_bar, relief = tk.RIDGE, borderwidth = 3)
		frame_clock.pack(fill = tk.Y, side = tk.LEFT)
		font_clock = tk.font.nametofont('TkFixedFont')
		font_clock.configure(size = 48)
		self.label_clock = tk.Label(master = frame_clock, text = '00:00:00', font = font_clock)
		self.label_clock.pack(side = tk.LEFT)

		frame_controls = tk.Frame(master = frame_clock)
		frame_controls.pack(fill = tk.Y, expand = True)
		self.button_toggle_session = tk.Button(text = 'Start Session', master = frame_controls, width = 8, bg = 'green', command = self.toggle_session)
		self.button_toggle_session.pack(fill = tk.Y, expand = True)

		# Sensor Frame
		frame_sensor = tk.Frame(master = frame_top_bar, relief = tk.RIDGE, borderwidth = 3)
		frame_sensor.pack(fill = tk.Y, side = tk.LEFT)

		self.entry_sensor_ip = tk.Entry(master = frame_sensor, width = 10, font = self.sensor_ip_font)
		self.entry_sensor_ip.insert(0, self.sensor_ip)
		self.entry_sensor_ip.pack()

		self.label_sensor = tk.Label(master = frame_sensor, text = 'Not Found', font = self.sensor_font)
		self.label_sensor.pack(side = tk.LEFT)


		# Tab bar
		tab_names = [
			('Timing', self.set_timing_tab),
			('Cars', self.set_cars_tab),
			('Results', self.set_results_tab),
			('Settings', self.set_settings_tab)
		]
		tab_bar_button_presets = {'width': 10, 'height': 3}
		frame_tab_bar = tk.Frame(master = frame_top_bar)
		frame_tab_bar.pack(side = tk.RIGHT, fill = tk.Y)

		tab_bar_buttons = {}
		for tab_name in tab_names:
			tab_bar_buttons[tab_name] = tk.Button(text = tab_name[0], master = frame_tab_bar, command = tab_name[1], **tab_bar_button_presets)
			tab_bar_buttons[tab_name].pack(side = tk.LEFT)

		self.frame_tab_content = tk.Frame()

	def clear_tab_content(self):
		self.frame_tab_content.destroy()
		self.frame_tab_content = tk.Frame(master = self.window, relief = tk.RIDGE, borderwidth = 3)
		self.frame_tab_content.pack(fill = tk.BOTH, expand = True)

	def set_timing_tab(self):
		if len(self.sessions) < 0:
			return

		self.clear_tab_content()
		self.current_tab = TimingTab(self)

	def set_cars_tab(self):
		self.current_tab = 'cars'
		self.clear_tab_content()

	def set_results_tab(self):
		self.current_tab = 'results'
		self.clear_tab_content()

	def set_settings_tab(self):
		self.current_tab = 'settings'
		self.clear_tab_content()

	def toggle_session(self):
		self.session_started = not self.session_started

		if self.session_started:
			self.button_toggle_session.configure(text = 'Start Session', bg = 'green')
		else:
			self.button_toggle_session.configure(text = 'Stop Session', bg = 'red')
			self.create_session()
			self.set_timing_tab()

		self.stopwatch.toggle()

	def create_session(self):
		self.session_count += 1
		self.sessions.append(Session(self, 'Session ' + str(self.session_count), self.stopwatch))

	def update_timer(self, time):
		self.label_clock['text'] = self.format_time_string(time)

	def update_sensor(self, distance):
		self.label_sensor['text'] = str(distance)

	def format_time_string(self, time_string):
		return datetime.strftime(datetime.utcfromtimestamp(time_string), "%M:%S:%f")[:-4]

