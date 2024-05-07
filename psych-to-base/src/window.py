from main import convert
import logging

def init():
	logging.info('Initiating window')

	# initiate the window

	# the code below should go on the callback when the person presses the convert button
	psych_mod_folder_path = 'path_after_user_selected_it'
	result_path = 'path_after_user_selected_it'
	options = {
		'shaders': True,
		'songs': False,
		'characters': True
	}

	if psych_mod_folder_path != None and result_path != None:
		convert(psych_mod_folder=psych_mod_folder_path, result_folder=result_path, options=options)

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
