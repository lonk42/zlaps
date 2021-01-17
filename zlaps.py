#!/usr/bin/python3

# System libraries
import tkinter as tk

# zlaps libraries
from lib.ui import UI
from lib.stopwatch import StopWatch

class zlaps():

	def __init__(self):
		print('Starting zlaps...')
		self.window = tk.Tk()
		self.stopwatch = StopWatch()
		self.sessions = []
		self.ui = UI(self.window, self.stopwatch, self.sessions)

		self.update_stopwatch()
		self.ui_scheduler()
		self.window.mainloop()
		print('Exiting.')

	def update_stopwatch(self):
		if self.stopwatch.running:
			self.ui.update_timer(self.stopwatch.get_duration())
		self.window.after(10, self.update_stopwatch)

	def ui_scheduler(self):
		try:
			self.ui.current_tab.scheduler()
		except:
			pass
		self.window.after(200, self.ui_scheduler)

# Launch Application
if __name__ == "__main__":
	zlaps()

