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
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel, QLineEdit, QPushButton, QFileDialog, QDialog, QVBoxLayout, QRadioButton, QTextBrowser

#the icon, in base64 (because its easier to compile)
icon = b64decode("iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAFVBMVEX/////3fv/fdtsPpT/LDdYtf8AKUvOkdnQAAAACXBIWXMAAC4jAAAuIwF4pT92AAABRUlEQVRIx73UQbLCIAwAUJzWvf03EC/gNBdgEfcuLDco9z/CB0JLgQDq/PlZ1clrkoZWIf4mTpcemLpg6oKpCy490BZTT5wm2QWyOWgf/Eh5bTUBC1oCQLqoN4HZA1sC7lx+oHwd3GQIC4ArIPe4fgnmKHgA8iC+AAPA3AOxxA24Pb8B5j1/bwJ75QAiqgzAlrdgREzFDoAAYiYGHmABgMCIRQlaFeUhjIDLsjzfB1ufDTwWime5D/eUW9oGcyqiCXzwYORBHCJuRZxDUtfAljcpULGA8cDUgLCp1RVY0yExTqrdzXpdPgVWjCo8hBUmA8KfLgagjS6AL+EQPaLhAPoyfk8mzKCSHvQWVUF4UcIqCLyUKAQtW9O6UYlcqHgYLDiepu2QA/p9jvlPAXXYwev4cSVBIv36sgj314Eo/wJ4If4nfgHb6rE0etNCVQAAAABJRU5ErkJggg==")
_windowTitleSuffix = "v0.1 [BETA]"
_defaultsFile = '.defaults'
_vocalSplitEnabledByDefault = False

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
		
