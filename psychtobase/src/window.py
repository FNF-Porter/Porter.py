import psychtobase.main as main
import logging
import os
import psychtobase.src.Constants as Constants
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

class Window(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("FNF Porter")
		self.setFixedSize(QSize(800, 600))
		self.setMinimumSize(QSize(800, 600))
		self.setMaximumSize(QSize(800, 600))

		self.setWindowIcon(QIcon(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'defaults', 'tempicon.ico'))))
		button = QPushButton("Convert")
		button.clicked.connect(lambda: print('hi'))
		


def init():
	logging.info('Initiating window')

	# initiate the window
	app = QApplication([])
	window = Window()
	window.show()

	convertCallback()

	app.exec()

def report_progress(text):
	# update the bottom text to display text
	print(text)

def prompt(prompt, body, inputs, file):
	# Simple prompt
	if prompt == 'input':
		print(f'[{file}] Requesting information') # Window title
		print(body) # Text

		results = ['' for i in enumerate(inputs)]

		for index, entry in enumerate(inputs):
			input_label = entry[0]
			input_placeholder = entry[1]

			print(input_label) # Text above the input
			results[index] = input(input_placeholder)
			# Inside the input as a placeholder goes the input_placeholder

		button = 'Continue'

		return results # When the continue button is pressed

def convertCallback():
	# the code below should go on the callback when the person presses the convert button
	psych_mod_folder_path = 'path_after_user_selected_it'
	result_path = 'path_after_user_selected_it'
	options = Constants.DEFAULT_OPTIONS

	if psych_mod_folder_path != None and result_path != None:
		main.convert(psych_mod_folder=psych_mod_folder_path, result_folder=result_path, options=options)