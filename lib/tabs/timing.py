import tkinter as tk
from functools import partial

class TimingTab():

	def __init__(self, ui):
		self.ui = ui

		# Container
		frame_title = tk.Frame(master = self.ui.frame_tab_content)
		frame_title.pack()

		# Heading
		self.entry_session_title = tk.Entry(master = frame_title, width = 16, font = self.ui.session_font)
		self.entry_session_title.insert(0, self.ui.sessions[-1].session_name)
		self.entry_session_title.pack()

		# Splits
		self.frame_splits = None
		self.draw_splits()
		self.draw_times()

	def scheduler(self):
		self.ui.sessions[-1].session_name = self.entry_session_title.get()
		self.ui.sessions[-1].calculate_laps()
		self.save_splits()

	def save_splits(self):

		# Read off any existing car numbers
		for split in self.ui.sessions[-1].splits:
			if split.car_number_form is not None:
				try:
					split.car_number = split.car_number_form.get()
				except:
					pass

	def draw_times(self):
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
		self.canvas_splits = tk.Canvas(self.ui.frame_tab_content)
		self.scroll_y_splits = tk.Scrollbar(self.ui.frame_tab_content, orient="vertical", command=self.canvas_splits.yview)
		self.frame_splits = tk.Frame(self.canvas_splits)

		# Populate splits
		for split in self.ui.sessions[-1].splits:
			split_frame = tk.Frame(master = self.frame_splits, relief = tk.GROOVE, borderwidth = 3)
			split_frame.pack(side = tk.TOP, fill = tk.X)

			split_button_delete = tk.Button(
				master = split_frame, text = 'X', width = 1, height = 1, 
				command = partial(self.ui.sessions[-1].remove_split, split)
			)
			split_button_delete.pack(side = tk.LEFT)

			split_label = tk.Label(master = split_frame, text = self.ui.format_time_string(split.split_time) + ' ', font = self.ui.split_font)
			split_label.pack(side = tk.LEFT)

			split_entry_car_number = tk.Entry(master = split_frame, width = 5, font = self.ui.split_font)
			split_entry_car_number.insert(0, split.car_number)
			split.car_number_form = split_entry_car_number
			split_entry_car_number.pack(side = tk.LEFT)

			# Lap times if there is one
			if split.lap_time != -1:
				split_label_lap_time = tk.Label(master = split_frame, text = self.ui.format_time_string(split.lap_time))
				split_label_lap_time.pack(side = tk.LEFT)

		# Manual button
		add_split_button = tk.Button(text = 'Add Split', master = self.frame_splits, width = 25, height = 4, command = self.ui.sessions[-1].add_split)
		add_split_button.pack(side = tk.TOP)

		# Populate everything
		self.canvas_splits.create_window(0, 0, anchor='nw', window=self.frame_splits)
		self.canvas_splits.update_idletasks()

		self.canvas_splits.configure(scrollregion=self.canvas_splits.bbox('all'), yscrollcommand=self.scroll_y_splits.set)

		self.canvas_splits.pack(fill = tk.BOTH, expand = True, side = tk.LEFT)
		self.scroll_y_splits.pack(fill = tk.Y, side = tk.RIGHT)