class Window(QMainWindow):
	def closeEvent(self, event):
		logging.info('Thanks for using FNF Porter!')
		#time.sleep(0.1)
		event.accept()

	def __init__(self):
		super().__init__()

		self.setWindowTitle(f"FNF Porter {_windowTitleSuffix}")
		wid = 750
		hei = 650
		
		self.setFixedSize(QSize(wid, hei))
		self.setMinimumSize(QSize(wid, hei))
		self.setMaximumSize(QSize(wid, hei))
		
		pixmap = QPixmap()
		pixmap.loadFromData(icon)
		self.setWindowIcon(QIcon(pixmap))

		self.modLabel = 		QLabel("Path to your Psych Engine mod:", self)
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
		self.onlyCharts.setToolTip("A default option. Quick for fast and only chart converting.")

		self.onlySongs = QRadioButton('Only Audio', self)
		self.onlySongs.move(rX, 170)
		self.onlySongs.setToolTip("A default option. Quick for fast and only audio converting/copying.")

		self.onlyChars = QRadioButton('Only Characters', self) # not to be confused with onlyCharts
		self.onlyChars.move(rX, 200)
		self.onlyChars.resize(400, 30)
		self.onlyChars.setToolTip("A default option. Quick for fast and only character converting.")

		self.onlyStages = QRadioButton('Only Stages', self)
		self.onlyStages.move(rX, 230)
		self.onlyStages.setToolTip("A default option. Quick for fast and only stage converting.")

		self.fullMod = QRadioButton('Full Mod', self)
		self.fullMod.move(rX, 260)
		self.fullMod.setToolTip("A default option. Quick for converting the entire mod.")
		self.fullMod.setChecked(True) # Default

		self.iChoose = QRadioButton('Let me choose', self)
		self.iChoose.move(rX, 290)
		self.iChoose.setToolTip("Select this to customize your conversion experience.")

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
		self.helpButton.setToolTip('https://github.com/gusborg88/fnf-porter/issues/new')
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
		sSX = sX + 10

		self.optionsLabel = QLabel("Options", self)
		self.optionsLabel.move(sX, 100)
		self.optionsLabel.resize(220, 30)

		self.charts = QCheckBox("Charts", self)
		self.charts.move(sX, 140)
		self.charts.setToolTip("Select all charts in the \"/data/\" directory of your mod and convert them.")

		self.songs = QCheckBox("Songs", self)
		self.songs.move(sX, 170)
		self.songs.setToolTip("Select all songs in the \"/songs/\" directory of your mod and copy them.")

		self.songs.stateChanged.connect(self.songsSection)

		self.insts = QCheckBox("Instrumentals", self)
		self.insts.move(sSX, 190)
		self.insts.setToolTip("Copy over \"Inst.ogg\" files.")

		self.voices = QCheckBox("Voices", self)
		self.voices.move(sSX, 210)
		self.voices.setToolTip("Copy over \"Voices.ogg\" files.")

		# Is available just not for avoiding error :D
		self.vocalsplit = QCheckBox("Vocal Split", self)
		self.vocalsplit.move(sSX, 230)
		self.vocalsplit.setToolTip("Splits \"Voices.ogg\" files into two files (\"Voices-opponent.ogg\" and \"Voices-player.ogg\") using their charts. This requires ffmpeg in PATH, and Charts enabled.")

		self.chars = QCheckBox("Characters", self)
		self.chars.move(sX, 270)
		self.chars.setToolTip("Select all characters in the \"/characters/\" directory of your mod and convert them.")

		self.chars.stateChanged.connect(self.characterSection)

		self.icons = QCheckBox("Health Icons", self)
		self.icons.move(sSX, 290)
		self.icons.setToolTip("Copies over all of your character icon .png files from the \"/images/icons/\" directory of your mod. This also includes the Freeplay Icons.")

		self.jsons = QCheckBox(".json files", self)
		self.jsons.move(sSX, 310)
		self.jsons.setToolTip("Converts your character's .json files to the appropiate format.")

		self.charassets = QCheckBox("Assets", self)
		self.charassets.move(sSX, 330)
		self.charassets.setToolTip("Copies over your .png and .xml files from the \"/images/characters/\" directory of your mod.")

		self.weeks = QCheckBox("Weeks", self)
		self.weeks.move(sX, 370)
		self.weeks.setToolTip("Select week conversions.")

		self.weeks.stateChanged.connect(self.weekSection)

		self.props = QCheckBox("Menu Characters (Props)", self)
		self.props.move(sSX, 390)
		self.props.resize(400, 30)
		self.props.setToolTip("Converts your menu character .json files from the \"/images/menucharacters/\" directory of your mod to the appropiate format.")

		self.titles = QCheckBox("Week Images (Titles)", self)
		self.titles.move(sSX, 410)
		self.titles.resize(400, 30)
		self.titles.setToolTip("Copies over your .png files from the \"/images/storymenu/\" directory of your mod.")

		self.levels = QCheckBox("Levels", self)
		self.levels.move(sSX, 430)
		self.levels.setToolTip("Converts your week .json files from the \"/weeks/\" directory of your mod to the appropiate format.")

		self.stages = QCheckBox("Stages", self)
		self.stages.move(sX, 470)
		self.stages.setToolTip("Converts stage .jsons from the \"/stages/\" directory of your mod and parses the .lua files to asign props.")

		self.meta = QCheckBox("Pack Meta", self)
		self.meta.move(sX, 500)
		self.meta.setToolTip("Converts your \"pack.json\" to the appropiate format, and copies your \"pack.png\" file.")

		self.images = QCheckBox("Images", self)
		self.images.move(sX, 530)
		self.images.setToolTip("Copies over your .png and .xml files from the \"/images/\" directory of your mod.")

		self.convert = QPushButton("Convert", self)
		self.convert.move((self.width() - 20) - self.convert.width(), (self.height() - 20) - self.convert.height())
		self.convert.clicked.connect(self.convertCallback)

		self.radioCheck(True, True)

	def allToDefaults(self, checked = True, enabled = False):
		self.charts.setChecked(checked)
		self.songs.setChecked(checked)
		self.insts.setChecked(checked)
		self.voices.setChecked(checked)
		self.vocalsplit.setChecked(checked == _vocalSplitEnabledByDefault and checked != False)
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
		self.songs.setEnabled(enabled)
		self.insts.setEnabled(enabled)
		self.voices.setEnabled(enabled)
		self.vocalsplit.setEnabled(enabled)
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
			if self.sender() == self.onlySongs:
				self.allToDefaults(False)

				self.songs.setEnabled(True)
				self.songs.setChecked(True)

				self.insts.setChecked(True)
				self.voices.setChecked(True)
				self.vocalsplit.setChecked(_vocalSplitEnabledByDefault)
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

	def songsSection(self, state):
		if state == 2:  # Checked
			self.insts.setEnabled(True)
			self.voices.setEnabled(True)
			self.vocalsplit.setEnabled(_vocalSplitEnabledByDefault)
		elif state == 0:  # Unchecked
			self.insts.setEnabled(False)
			self.voices.setEnabled(False)
			self.vocalsplit.setEnabled(False)

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
			#i was trying to get this to be a window but it wasnt working
		options = Constants.DEFAULT_OPTIONS
		options['charts'] = self.charts.isChecked()
		if self.songs.isChecked():
			logging.info('Songs will be converted')
			options['songs']['inst'] = self.insts.isChecked()
			options['songs']['voices'] = self.voices.isChecked()
			options['songs']['split'] = self.vocalsplit.isChecked()
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
			# Now writing the last log file, which we can query to the user
			open(_defaultsFile, 'w').write(f'{psych_mod_folder_path}\n{result_path}\n{log.logMemory.current_log_file}')
		except Exception as e:
			logging.error(f'Problems with your save file: {e}')

		if psych_mod_folder_path != None and result_path != None:
			main.convert(psych_mod_folder_path, result_path, options)

	def goToIssues(self):
		#note this is a custom link that puts some things into the body, it should be the same as in readme.md
		webbrowser.open('https://github.com/gusborg88/fnf-porter/issues/new?body=Log+file+output+(check+logs+folder):%0A```%0A%0A```')

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
	
	def prompt(self, inputs, title, body):
		button = 'Continue'
		return self.open_dialog(title=title, inputs=inputs, button=button, body=body)

app = QApplication([])

window = Window()

def init():
	logging.info('Initiating window')

	# initiate the window
	window.show()

	app.exec()

def prompt(prompt, body, inputs, file):
	# Simple prompt
	if prompt == 'input':

		title = f'[{file}] Requesting information'
		logging.info(title)

		return window.prompt(inputs, title, body) # 3 return calls, boy its just python
	
	# How to use this damn function:

	### window.prompt('input', 'Some text about the request', [['Some text about the purpose of this input', 'Placeholder (Gray text) on this input']], 'file.py')
