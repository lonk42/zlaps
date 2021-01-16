import tkinter as tk
import tkinter.font
from datetime import datetime
from functools import partial

# zlaps libraries
from lib.stopwatch import StopWatch
from lib.session import Session

class UI():

	def __init__(self, window, stopwatch, sessions):

		self.session_started = True

		print('Initializing GUI...')
		self.stopwatch = stopwatch
		self.window = window
		self.sessions = sessions
		self.session_count = 0
		self.current_tab = ''

		# Fonts
		self.spilt_font = tk.font.Font(family = 'Helvetica', name = 'split_font', size = 18)
		self.session_font = tk.font.Font(family = 'Helvetica', name = 'session_font', size = 24)
		self.title_font = tk.font.Font(family = 'Helvetica', name = 'title_font', size = 24)

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

		# Tab bar
		tab_names = [
			('Timing', self.set_timing_tab),
			('Cars', self.set_cars_tab),
			('Results', self.set_results_tab),
			('Settings', self.set_settings_tab)
		]
		tab_bar_button_presets = {'width': 20, 'height': 3}
		frame_tab_bar = tk.Frame(master = frame_top_bar)
		frame_tab_bar.pack(side = tk.RIGHT, fill = tk.Y)

		tab_bar_buttons = {}
		for tab_name in tab_names:
			tab_bar_buttons[tab_name] = tk.Button(text = tab_name[0], master = frame_tab_bar, command = tab_name[1], **tab_bar_button_presets)
			tab_bar_buttons[tab_name].pack(side = tk.LEFT)

		self.frame_tab_content = tk.Frame()

	def scheduler(self):
		if self.current_tab == 'timing':
			self.save_splits()

	def clear_tab_content(self):
		self.frame_tab_content.destroy()
		self.frame_tab_content = tk.Frame(master = self.window, relief = tk.RIDGE, borderwidth = 3)
		self.frame_tab_content.pack(fill = tk.BOTH, expand = True)

	##### Timing Tab

	def set_timing_tab(self):
		self.current_tab = 'timing'
		self.clear_tab_content()

		if len(self.sessions) < 0:
			return

		# Container
		frame_title = tk.Frame(master = self.frame_tab_content)
		frame_title.pack()

		# Heading
		self.label_session_title = tk.Label(master = frame_title, text = self.sessions[-1].session_name, font = 'session_font')
		self.label_session_title.pack()

		# Splits
		self.frame_splits = None
		#self.frame_splits = tk.Frame(master = self.frame_tab_content, relief = tk.RIDGE, borderwidth = 3)
		#self.frame_splits.pack(side = tk.LEFT, fill = tk.Y)

		self.draw_splits()

	def save_splits(self):

		# Read off any existing car numbers
		for split in self.sessions[-1].splits:
			if split.car_number_form is not None:
				try:
					split.car_number = split.car_number_form.get()
				except:
					pass

	def draw_splits(self):

		# Clear splits
		self.save_splits()
		try:
			self.frame_splits.destroy()
			self.canvas_splits.destroy()
			self.scroll_y_splits.destroy()
		except:
			pass

		# Create canvas and frames
		self.canvas_splits = tk.Canvas(self.frame_tab_content)
		self.scroll_y_splits = tk.Scrollbar(self.frame_tab_content, orient="vertical", command=self.canvas_splits.yview)
		self.frame_splits = tk.Frame(self.canvas_splits)

		# Populate splits
		for split in self.sessions[-1].splits:
			split_frame = tk.Frame(master = self.frame_splits, relief = tk.GROOVE, borderwidth = 3)
			split_frame.pack(side = tk.TOP)

			split_button_delete = tk.Button(
				master = split_frame, text = 'X', width = 1, height = 1, 
				command = partial(self.sessions[-1].remove_split, split)
			)
			split_button_delete.pack(side = tk.LEFT)

			split_label = tk.Label(master = split_frame, text = self.format_time_string(split.split_time) + ' ', font = 'split_font')
			split_label.pack(side = tk.LEFT)

			split_entry_car_number = tk.Entry(master = split_frame, width = 5, font = 'split_font')
			split_entry_car_number.insert(0, split.car_number)
			split.car_number_form = split_entry_car_number
			split_entry_car_number.pack()

		add_split_button = tk.Button(text = 'Add Split', master = self.frame_splits, width = 25, height = 4, command = self.sessions[-1].add_split)
		add_split_button.pack(side = tk.TOP)

		# Populate everything
		self.canvas_splits.create_window(0, 0, anchor='nw', window=self.frame_splits)
		self.canvas_splits.update_idletasks()

		self.canvas_splits.configure(scrollregion=self.canvas_splits.bbox('all'), yscrollcommand=self.scroll_y_splits.set)

		self.canvas_splits.pack(fill='both', expand=True, side='left')
		self.scroll_y_splits.pack(fill='y', side='right')

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

	def format_time_string(self, time_string):
		return datetime.strftime(datetime.utcfromtimestamp(time_string), "%M:%S:%f")[:-4]

