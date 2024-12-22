import logging
import platform
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

class WindowUtil:
	"Utility class for managing `DefaultUtil`"

	WIDTH = 750
	HEIGHT = 650

	APP_ICON = b64decode(Constants.BASE64_IMAGES.get('windowIcon'))
	icon:QIcon = None

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
	"""
	HOW TO USE:
	- `name`: Name for your preset (The thing that will appear in frontend)
	- `options`: The options it enables
	- `disableAllOptions`: Disables EVERY option (useful for presets where you want to disable everything) (`True` by default)
	- `excludeSelected`: Doesn't disable options inside of the options parameter (`True` by default)

	KEEP IN MIND: ENABLING AND CHECKING AN OPTION IS NOT THE SAME!!!
	"""

	@staticmethod
	def getIcon() -> QIcon:
		"""
		Method to get (or generate a new) app icon.
		"""

		if not WindowUtil.icon:
			iconMap = QPixmap()
			iconMap.loadFromData(WindowUtil.APP_ICON)
			WindowUtil.icon = QIcon(iconMap)

		return WindowUtil.icon

	@staticmethod
	def getOptionData(obj: str | tuple) -> tuple:
		"""
		Packs all option data conveniently inside of a `tuple`.\n
		First item is option's label, the second item is the object name.\n
		In case this object is not a string or a tuple, it returns `None`
		"""

		if isinstance(obj, tuple):
			return obj
		if isinstance(obj, str):
			newTuple = (obj, obj.lower())
			return newTuple
		
		return None

class DefaultWindow(QMainWindow):
	# Welcome to the jungle 💀

	def closeEvent(self, event):
		logging.info('Thanks for using FNF Porter!')
		#time.sleep(0.1)
		event.accept()

	def getDirectory(self, foldertype:str, item:QLineEdit):
		path = QFileDialog.getExistingDirectory(self, f"Select {foldertype.capitalize()} Folder", item.text())

		if (len(path.strip()) > 0):
			item.setText(path)

	def generateOptionsMap(self) -> dict:
		"""
		Creates a map with all option data!
		"""

		options = {}

		for i in range(self.options.count()):
			option = self.options.itemAt(i).widget()
			objName = option.objectName().strip()

			if len(objName) < 1:
				continue

			if isinstance(option, QGroupBox):
				objData = {}

				for child in option.findChildren(QCheckBox):
					objData[child.objectName()] = option.isChecked() and child.isChecked()

				options[objName] = objData

			if isinstance(option, QCheckBox):
				options[objName] = option.isChecked()
		
		return options

	def createOption(self, name: str | tuple, items:list[str] = None) -> QGroupBox | QCheckBox:
		optData = WindowUtil.getOptionData(name)
		isGroup = items != None and len(items) > 0

		if optData == None:
			print("[!] Corrupt option data for", name)
			return

		optionLabel, objectName = optData

		if isGroup:
			grp = QGroupBox(optionLabel)
			grp.setObjectName(objectName)
			grp.setCheckable(True)

			_layout = QVBoxLayout()
			_layout.setSpacing(0)

			for item in items:
				subOptData = WindowUtil.getOptionData(item)

				if optData:
					subOptionLabel, subObjectName = subOptData
					itemWidget = QCheckBox(subOptionLabel)
					itemWidget.setObjectName(subObjectName)
					_layout.addWidget(itemWidget)
				else:
					print(f"[!] Corrupt option data for {subOptData} in group {optionLabel}")

			grp.setLayout(_layout)
			return grp
		
		checkbox = QCheckBox(optionLabel)
		checkbox.setObjectName(objectName)

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

		preset = WindowUtil.PRESETS.get(name, {})
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
		findModButton.clicked.connect(
			lambda: self.getDirectory("mod", modLineEdit)
		)

		findBaseGameButton = QPushButton("Locate...")
		findBaseGameButton.setToolTip("Open File Dialog")
		findBaseGameButton.clicked.connect(
			lambda: self.getDirectory("base game", baseGameLineEdit)
		)
		
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

		for name, preset in WindowUtil.PRESETS.items():
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

		options.addWidget(self.createOption("Charts", ["Notes", "Events"]))

		### AUDIO settings

		options.addWidget(self.createOption("Audio", [
			("Instrumentals", "inst"),
			"Voices",
			"Music",
			"Sounds",
			("Vocal Split", "split")
		]))

		### CHARACTER settings

		options.addWidget(self.createOption("Characters", [
			("Health Icons", "icons"),
			("Character Files ('.json')", "json"),
			("Character Assets ('.png', '.xml')", "assets")
		]))

		### WEEK settings

		options.addWidget(self.createOption("Weeks", [
			("Menu Characters ('Props')", "props"),
			("Week Images ('Titles')", "levels"),
			("Week Data ('Levels')", "titles")
		]))

		### OTHER settings

		options.addWidget(self.createOption("Images"))
		options.addWidget(self.createOption("Stages"))
		options.addWidget(self.createOption(("Pack Meta", "meta")))

		## Convert button

		convertSection = QHBoxLayout()
		convertSection.addStretch()

		convertButton = QPushButton("Convert")
		convertSection.addWidget(convertButton)

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

		self.convertButton = convertButton
		self.baseGameLineEdit = baseGameLineEdit
		self.modLineEdit = modLineEdit
		self.logsLabel = logsLabel

		self.forceToggle()

		self.setWindowTitle(f"FNF Porter {_windowTitleSuffix}")
		self.setWindowIcon(WindowUtil.getIcon())
		self.setMaximumSize(QSize(1000, 720))
		self.resize(QSize(WindowUtil.WIDTH, WindowUtil.HEIGHT))
	
	def addOnButtonEvent(self, handler):
		self.convertButton.clicked.connect(handler)

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

		self.setWindowIcon(WindowUtil.getIcon())

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

_isInit = False
_app = None

window = None

def init() -> QApplication:
	global _app, window, _isInit

	try:
		if _isInit:
			logging.warning("Window was already initialized!")
			return _app

		logger, console_handler = log.setup()
		logging.info('Initializing Window')

		_app = QApplication([])
		window = DefaultWindow()

		console_handler.logsLabel = window.logsLabel
		window.logsLabel.append("Welcome to FNF Porter!")

		window.show()

	except Exception as e:
		logging.critical(f'Unable to setup! {type(e).__name__}: {e}')

	else:
		_isInit = True
		return _app

def prompt(prompt, body, inputs, file):
	# Simple prompt
	if prompt == 'input':

		title = f'[{file}] Requesting information'
		logging.info(title)

		return window.prompt(inputs, title, body) # 3 return calls, boy its just python
	
	# How to use this damn function:

	### window.prompt('input', 'Some text about the request', [['Some text about the purpose of this input', 'Placeholder (Gray text) on this input']], 'file.py')
