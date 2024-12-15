import logging
import platform
import subprocess
import webbrowser
from base64 import b64decode
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtWidgets import (
	QApplication, QMainWindow, QDialog, QFileDialog,
	QHBoxLayout, QVBoxLayout, QGridLayout,
	QWidget, QLabel, QLineEdit, QTextBrowser,
	QRadioButton, QCheckBox, QPushButton, QGroupBox
)

import main
from . import log, Constants
from .data import GitHub

_windowTitleSuffix = f"- Build {GitHub.get_version()} [BETA]"
_defaultsFile = main.root.joinpath(".defaults")
_vocalSplitEnabledByDefault = platform.system() == 'Windows'

class WindowData:
	WIDTH = 750
	HEIGHT = 650

	APP_ICON = b64decode(Constants.BASE64_IMAGES.get('windowIcon'))
	icon:QIcon = None

	"""
		HOW TO USE:
		- name: Name for your preset (The thing that will appear in frontend)
		- options: The options it enables
		- disableAllOptions: Disables EVERY option (useful for presets where you want to disable everything) (True by default)
		- excludeSelected: Doesn't disable options inside of the options parameter (True by default)

		KEEP IN MIND: ENABLING AND CHECKING AN OPTION IS NOT THE SAME!!!
	"""
	PRESETS:dict[dict[str, str | bool | list[str]]] = {
		"charts": {
			"name": "Only Charts",
			"options": ["charts"],
		},
		"audio": {
			"name": "Only Audio",
			"options": ["audio"],
		},
		"characters": {
			"name": "Only Characters",
			"options": ["characters"],
		},
		"stages": {
			"name": "Only Stages",
			"options": ["stages"],
		},
		"all": {
			"name": "Full Mod",
			"options": ["*"],
			"excludeSelected": False
		},
		"custom": {
			"name": "Custom",
			"options": ["*"],
			"disableAllOptions": False
		}
	}

	@staticmethod
	def getIcon() -> QIcon:
		"""
		Method to get (or generate a new) app icon.
		"""

		if not WindowData.icon:
			iconMap = QPixmap()
			iconMap.loadFromData(WindowData.APP_ICON)
			WindowData.icon = QIcon(iconMap)

		return WindowData.icon

