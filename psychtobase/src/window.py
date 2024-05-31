from base64 import b64decode
from pathlib import Path
import platform
import subprocess
import time
import logging
import src.log as log
import src.Constants as Constants
import main

import webbrowser

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel, QLineEdit, QFileDialog, QDialog, QVBoxLayout, QRadioButton, QTextBrowser, QWidget

icon = b64decode(Constants.BASE64_IMAGES.get('windowIcon'))
_windowTitleSuffix = "v0.1 [BETA]"
_defaultsFile = '.defaults'
_vocalSplitEnabledByDefault = False

app = QApplication([])
class SimpleDialog(QDialog):
	def __init__(self, title, inputs, button, body):
		super().__init__()

		self.layout = QVBoxLayout(self)
		self.inputs = []

		self.bodyLabel = QLabel(body, self)
		self.bodyLabel.move(20, 20)
		self.bodyLabel.resize(430, 30)

		for i, input in enumerate(inputs):
			label = QLabel(f"{input[0]}:", self)
			label.move(20, 50 + (60 * i))
			label.resize(430, 30)

			inputEdit = QLineEdit("", self)
			inputEdit.setPlaceholderText(input[1])
			inputEdit.resize(410, 30)
			inputEdit.move(20, 80 + (60 * i))

			self.inputs.append(inputEdit)

		self.buttonContinue = QPushButton(button, self)
		self.buttonContinue.clicked.connect(self.on_button_clicked)
		self.buttonContinue.resize(100, 30)
		self.buttonContinue.move(330, 200)

		self.setFixedSize(QSize(450, 250))
		self.setWindowTitle(title)

		pixmap = QPixmap()
		pixmap.loadFromData(icon)
		self.setWindowIcon(QIcon(pixmap))

		self.exec()

	def on_button_clicked(self):
		self.input_values = [input.text() for input in self.inputs]
		# print(self.input_values)

		self.close()

class ErrorMessage(QDialog):
	def __init__(self, text, actual_error_text, windowObject):
		super().__init__()
		layout = QVBoxLayout(self)
		self.layout = layout

		try:
			text
		except:
			#if text isnt given itll set it to unknown error
			text = 'Unknown Error'

		try:
			actual_error_text
		except:
			actual_error_text = "the fucking error handler had a bug dude, you're fucked! This is indeed a classic FNF moment"

		self.setWindowTitle(text)

		widErr = 400
		heiErr = 200

		self.setFixedSize(QSize(widErr, heiErr))
		
		pixmap = QPixmap()
		pixmap.loadFromData(b64decode(Constants.BASE64_IMAGES.get('errorIcon')))
		self.errorIcon = QImage(pixmap)

		self.text = QLabel(actual_error_text, self)
		self.text.move(20, 20)
		self.text.resize(widErr - 40, heiErr - 40)

		self.openLog = QPushButton('Open log file', self)
		self.openLog.move((widErr - self.openLog.width()) - 20, (heiErr - self.openLog.height()) - 20)
		self.openLog.clicked.connect(windowObject.openLogFile)

		self.buttonContinue = QPushButton("I dont care", self)
		self.buttonContinue.clicked.connect(self.on_button_clicked)
		self.buttonContinue.move((widErr - (self.openLog.width() + self.buttonContinue.width())) - 20, (heiErr - self.buttonContinue.height()) - 20)

		self.exec()

	def on_button_clicked(self):
		self.close()
		
class Window(QMainWindow):
	def closeEvent(self, event):
		logging.info('Thanks for using FNF Porter!')
		#time.sleep(0.1)
		event.accept()

	def __init__(self):
		super().__init__()

		_windowTitleSuffix = f"v{Constants.VERSION} [BETA]"
		self.setWindowTitle(f"FNF Porter {_windowTitleSuffix}")
		wid = 750
		hei = 650
		
		self.setFixedSize(QSize(wid, hei))
		self.setMinimumSize(QSize(wid, hei))
		self.setMaximumSize(QSize(wid, hei))
		
		pixmap = QPixmap()
		pixmap.loadFromData(icon)
		self.setWindowIcon(QIcon(pixmap))

		self.modLabel = QLabel("Path to your Psych Engine mod:", self)
		self.baseGameLabel = 	QLabel("Path to Base Game mods folder:", self)
		self.modLabel.move(20, 20)
		self.modLabel.resize(220, 30)
		self.baseGameLabel.move(20, 60)
		self.baseGameLabel.resize(220, 30)

		self.findModButton = QPushButton("Locate...", self)
		self.findBaseGameButton = QPushButton("Locate...", self)
		self.findModButton.setToolTip("Open File Dialog")
		self.findBaseGameButton.setToolTip("Open File Dialog")
		self.findModButton.move((self.width() - 20) - self.findModButton.width(), 20)
		self.findBaseGameButton.move((self.width() - 20) - self.findBaseGameButton.width(), 60)  # Move the button closer to the other one
		self.findModButton.clicked.connect(self.findMod)
		self.findBaseGameButton.clicked.connect(self.findBaseGame)

		# thingDefaultPath
		modDP = ''
		bGDP = ''
		if Path(_defaultsFile).exists():
			try:
				parse = open(_defaultsFile, 'r').read()
				for index, line in enumerate(parse.split('\n')):
					if index == 0:
						modDP = line
					if index == 1:
						bGDP = line
			except Exception as e:
				logging.error(f'Problems loading your save: {e}')

		self.modLineEdit = QLineEdit(modDP, self)
		self.baseGameLineEdit = QLineEdit(bGDP, self)
		self.modLineEdit.move((self.findModButton.x() - 20) - 400, 20)
		self.baseGameLineEdit.move((self.findBaseGameButton.x() - 20) - 400, 60)
		self.modLineEdit.resize(400, 30)  # Adjust the size as needed
		self.baseGameLineEdit.resize(400, 30)  # Adjust the size as needed

		## Section 1, PRESETS
		rX = 20

		self.defaultsLabel = QLabel("Presets", self)
		self.defaultsLabel.move(rX, 100)
		self.defaultsLabel.resize(220, 30)

		self.onlyCharts = QRadioButton('Only Charts', self)
		self.onlyCharts.move(rX, 140)

		self.onlySongs = QRadioButton('Only Audio', self)
		self.onlySongs.move(rX, 170)

		self.onlyChars = QRadioButton('Only Characters', self) # not to be confused with onlyCharts
		self.onlyChars.move(rX, 200)
		self.onlyChars.resize(400, 30)

		self.onlyStages = QRadioButton('Only Stages', self)
		self.onlyStages.move(rX, 230)

		self.fullMod = QRadioButton('Full Mod', self)
		self.fullMod.move(rX, 260)
		self.fullMod.setChecked(True) # Default

		self.iChoose = QRadioButton('Custom', self)
		self.iChoose.move(rX, 290)

		self.onlyCharts.toggled.connect(self.radioCheck)
		self.onlySongs.toggled.connect(self.radioCheck)
		self.onlyChars.toggled.connect(self.radioCheck)
		self.onlyStages.toggled.connect(self.radioCheck)
		self.fullMod.toggled.connect(self.radioCheck)
		self.iChoose.toggled.connect(self.radioCheck)

		## Section 2, Help

		self.ohioSkibidi = QPushButton("Open log file", self)
		self.ohioSkibidi.move(20, 320)
		self.ohioSkibidi.resize(100, 30)
		self.ohioSkibidi.clicked.connect(self.openLogFile)

		self.logsLabel = QTextBrowser(self)
		self.logsLabel.move(20, 360)
		self.logsLabel.resize(320, 270)

		self.helpButton = QPushButton("Report an issue", self)
		self.helpButton.setToolTip('https://github.com/gusborg88/fnf-porter/issues/new/choose/')
		self.helpButton.move(130, 320)
		self.helpButton.resize(100, 30)
		self.helpButton.clicked.connect(self.goToIssues)

		self.gbButton = QPushButton("Gamebanana", self)
		self.gbButton.setToolTip('https://gamebanana.com/tools/16982')
		self.gbButton.move(240, 320)
		self.gbButton.resize(100, 30)
		self.gbButton.clicked.connect(self.goToGB)

		## Section 3, Options
		sX = int(wid / 2)

		_catItemLeftSpacing = 15 # Categorized group padding-left.

		sSX = sX + _catItemLeftSpacing

		_newCheckbox = 20 # A checkbox, categorized or not.
		_newCheckboxInCat = 20 # A checkbox inside a categorized group.
		_newCheckboxAfterCat = 30 # A checkbox after a categorized group of checkboxes.
		_spacingBelowLabel = 40 # A checkbox below a label.

		_currentYPos = 100

		self.optionsLabel = QLabel("Options", self)
		self.optionsLabel.move(sX, _currentYPos)
		self.optionsLabel.resize(220, 30)

		_currentYPos += _spacingBelowLabel

		self.charts = QCheckBox("Charts", self)
		self.charts.move(sX, _currentYPos)
		self.charts.setToolTip("Select all charts in the \"/data/\" directory of your mod and convert them.")

		self.charts.stateChanged.connect(self.chartsEventsSection)

		_currentYPos += _newCheckboxInCat

		self.events = QCheckBox("Events", self)
		self.events.move(sSX, _currentYPos)
		self.events.setToolTip("Adds minimal support for events: \"Play Animation\", \"Alt Animation\" notes and \"Change Character\" (Creates a module file at the root of your mod).")

		_currentYPos += _newCheckboxAfterCat

		self.songs = QCheckBox("Audio", self)
		self.songs.move(sX, _currentYPos)
		self.songs.setToolTip("Select audio in different directories of your mod and copy them.")

		self.songs.stateChanged.connect(self.songsSection)

		_currentYPos += _newCheckboxInCat

		self.insts = QCheckBox("Instrumentals", self)
		self.insts.move(sSX, _currentYPos)
		self.insts.setToolTip("Copy over \"Inst.ogg\" files.")

		_currentYPos += _newCheckboxInCat

		self.voices = QCheckBox("Voices", self)
		self.voices.move(sSX, _currentYPos)
		self.voices.setToolTip("Copy over \"Voices.ogg\" files.")

		_currentYPos += _newCheckboxInCat

		self.music = QCheckBox("Music", self)
		self.music.move(sSX, _currentYPos)
		self.music.setToolTip("Copies over files in the \"music\" directory of your mod.")

		_currentYPos += _newCheckboxInCat

		self.sounds = QCheckBox("Sounds", self)
		self.sounds.move(sSX, _currentYPos)
		self.sounds.setToolTip("Copies over files and folders in the \"sounds\" directory of your mod.")
		
		_currentYPos += _newCheckboxInCat

		# Is available just not for avoiding error :D
		self.vocalsplit = QCheckBox("Vocal Split", self)
		self.vocalsplit.move(sSX, _currentYPos)
		self.vocalsplit.setToolTip("Splits \"Voices.ogg\" files into two files (\"Voices-opponent.ogg\" and \"Voices-player.ogg\") using their charts. This requires ffmpeg in PATH, and Charts enabled.")

		_currentYPos += _newCheckboxAfterCat

		self.chars = QCheckBox("Characters", self)
		self.chars.move(sX, _currentYPos)
		self.chars.setToolTip("Select all characters in the \"/characters/\" directory of your mod and convert them.")

		self.chars.stateChanged.connect(self.characterSection)

		_currentYPos += _newCheckboxInCat

		self.icons = QCheckBox("Health Icons", self)
		self.icons.move(sSX, _currentYPos)
		self.icons.setToolTip("Copies over all of your character icon .png files from the \"/images/icons/\" directory of your mod. This also generates Freeplay Icons (These require characters enabled).")

		_currentYPos += _newCheckboxInCat

		self.jsons = QCheckBox(".json files", self)
		self.jsons.move(sSX, _currentYPos)
		self.jsons.setToolTip("Converts your character's .json files to the appropiate format.")

		_currentYPos += _newCheckboxInCat

		self.charassets = QCheckBox("Assets", self)
		self.charassets.move(sSX, _currentYPos)
		self.charassets.setToolTip("Copies over your .png and .xml files from the \"/images/characters/\" directory of your mod.")

		_currentYPos += _newCheckboxAfterCat

		self.weeks = QCheckBox("Weeks", self)
		self.weeks.move(sX, _currentYPos)
		self.weeks.setToolTip("Select week conversions.")

		self.weeks.stateChanged.connect(self.weekSection)

		_currentYPos += _newCheckboxInCat

		self.props = QCheckBox("Menu Characters (Props)", self)
		self.props.move(sSX, _currentYPos)
		self.props.resize(400, 30)
		self.props.setToolTip("Converts your menu character .json files from the \"/images/menucharacters/\" directory of your mod to the appropiate format.")

		_currentYPos += _newCheckboxInCat

		self.titles = QCheckBox("Week Images (Titles)", self)
		self.titles.move(sSX, _currentYPos)
		self.titles.resize(400, 30)
		self.titles.setToolTip("Copies over your .png files from the \"/images/storymenu/\" directory of your mod.")

		_currentYPos += _newCheckboxInCat

		self.levels = QCheckBox("Levels", self)
		self.levels.move(sSX, _currentYPos)
		self.levels.setToolTip("Converts your week .json files from the \"/weeks/\" directory of your mod to the appropiate format.")

		_currentYPos += _newCheckboxAfterCat

		self.stages = QCheckBox("Stages", self)
		self.stages.move(sX, _currentYPos)
		self.stages.setToolTip("Converts stage .jsons from the \"/stages/\" directory of your mod and parses the .lua files to asign props.")

		_currentYPos += _newCheckbox

		self.meta = QCheckBox("Pack Meta", self)
		self.meta.move(sX, _currentYPos)
		self.meta.setToolTip("Converts your \"pack.json\" to the appropiate format, and copies your \"pack.png\" file.")

		_currentYPos += _newCheckbox

		self.images = QCheckBox("Images", self)
		self.images.move(sX, _currentYPos)
		self.images.setToolTip("Copies over your .png and .xml files from the \"/images/\" directory of your mod.")

		self.convert = QPushButton("Convert", self)
		self.convert.move((self.width() - 20) - self.convert.width(), (self.height() - 20) - self.convert.height())
		self.convert.clicked.connect(self.convertCallback)

		self.radioCheck(True, True)

	def allToDefaults(self, checked = True, enabled = False):
		self.charts.setChecked(checked)
		self.events.setChecked(checked)
		self.songs.setChecked(checked)
		self.insts.setChecked(checked)
		self.voices.setChecked(checked)
		self.vocalsplit.setChecked(checked == _vocalSplitEnabledByDefault and checked != False)
		self.music.setChecked(checked)
		self.sounds.setChecked(checked)
		self.chars.setChecked(checked)
		self.icons.setChecked(checked)
		self.jsons.setChecked(checked)
		self.charassets.setChecked(checked)
		self.weeks.setChecked(checked)
		self.props.setChecked(checked)
		self.titles.setChecked(checked)
		self.levels.setChecked(checked)
		self.stages.setChecked(checked)
		self.meta.setChecked(checked)
		self.images.setChecked(checked)


		self.charts.setEnabled(enabled)
		self.events.setEnabled(enabled)
		self.songs.setEnabled(enabled)
		self.insts.setEnabled(enabled)
		self.voices.setEnabled(enabled)
		self.vocalsplit.setEnabled(enabled)
		self.music.setEnabled(enabled)
		self.sounds.setEnabled(enabled)
		self.chars.setEnabled(enabled)
		self.icons.setEnabled(enabled)
		self.jsons.setEnabled(enabled)
		self.charassets.setEnabled(enabled)
		self.weeks.setEnabled(enabled)
		self.props.setEnabled(enabled)
		self.titles.setEnabled(enabled)
		self.levels.setEnabled(enabled)
		self.stages.setEnabled(enabled)
		self.meta.setEnabled(enabled)
		self.images.setEnabled(enabled)

	# Shut up about my code
	def radioCheck(self, check, default = False):
		if check:
			if self.sender() == self.fullMod or default:
				# Set enabled after to avoid conflicts with other stateChanged callbacks
				self.allToDefaults()
			if self.sender() == self.onlyCharts:
				self.allToDefaults(False)

				self.charts.setEnabled(True)
				self.charts.setChecked(True)
				self.events.setChecked(True)
			if self.sender() == self.onlySongs:
				self.allToDefaults(False)

				self.songs.setEnabled(True)
				self.songs.setChecked(True)

				self.insts.setChecked(True)
				self.voices.setChecked(True)
				self.vocalsplit.setChecked(_vocalSplitEnabledByDefault)
				self.music.setChecked(True)
				self.sounds.setChecked(True)
			if self.sender() == self.onlyChars:
				self.allToDefaults(False)

				self.chars.setEnabled(True)
				self.chars.setChecked(True)

				self.icons.setChecked(True)
				self.jsons.setChecked(True)
				self.charassets.setChecked(True)
			if self.sender() == self.onlyStages:
				self.allToDefaults(False)

				self.stages.setEnabled(True)
				self.stages.setChecked(True)
			if self.sender() == self.iChoose:
				self.allToDefaults(True, True)
	
	def chartsEventsSection(self, state):
		if state == 2:  # Checked
			self.events.setEnabled(True)
		elif state == 0:  # Unchecked
			self.events.setEnabled(False)

	def songsSection(self, state):
		if state == 2:  # Checked
			self.insts.setEnabled(True)
			self.voices.setEnabled(True)
			self.vocalsplit.setEnabled(_vocalSplitEnabledByDefault)
			self.sounds.setEnabled(True)
			self.music.setEnabled(True)
		elif state == 0:  # Unchecked
			self.insts.setEnabled(False)
			self.voices.setEnabled(False)
			self.vocalsplit.setEnabled(False)
			self.sounds.setEnabled(False)
			self.music.setEnabled(False)

	def characterSection(self, state):
		if state == 2:  # Checked
			self.icons.setEnabled(True)
			self.jsons.setEnabled(True)
			self.charassets.setEnabled(True)
		elif state == 0:  # Unchecked
			self.icons.setEnabled(False)
			self.jsons.setEnabled(False)
			self.charassets.setEnabled(False)

	def weekSection(self, state):
		if state == 2:  # Checked
			self.props.setEnabled(True)
			self.titles.setEnabled(True)
			self.levels.setEnabled(True)
		elif state == 0:  # Unchecked
			self.props.setEnabled(False)
			self.titles.setEnabled(False)
			self.levels.setEnabled(False)

	def findMod(self):
		modFolder = QFileDialog.getExistingDirectory(self, "Select Mod Folder")
		self.modLineEdit.setText(modFolder)

	def findBaseGame(self):
		baseGameFolder = QFileDialog.getExistingDirectory(self, "Select Base Game Folder")
		self.baseGameLineEdit.setText(baseGameFolder)

	def convertCallback(self, what):
		# the code below should go on the callback when the person presses the convert button
		psych_mod_folder_path = self.modLineEdit.text()
		result_path = self.baseGameLineEdit.text()
		if Path(result_path).exists():	
			logging.warn(f'Folder {result_path} already existed before porting, files may have been overwritten.')
		options = Constants.DEFAULT_OPTIONS
		options['charts']['songs'] = self.charts.isChecked()
		if self.charts.isChecked():
			logging.info('Misc of charts will be converted')
			options['charts']['events'] = self.events.isChecked()
		if self.songs.isChecked():
			logging.info('Audio will be converted')
			options['songs']['inst'] = self.insts.isChecked()
			options['songs']['voices'] = self.voices.isChecked()
			options['songs']['split'] = self.vocalsplit.isChecked()
			options['songs']['music'] = self.music.isChecked()
			options['songs']['sounds'] = self.sounds.isChecked()
		if self.chars.isChecked():
			logging.info('Characters will be converted')
			options['characters']['json'] = self.jsons.isChecked()
			options['characters']['icons'] = self.icons.isChecked()
			options['characters']['assets'] = self.charassets.isChecked()
		if self.weeks.isChecked():
			logging.info('Weeks will be converted')
			options['weeks']['props'] = self.props.isChecked()
			options['weeks']['levels'] = self.levels.isChecked()
			options['weeks']['titles'] = self.titles.isChecked()	
		options['stages'] = self.stages.isChecked()
		options['modpack_meta'] = self.meta.isChecked()
		options['images'] = self.images.isChecked()

		try:
			optionsParsed = ''
			for key in options.keys():
				if type(options[key]) == bool:
					optionsParsed += '\n	' + key + ': ' + 'Yes' if options[key] else 'No'
				elif type(options[key]) == dict:
					optionsParsed += '\n	' + key + ':'
					for subkey in options[key].keys():
						optionsParsed += '\n		' + subkey + ': ' + 'Yes' if bool(options[key][subkey]) else 'No'

			# Now writing the last log file, which we can query to the user
			open(_defaultsFile, 'w').write(f'{psych_mod_folder_path}\n{result_path}\n\nLAST LOG: {log.logMemory.current_log_file}\n======================\nOPTIONS:{optionsParsed}')
		except Exception as e:
			logging.error(f'Problems with your save file: {e}')

		if psych_mod_folder_path != None and result_path != None:
			try:
				main.convert(psych_mod_folder_path, result_path, options)
			except Exception as e:
				self.throwError('Exception ocurred', f'{e}')
		else:
			logging.warn('Select an input folder or output folder first!')

	def goToIssues(self):
		webbrowser.open('https://github.com/gusborg88/fnf-porter/issues/new/choose')

	def goToGB(self):
		_GB_ToolID = '16982'
		webbrowser.open(f'https://gamebanana.com/tools/{_GB_ToolID}')

	def openLogFile(self):
		file = log.logMemory.current_log_file
		realLogPath = Path(file).resolve()
		print(realLogPath)
		logging.info(f'Attempting to open file: {realLogPath}')

		currentPlatform = platform.system()

		if currentPlatform == 'Windows':
			subprocess.Popen(['notepad.exe', str(realLogPath)])
		elif currentPlatform == 'Darwin':
			subprocess.Popen(['open', str(realLogPath)])

	def open_dialog(self, title, inputs, button, body):
		self.dialog = SimpleDialog(title, inputs, button, body)
		self.dialog.show()

		values = self.dialog.input_values
		self.dialog.hide()

		return values
	
	def throwError(self, text, actual_error_text):
		self.newError = ErrorMessage(text, actual_error_text, self)
		self.newError.show()

		# if the user does something, because exec is blocking call we close it!
		self.newError.hide()

	def prompt(self, inputs, title, body):
		button = 'Continue'
		return self.open_dialog(title=title, inputs=inputs, button=button, body=body)
	
window = Window()

def init():
	logging.info('Initiating window')

	# initiate the window
	try:
		window.show()
	except Exception as e:
		#why does this never fire
		logging.critical(f'Window could not show! {e}')
	
	#work in progress
	#Window.throwError(self=QDialog, text='d', actual_error_text='poooop')
	print('pooop')

	app.exec()

def prompt(prompt, body, inputs, file):
	# Simple prompt
	if prompt == 'input':

		title = f'[{file}] Requesting information'
		logging.info(title)

		return window.prompt(inputs, title, body) # 3 return calls, boy its just python
	
	# How to use this damn function:

	### window.prompt('input', 'Some text about the request', [['Some text about the purpose of this input', 'Placeholder (Gray text) on this input']], 'file.py')