class DefaultWindow(QMainWindow):
	# Welcome to the jungle 💀

	def closeEvent(self, event):
		logging.info('Thanks for using FNF Porter!')
		#time.sleep(0.1)
		event.accept()

	def createOption(self, codename:str, name:str, items:list[str] = None) -> QGroupBox | QCheckBox:
		isGroup = items != None and len(items) > 0

		if isGroup:
			grp = QGroupBox(name)
			grp.setObjectName(codename)
			grp.setCheckable(True)

			_layout = QVBoxLayout()
			_layout.setSpacing(0)

			for item in items:
				itemWidget = QCheckBox(item)
				_layout.addWidget(itemWidget)

			grp.setLayout(_layout)
			return grp
		
		checkbox = QCheckBox(name)
		checkbox.setObjectName(codename)

		return checkbox

	def forceToggle(self, radio:str = "all"):
		for i in range(self.presets.count()):
			option = self.presets.itemAt(i).widget()

			if isinstance(option, QRadioButton) and option.objectName() == radio:
				option.setChecked(True)
				break

	def setPreset(self):
		sender = self.sender()

		# If there was an issue with getting the sender, we simply close the script to prevent crashes
		if not sender:
			return

		name = sender.objectName()

		preset = WindowData.PRESETS.get(name, {})
		options = preset.get("options", [])

		selectEverything = len(options) == 1 and options[0] == "*"
		disableAllOptions = preset.get("disableAllOptions", True)
		excludeSelected = preset.get("excludeSelected", True)

		for i in range(self.options.count()):
			option = self.options.itemAt(i).widget()

			exists = option.objectName() in options or selectEverything
			enabled = (exists and excludeSelected) or not disableAllOptions

			if isinstance(option, QGroupBox):
				option.setChecked(exists)
				option.setEnabled(enabled)

				for child in option.findChildren(QCheckBox):
					child.setChecked(exists)

			if isinstance(option, QCheckBox):
				option.setChecked(exists)
				option.setEnabled(enabled)

	def __init__(self):

		# First load save data

		modDP = ""
		bGDP = ""

		if _defaultsFile.exists():
			try:
				parse = _defaultsFile.read_text().split('\n')
				modDP = parse[0]
				bGDP = parse[1]

			except Exception as e:
				logging.warning(f"There was a problem with loading your save file! {type(e).__name__}: {e}")

		# INIT

		super().__init__()

		mainLayout = QVBoxLayout()

		# FOLDER BUTTONS

		inputBoxes = QGridLayout()

		modLabel = QLabel("Path to your Psych Engine mod:")
		baseGameLabel = QLabel("Path to Base Game mods folder:")

		modLineEdit = QLineEdit(modDP)
		baseGameLineEdit = QLineEdit(bGDP)
		
		findModButton = QPushButton("Locate...")
		findModButton.setToolTip("Open File Dialog")
		findModButton.clicked.connect(self.findMod)

		findBaseGameButton = QPushButton("Locate...")
		findBaseGameButton.setToolTip("Open File Dialog")
		findBaseGameButton.clicked.connect(self.findBaseGame)
		
		inputBoxes.addWidget(modLabel, 0, 0)
		inputBoxes.addWidget(modLineEdit, 0, 1)
		inputBoxes.addWidget(findModButton, 0, 2)

		inputBoxes.addWidget(baseGameLabel, 1, 0)
		inputBoxes.addWidget(baseGameLineEdit, 1, 1)
		inputBoxes.addWidget(findBaseGameButton, 1, 2)

		# THE MAIN BUTTONS

		section1 = QHBoxLayout()
		leftWidgets = QVBoxLayout()

		## PRESETS LAYOUT

		presets = QVBoxLayout()

		defaultsLabel = QLabel("Presets")
		presets.addWidget(defaultsLabel)
		presets.addSpacing(5)

		for name, preset in WindowData.PRESETS.items():
			presetWidget = QRadioButton(preset.get("name", "???"))
			presetWidget.setObjectName(name)
			presetWidget.toggled.connect(self.setPreset)
			presets.addWidget(presetWidget)

		## LOG LAYOUT

		gitPage = GitHub.page("issues/new/choose")
		gbPage = "https://gamebanana.com/tools/16982"

		logItems = QGridLayout()

		logsLabel = QTextBrowser()
		logsLabel.setMaximumHeight(270)

		ohioSkibidi = QPushButton("Open log file")
		ohioSkibidi.clicked.connect(log.open)

		helpButton = QPushButton("Report an issue")
		helpButton.setToolTip(gitPage)
		helpButton.clicked.connect(lambda: webbrowser.open(gitPage))

		gbButton = QPushButton("Gamebanana")
		gbButton.setToolTip(gbPage)
		gbButton.clicked.connect(lambda: webbrowser.open(gbPage))

		logItems.addWidget(ohioSkibidi, 0, 0)
		logItems.addWidget(helpButton, 0, 1)
		logItems.addWidget(gbButton, 0, 2)

		logItems.addWidget(logsLabel, 1, 0, 1, 3)

		## OPTIONS LAYOUT

		options = QVBoxLayout()
		options.setSpacing(5)

		optionsLabel = QLabel("Conversion Settings")
		options.addWidget(optionsLabel)

		### CHART settings

		options.addWidget(self.createOption("charts", "Charts", ["Events"]))

		### AUDIO settings

		options.addWidget(self.createOption("audio", "Audio", [
			"Instrumentals",
			"Voices",
			"Music",
			"Sounds",
			"Vocal Split"
		]))

		### CHARACTER settings

		options.addWidget(self.createOption("characters", "Characters", [
			"Health Icons",
			"Character Files ('.json')",
			"Character Assets ('.png', '.xml')"
		]))

		### WEEK settings

		options.addWidget(self.createOption("weeks", "Weeks", [
			"Menu Characters ('Props')",
			"Week Images ('Titles')",
			"Week Data ('Levels')"
		]))

		### OTHER settings

		options.addWidget(self.createOption("images", "Images"))
		options.addWidget(self.createOption("stages", "Stages"))
		options.addWidget(self.createOption("meta", "Pack Meta"))

		## Convert button

		convertSection = QHBoxLayout()
		convertSection.addStretch()

		convert = QPushButton("Convert")
		convertSection.addWidget(convert)

		# Layering everything properly

		presets.setAlignment(Qt.AlignmentFlag.AlignVCenter)

		leftWidgets.addLayout(presets)
		leftWidgets.addLayout(logItems)

		section1.addLayout(leftWidgets)
		section1.addLayout(options)

		mainLayout.addLayout(inputBoxes)
		mainLayout.addLayout(section1)
		mainLayout.addLayout(convertSection)

		mainLayout.setContentsMargins(20, 10, 20, 10)
		options.setContentsMargins(20, 0, 0, 0)

		centralWidget = QWidget(self)
		self.setCentralWidget(centralWidget)
		centralWidget.setLayout(mainLayout)

		# Default APP data

		self.presets = presets
		self.options = options

		self.baseGameLineEdit = baseGameLineEdit
		self.modLineEdit = modLineEdit
		self.logsLabel = logsLabel

		self.forceToggle()

		self.setWindowTitle(f"FNF Porter {_windowTitleSuffix}")
		self.setWindowIcon(WindowData.getIcon())
		self.setMaximumSize(QSize(1000, 720))
		self.resize(QSize(WindowData.WIDTH, WindowData.HEIGHT))

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
			for key in options:
				optionsParsed += f'\n	{key = }'

			# Now writing the last log file, which we can query to the user
			with _defaultsFile.open("w") as f:
				f.write(f'{psych_mod_folder_path}\n{result_path}\n\nLAST LOG: {log.getFile()}\n======================\nOPTIONS:{optionsParsed}')

		except Exception as e:
			logging.error(f'Problems with your save file: {e}')
			self.throwError(f'Problems on your save file! {e}')

		if psych_mod_folder_path != None and result_path != None:
			# try:
				main.convert(psych_mod_folder_path, result_path, options)
			# except Exception as e:
				# self.throwError('Exception ocurred', f'{e}')
				# This is kinda(?) unfinished
		else:
			logging.warn('Select an input folder or output folder first!')

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

		self.setWindowIcon(WindowData.getIcon())

		self.exec()

	def on_button_clicked(self):
		self.input_values = [input.text() for input in self.inputs]
		# print(self.input_values)

		self.close()

class ErrorMessage(QDialog):
	def __init__(self, text, actual_error_text, windowObject: DefaultWindow):
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
		self.openLog.clicked.connect(log.open)

		self.buttonContinue = QPushButton("I dont care", self)
		self.buttonContinue.clicked.connect(self.on_button_clicked)
		self.buttonContinue.move((widErr - (self.openLog.width() + self.buttonContinue.width())) - 20, (heiErr - self.buttonContinue.height()) - 20)

		self.exec()

	def on_button_clicked(self):
		self.close()

app = QApplication([])
window = DefaultWindow()

def init():
	logging.info('Initiating window')

	# initiate the window
	try:
		window.show()
	except Exception as e:
		logging.critical(f'Window could not show! {e}')

	app.exec()

def prompt(prompt, body, inputs, file):
	# Simple prompt
	if prompt == 'input':

		title = f'[{file}] Requesting information'
		logging.info(title)

		return window.prompt(inputs, title, body) # 3 return calls, boy its just python
	
	# How to use this damn function:

	### window.prompt('input', 'Some text about the request', [['Some text about the purpose of this input', 'Placeholder (Gray text) on this input']], 'file.py')
