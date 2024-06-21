


import json
import logging
import main
import platform
import subprocess
import webbrowser

from . import log, Constants
from base64 import b64decode
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt6.QtWidgets import *

import src.tools.VocalSplit as VocalSplit

icon = b64decode(Constants.BASE64_IMAGES.get('windowIcon'))

_windowTitleSuffix = f"v{Constants.VERSION} [ultra alpha based version 1]"
_defaultsFile = '.defaults'
_vocalSplitEnabledByDefault = platform.system() == 'Windows'

app = QApplication([])


class BaseUI():
	def __init__(self, targetWindow:QMainWindow):
		super().__init__()

		self.senderWindow = targetWindow

		self.homeButton = QPushButton('<|== Back', targetWindow)
		self.homeButton.move(5, 5)

		def goToHome():
			targetWindow.goToState('home')

		self.homeButton.clicked.connect(goToHome)

		self.widgetsList = [self.homeButton]

		self.stateId = None

	def showAll(self):
		for widget in self.widgetsList:
			try:
				widget.show()
			except Exception as e:
				logging.error(f'Could not show UI element!: {e}')

	def hideAll(self):
		for widget in self.widgetsList:
			try:
				widget.hide()
			except Exception as e:
				logging.error(f'Could not hide UI element!: {e}')

class VocalSplitUI(BaseUI):
	def __init__(self, targetWindow:QMainWindow):
		super().__init__(targetWindow)

		self.stateId = 'vocalsplit'

		self.featureName = QLabel(f'Vocal Split', targetWindow)
		self.featureName.resize(100, 30)

		elementsY = 50

		self.featureName.move(20, elementsY)

		elementsY += 40

		self.vocsLabel = QLabel("Vocals", targetWindow)
		self.vocsLabel.resize(220, 30)

		self.findVoc = QPushButton("Locate...", targetWindow)
		self.findVoc.setToolTip("Open File Dialog")
		self.vocLineEdit = QLineEdit('', targetWindow)
		self.chartLineEdit = QLineEdit('', targetWindow)

		def findVocsOFD():
			vocalsOgg = QFileDialog.getOpenFileName(self.senderWindow, "Select Vocals .OGG", filter="*.ogg")
			if len(vocalsOgg[0]) > 0:
				self.vocLineEdit.setText(vocalsOgg[0])

		self.supportedChartFormats = [
			'Legacy FNF',
			'Funkin\' 0.4.1'
		]

		self.findVoc.clicked.connect(findVocsOFD)

		#elementsY += 30

		#elementsY += 40

		self.vocsLabel.move(20, elementsY)
		self.findVoc.move((targetWindow.width() - 20) - self.findVoc.width(), elementsY)
		self.vocLineEdit.move((self.findVoc.x() - 20) - 400, elementsY)

		self.vocLineEdit.resize(400, 30)
		self.chartLineEdit.resize(400, 30)

		elementsY += 40

		self.chartFormatLabel = QLabel("Chart", targetWindow)
		self.chartFormatLabel.move(20, elementsY)

		self.findChart = QPushButton("Locate...", targetWindow)
		self.findChart.move((targetWindow.width() - 20) - self.findChart.width(), elementsY)

		self.chartLineEdit.move((self.findChart.x() - 20) - 400, elementsY)

		def findChartLocation():
			chartFile = QFileDialog.getOpenFileName(self.senderWindow, "Select Chart File", filter="*.json")
			if len(chartFile[0]) > 0:
				self.chartLineEdit.setText(chartFile[0])

		self.findChart.clicked.connect(findChartLocation)

		elementsY += 40

		self.chartFormatDropdown = QComboBox(targetWindow)
		self.chartFormatDropdown.addItems(self.supportedChartFormats)
		dropDownX = int((targetWindow.width() - 20) - self.findVoc.width())
		self.chartFormatDropdown.move(dropDownX, elementsY)

		def startVocalSplit():
			try:
				resultPath = Path(self.vocLineEdit.text()).parent

				if self.chartFormatDropdown.currentIndex() == 0:
					chartFile = json.loads(open(self.chartLineEdit.text(), 'r').read())['song']

					chartBPM = chartFile['bpm']
					sections = chartFile['notes']

					songName = chartFile['song']

					VocalSplit.vocalsplit(
						chart=sections,
						bpm=chartBPM,
						origin=self.vocLineEdit.text(),
						path=f'{resultPath}/',
						key=songName,
						characters=[chartFile['player1'], chartFile['player2']],
						ignoreOgg=True
					)
				elif self.chartFormatDropdown.currentIndex() == 1: ## I DO NOT KNOW IF THIS WORKS. I hope it does
					metadataFile = QFileDialog.getOpenFileName(self.senderWindow, "Select Metadata File", filter="*.json")
					if len(metadataFile[0]) > 0:
						metaFile = metadataFile[0]

						metadata = json.loads(open(metaFile, 'r').read())
						chartFile = json.loads(open(self.chartLineEdit.text(), 'r').read())

						chartBPM = metadata['timeChanges'][0]['bpm']

						def parseSections(focusCameraEvents):
							returner = []

							timeLastValid = 0

							for event in focusCameraEvents:
								time = event['t']

								if event['e'] != 'FocusCamera':
									continue

								stepCrochet = ((60 / chartBPM) * 1000) / 4
								stepsItTook = round((time - timeLastValid) / stepCrochet)
								isEventMustHitNew = type(event['v']) == dict

								#print(isEventMustHitNew, mustHitEvent)

								isMustHitForBF = False

								if isEventMustHitNew:
									isMustHitForBF = event['v']['char'] == 1
								else:
									isMustHitForBF = event['v'] == 1

								returner.append({
									'mustHitSection': isMustHitForBF,
									'lengthInSteps': stepsItTook
								})

								timeLastValid = time

							return returner
													
						sections = parseSections(chartFile['events'])

						songName = metadata['songName']

						VocalSplit.vocalsplit(
							chart=sections,
							bpm=chartBPM,
							origin=self.vocLineEdit.text(),
							path=f'{resultPath}/',
							key=songName,
							characters=[metadata['playData']['characters']['player'], metadata['playData']['characters']['opponent']],
							ignoreOgg=True
						)
					else:
						raise Exception('No metadata file provided, cannot continue generating legacy chart format!')
				else:
					raise Exception(f'Unsupported Chart Format for Vocal Split: {self.chartFormatDropdown.currentIndex()}')
			except Exception as e:
				logging.error(f'Failed to perform vocal split operation', exc_info=e)

		self.convert = QPushButton("Start", targetWindow)
		self.convert.move((targetWindow.width() - 20) - self.convert.width(), (targetWindow.logsLabel.y() - 20) - self.convert.height())
		self.convert.clicked.connect(startVocalSplit)

		self.widgetsList += [
			self.featureName,
			self.vocsLabel,
			self.findVoc,
			self.vocLineEdit,
			self.chartLineEdit,
			self.findChart,
			self.chartFormatLabel,
			self.chartFormatDropdown,
			self.convert
		]

class HomePageUI(BaseUI):
	def __init__(self, targetWindow:QMainWindow):
		super().__init__(targetWindow)

		self.stateId = 'home'

		# Remove the back button, since this is the home page
		self.homeButton.hide()
		self.widgetsList.remove(self.homeButton)

		self.engineDropdownFrom = QComboBox(targetWindow)
		self.engineDropdownTo = QComboBox(targetWindow)
		self.toLabel = QLabel('to', targetWindow)

		groupOptionsY = 100

		leftButtonX = int((targetWindow.width() / 2) - (self.engineDropdownFrom.width() + 50))
		rightButtonX = int((targetWindow.width() / 2) + 50)
		toX = int((targetWindow.width() / 2) - 8)
		buttonX = int((targetWindow.width() / 2) - 100)

		self.engineDropdownFrom.move(leftButtonX, groupOptionsY)
		self.engineDropdownTo.move(rightButtonX, groupOptionsY)
		self.toLabel.move(toX, groupOptionsY)

		self.supportedConversions = [
			('Psych Engine', 'Base Game'),
			#('Base Game', 'Psych Engine')
		]

		for engineFrom, engineTo in self.supportedConversions:
			self.engineDropdownFrom.addItem(engineFrom)
			self.engineDropdownTo.addItem(engineTo)

		self.engineDropdownFrom.currentIndexChanged.connect(self.dropdownChanged)
		self.engineDropdownTo.currentIndexChanged.connect(self.dropdownChanged)

		self.loadUi = QPushButton('Convert', targetWindow)
		self.loadUi.resize(200, 30)
		self.loadUi.move(buttonX, groupOptionsY + 50)

		self.appName = QLabel(f'FNF Porter {_windowTitleSuffix}', targetWindow)
		self.appName.resize(300, 30)
		self.appName.move(20, 20)
		self.discordButton = QPushButton('Discord', targetWindow)
		self.discordButton.move((targetWindow.width() - 20) - self.discordButton.width(), 20)

		def goToVocalSplit():
			targetWindow.goToState('vocalsplit')

		self.vocalSplitButton = QPushButton('Vocal Split', targetWindow)
		self.vocalSplitButton.move(20, (targetWindow.logsLabel.y() - 20) - self.vocalSplitButton.height())
		self.vocalSplitButton.clicked.connect(goToVocalSplit)

		def openDiscord():
			webbrowser.open('https://discord.gg/3nqMvtCsJJ')

		def onStateClicked():
			indexFrom = self.engineDropdownFrom.currentIndex()
			indexTo = self.engineDropdownTo.currentIndex()
			stateTuple = (self.supportedConversions[indexFrom][0], self.supportedConversions[indexTo][1])

			targetWindow.goToStateWithConversionTuple(stateTuple)

		self.loadUi.clicked.connect(onStateClicked)
		self.discordButton.clicked.connect(openDiscord)

		self.dropdownChanged()

		self.widgetsList += [
			self.engineDropdownFrom,
			self.engineDropdownTo,
			self.loadUi,
			self.toLabel,
			self.appName,
			self.discordButton,
			self.vocalSplitButton
		]

	def dropdownChanged(self):
		indexF = self.engineDropdownFrom.currentIndex()
		indexT = self.engineDropdownTo.currentIndex()

		isCompatible = self.isConversionCompatible(indexF, indexT)
		self.loadUi.setEnabled(isCompatible)
		self.loadUi.setText('Convert' if isCompatible else 'Not supported')

	def isConversionCompatible(self, indexFrom, indexTo):
		tupleToCompareFrom = (self.supportedConversions[indexFrom][0], self.supportedConversions[indexTo][1])
		#print(tupleToCompareFrom)
		return tupleToCompareFrom in self.supportedConversions
	
class ConversionUI(BaseUI):
	def __init__(self, targetWindow:QMainWindow):
		super().__init__(targetWindow)

		self.stateId = 'default_conversion_ui'

		## Section 2, Help

		buttonsHeight = 30
		buttonsWidth = 100
		buttonsY = (targetWindow.logsLabel.y() - 20) - buttonsHeight

		self.ohioSkibidi = QPushButton("Open log file", targetWindow)
		self.ohioSkibidi.move(20, buttonsY)
		self.ohioSkibidi.resize(buttonsWidth, buttonsHeight)
		self.ohioSkibidi.clicked.connect(targetWindow.openLogFile)

		self.helpButton = QPushButton("Report an issue", targetWindow)
		self.helpButton.setToolTip('https://github.com/gusborg88/fnf-porter/issues/new/choose/')
		self.helpButton.move(130, buttonsY)
		self.helpButton.resize(buttonsWidth, buttonsHeight)
		self.helpButton.clicked.connect(self.goToIssues)

		self.gbButton = QPushButton("GameBanana", targetWindow)
		self.gbButton.setToolTip(f'https://gamebanana.com/tools/{Constants.GAME_BANANA_TOOL}')
		self.gbButton.move(240, buttonsY)
		self.gbButton.resize(buttonsWidth, buttonsHeight)
		self.gbButton.clicked.connect(self.goToGB)

	def goToIssues(self):
		webbrowser.open('https://github.com/gusborg88/fnf-porter/issues/new/choose')

	def goToGB(self):
		webbrowser.open(f'https://gamebanana.com/tools/{Constants.GAME_BANANA_TOOL}')
				
class PsychToBaseUI(ConversionUI):
	def __init__(self, targetWindow:QMainWindow):
		super().__init__(targetWindow)

		self.stateId = 'psych2base'

		modLineY = 50
		baseLineY = modLineY + 40

		self.modLabel = QLabel("Path to your Psych Engine mod:", targetWindow)
		self.baseGameLabel = 	QLabel("Path to Base Game mods folder:", targetWindow)
		self.modLabel.move(20, modLineY)
		self.modLabel.resize(220, 30)
		self.baseGameLabel.move(20, baseLineY)
		self.baseGameLabel.resize(220, 30)

		self.findModButton = QPushButton("Locate...", targetWindow)
		self.findBaseGameButton = QPushButton("Locate...", targetWindow)
		self.findModButton.setToolTip("Open File Dialog")
		self.findBaseGameButton.setToolTip("Open File Dialog")
		self.findModButton.move((targetWindow.width() - 20) - self.findModButton.width(), modLineY)
		self.findBaseGameButton.move((targetWindow.width() - 20) - self.findBaseGameButton.width(), baseLineY)  # Move the button closer to the other one
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

		self.modLineEdit = QLineEdit(modDP, targetWindow)
		self.baseGameLineEdit = QLineEdit(bGDP, targetWindow)
		self.modLineEdit.move((self.findModButton.x() - 20) - 400, modLineY)
		self.baseGameLineEdit.move((self.findBaseGameButton.x() - 20) - 400, baseLineY)
		self.modLineEdit.resize(400, 30)  # Adjust the size as needed
		self.baseGameLineEdit.resize(400, 30)  # Adjust the size as needed

		## Section 1, PRESETS
		rX = 20

		thingsY = baseLineY + 40

		self.defaultsLabel = QLabel("Presets", targetWindow)
		self.defaultsLabel.move(rX, thingsY)
		self.defaultsLabel.resize(220, 30)

		thingsY += 30

		self.onlyCharts = QRadioButton('Only Charts', targetWindow)
		self.onlyCharts.move(rX, thingsY)

		thingsY += 30

		self.onlySongs = QRadioButton('Only Audio', targetWindow)
		self.onlySongs.move(rX, thingsY)

		thingsY += 30

		self.onlyChars = QRadioButton('Only Characters', targetWindow) # not to be confused with onlyCharts
		self.onlyChars.move(rX, thingsY)
		self.onlyChars.resize(400, 30)

		thingsY += 30

		self.onlyStages = QRadioButton('Only Stages', targetWindow)
		self.onlyStages.move(rX, thingsY)

		thingsY += 30

		self.fullMod = QRadioButton('Full Mod', targetWindow)
		self.fullMod.move(rX, thingsY)
		self.fullMod.setChecked(True) # Default

		thingsY += 30

		self.iChoose = QRadioButton('Custom', targetWindow)
		self.iChoose.move(rX, thingsY)

		self.onlyCharts.toggled.connect(self.radioCheck)
		self.onlySongs.toggled.connect(self.radioCheck)
		self.onlyChars.toggled.connect(self.radioCheck)
		self.onlyStages.toggled.connect(self.radioCheck)
		self.fullMod.toggled.connect(self.radioCheck)
		self.iChoose.toggled.connect(self.radioCheck)

		## Section 2, Help

		## Section 3, Options
		sX = int(targetWindow.width() / 2)

		_catItemLeftSpacing = 15 # Categorized group padding-left.

		sSX = sX + _catItemLeftSpacing

		_newCheckbox = 20 # A checkbox, categorized or not.
		_newCheckboxInCat = 20 # A checkbox inside a categorized group.
		_newCheckboxAfterCat = 30 # A checkbox after a categorized group of checkboxes.
		_spacingBelowLabel = 40 # A checkbox below a label.
		_defaultYPos = baseLineY + 40

		_currentYPos = _defaultYPos

		self.optionsLabel = QLabel("Options", targetWindow)
		self.optionsLabel.move(sX, _currentYPos)
		self.optionsLabel.resize(220, 30)

		_currentYPos += _spacingBelowLabel

		self.charts = QCheckBox("Charts", targetWindow)
		self.charts.move(sX, _currentYPos)
		self.charts.setToolTip("Select all charts in the \"/data/\" directory of your mod and convert them.")

		self.charts.stateChanged.connect(self.chartsEventsSection)

		_currentYPos += _newCheckboxInCat

		self.events = QCheckBox("Events", targetWindow)
		self.events.move(sSX, _currentYPos)
		self.events.setToolTip("Adds minimal support for events: \"Play Animation\", \"Alt Animation\" notes and \"Change Character\" (Creates a module file at the root of your mod).")

		_currentYPos += _newCheckboxAfterCat

		self.songs = QCheckBox("Audio", targetWindow)
		self.songs.move(sX, _currentYPos)
		self.songs.setToolTip("Select audio in different directories of your mod and copy them.")

		self.songs.stateChanged.connect(self.songsSection)

		_currentYPos += _newCheckboxInCat

		self.insts = QCheckBox("Instrumentals", targetWindow)
		self.insts.move(sSX, _currentYPos)
		self.insts.setToolTip("Copy over \"Inst.ogg\" files.")

		_currentYPos += _newCheckboxInCat

		self.voices = QCheckBox("Voices", targetWindow)
		self.voices.move(sSX, _currentYPos)
		self.voices.setToolTip("Copy over \"Voices.ogg\" files.")

		_currentYPos += _newCheckboxInCat

		self.music = QCheckBox("Music", targetWindow)
		self.music.move(sSX, _currentYPos)
		self.music.setToolTip("Copies over files in the \"music\" directory of your mod.")

		_currentYPos += _newCheckboxInCat

		self.sounds = QCheckBox("Sounds", targetWindow)
		self.sounds.move(sSX, _currentYPos)
		self.sounds.setToolTip("Copies over files and folders in the \"sounds\" directory of your mod.")
		
		_currentYPos += _newCheckboxInCat

		# Is available just not for avoiding error :D
		self.vocalsplit = QCheckBox("Vocal Split", targetWindow)
		self.vocalsplit.move(sSX, _currentYPos)
		self.vocalsplit.setToolTip("Splits \"Voices.ogg\" files into two files (\"Voices-opponent.ogg\" and \"Voices-player.ogg\") using their charts. This requires ffmpeg in PATH, and Charts enabled.")

		_currentYPos += _newCheckboxAfterCat

		self.chars = QCheckBox("Characters", targetWindow)
		self.chars.move(sX, _currentYPos)
		self.chars.setToolTip("Select all characters in the \"/characters/\" directory of your mod and convert them.")

		self.chars.stateChanged.connect(self.characterSection)

		_currentYPos += _newCheckboxInCat

		self.icons = QCheckBox("Health Icons", targetWindow)
		self.icons.move(sSX, _currentYPos)
		self.icons.setToolTip("Copies over all of your character icon .png files from the \"/images/icons/\" directory of your mod. This also generates Freeplay Icons (These require characters enabled).")

		_currentYPos += _newCheckboxInCat

		self.jsons = QCheckBox(".json files", targetWindow)
		self.jsons.move(sSX, _currentYPos)
		self.jsons.setToolTip("Converts your character's .json files to the appropiate format.")

		_currentYPos += _newCheckboxInCat

		self.charassets = QCheckBox("Assets", targetWindow)
		self.charassets.move(sSX, _currentYPos)
		self.charassets.setToolTip("Copies over your .png and .xml files from the \"/images/characters/\" directory of your mod.")

		_currentYPos = _defaultYPos
		_currentYPos += _spacingBelowLabel

		sX += 150
		sSX = sX + _catItemLeftSpacing

		self.weeks = QCheckBox("Weeks", targetWindow)
		self.weeks.move(sX, _currentYPos)
		self.weeks.setToolTip("Select week conversions.")

		self.weeks.stateChanged.connect(self.weekSection)

		_currentYPos += _newCheckboxInCat

		self.props = QCheckBox("Menu Characters (Props)", targetWindow)
		self.props.move(sSX, _currentYPos)
		self.props.resize(400, 30)
		self.props.setToolTip("Converts your menu character .json files from the \"/images/menucharacters/\" directory of your mod to the appropiate format.")

		_currentYPos += _newCheckboxInCat

		self.titles = QCheckBox("Week Images (Titles)", targetWindow)
		self.titles.move(sSX, _currentYPos)
		self.titles.resize(400, 30)
		self.titles.setToolTip("Copies over your .png files from the \"/images/storymenu/\" directory of your mod.")

		_currentYPos += _newCheckboxInCat

		self.levels = QCheckBox("Levels", targetWindow)
		self.levels.move(sSX, _currentYPos)
		self.levels.setToolTip("Converts your week .json files from the \"/weeks/\" directory of your mod to the appropiate format.")

		_currentYPos += _newCheckboxAfterCat

		self.stages = QCheckBox("Stages", targetWindow)
		self.stages.move(sX, _currentYPos)
		self.stages.setToolTip("Converts stage .jsons from the \"/stages/\" directory of your mod and parses the .lua files to asign props.")

		_currentYPos += _newCheckbox

		self.meta = QCheckBox("Pack Meta", targetWindow)
		self.meta.move(sX, _currentYPos)
		self.meta.setToolTip("Converts your \"pack.json\" to the appropiate format, and copies your \"pack.png\" file.")

		_currentYPos += _newCheckbox

		self.images = QCheckBox("Images", targetWindow)
		self.images.move(sX, _currentYPos)
		self.images.setToolTip("Copies over your .png and .xml files from the \"/images/\" directory of your mod.")

		self.convert = QPushButton("Convert", targetWindow)
		self.convert.move((targetWindow.width() - 20) - self.convert.width(), (targetWindow.logsLabel.y() - 20) - self.convert.height())
		self.convert.clicked.connect(self.convertCallback)

		self.radioCheck(True, True)

		self.widgetsList += [
			self.modLabel,
			self.baseGameLabel,
			self.findModButton,
			self.findBaseGameButton,
			self.modLineEdit,
			self.baseGameLineEdit,
			self.defaultsLabel,
			self.onlyChars,
			self.onlySongs,
			self.onlyChars,
			self.onlyCharts,
			self.onlyStages,
			self.fullMod,
			self.iChoose,
			self.ohioSkibidi,
			self.helpButton,
			self.gbButton,
			self.optionsLabel,
			self.charts,
			self.events,
			self.songs,
			self.insts,
			self.voices,
			self.music,
			self.sounds,
			self.vocalsplit,
			self.chars,
			self.icons,
			self.jsons,
			self.charassets,
			self.weeks,
			self.props,
			self.titles,
			self.levels,
			self.stages,
			self.meta,
			self.images,
			self.convert
		]

		#self.hideAll()

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
		sender = self.senderWindow.sender()
		if check:
			if sender == self.fullMod or default:
				# Set enabled after to avoid conflicts with other stateChanged callbacks
				self.allToDefaults()
			if sender == self.onlyCharts:
				self.allToDefaults(False)

				self.charts.setEnabled(True)
				self.charts.setChecked(True)
				self.events.setChecked(True)
			if sender == self.onlySongs:
				self.allToDefaults(False)

				self.songs.setEnabled(True)
				self.songs.setChecked(True)

				self.insts.setChecked(True)
				self.voices.setChecked(True)
				self.vocalsplit.setChecked(_vocalSplitEnabledByDefault)
				self.music.setChecked(True)
				self.sounds.setChecked(True)
			if sender == self.onlyChars:
				self.allToDefaults(False)

				self.chars.setEnabled(True)
				self.chars.setChecked(True)

				self.icons.setChecked(True)
				self.jsons.setChecked(True)
				self.charassets.setChecked(True)
			if sender == self.onlyStages:
				self.allToDefaults(False)

				self.stages.setEnabled(True)
				self.stages.setChecked(True)
			if sender == self.iChoose:
				self.allToDefaults(True, True)
	
	def chartsEventsSection(self, state):
		self.events.setEnabled(state == 2)

	def songsSection(self, state):
		self.insts.setEnabled(state == 2)
		self.voices.setEnabled(state == 2)
		self.vocalsplit.setEnabled(_vocalSplitEnabledByDefault and state == 2)
		self.sounds.setEnabled(state == 2)
		self.music.setEnabled(state == 2)

	def characterSection(self, state):
		self.icons.setEnabled(state == 2)
		self.jsons.setEnabled(state == 2)
		self.charassets.setEnabled(state == 2)

	def weekSection(self, state):
		self.props.setEnabled(state == 2)
		self.titles.setEnabled(state == 2)
		self.levels.setEnabled(state == 2)

	def findMod(self):
		modFolder = QFileDialog.getExistingDirectory(self.senderWindow, "Select Mod Folder")
		self.modLineEdit.setText(modFolder)

	def findBaseGame(self):
		baseGameFolder = QFileDialog.getExistingDirectory(self.senderWindow, "Select Base Game Folder")
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
			open(_defaultsFile, 'w').write(f'{psych_mod_folder_path}\n{result_path}\n\nLAST LOG: {log.logMemory.current_log_file}\n======================\nOPTIONS:{optionsParsed}')
		except Exception as e:
			logging.error(f'Problems with your save file: {e}')
			self.senderWindow.throwError(f'Problems on your save file! {e}')

		if psych_mod_folder_path != None and result_path != None:
			# try:
			main.convert(psych_mod_folder_path, result_path, options)
			# except Exception as e:
				# self.throwError('Exception ocurred', f'{e}')
				# This is kinda(?) unfinished
		else:
			logging.warn('Select an input folder or output folder first!')

class BaseToPsychUI(ConversionUI):
	def __init__(self, targetWindow:QMainWindow):
		super().__init__(targetWindow)

		self.stateId = 'psych2base'

		modLineY = 50
		baseLineY = modLineY + 40

		self.modLabel = QLabel("Path to your Psych Engine mod:", targetWindow)
		self.baseGameLabel = 	QLabel("Path to Base Game mods folder:", targetWindow)
		self.modLabel.move(20, modLineY)
		self.modLabel.resize(220, 30)
		self.baseGameLabel.move(20, baseLineY)
		self.baseGameLabel.resize(220, 30)

		self.findModButton = QPushButton("Locate...", targetWindow)
		self.findBaseGameButton = QPushButton("Locate...", targetWindow)
		self.findModButton.setToolTip("Open File Dialog")
		self.findBaseGameButton.setToolTip("Open File Dialog")
		self.findModButton.move((targetWindow.width() - 20) - self.findModButton.width(), modLineY)
		self.findBaseGameButton.move((targetWindow.width() - 20) - self.findBaseGameButton.width(), baseLineY)  # Move the button closer to the other one
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

		self.modLineEdit = QLineEdit(modDP, targetWindow)
		self.baseGameLineEdit = QLineEdit(bGDP, targetWindow)
		self.modLineEdit.move((self.findModButton.x() - 20) - 400, modLineY)
		self.baseGameLineEdit.move((self.findBaseGameButton.x() - 20) - 400, baseLineY)
		self.modLineEdit.resize(400, 30)  # Adjust the size as needed
		self.baseGameLineEdit.resize(400, 30)  # Adjust the size as needed

		## Section 1, PRESETS
		rX = 20

		thingsY = baseLineY + 40

		self.defaultsLabel = QLabel("Presets", targetWindow)
		self.defaultsLabel.move(rX, thingsY)
		self.defaultsLabel.resize(220, 30)

		thingsY += 30

		self.onlyCharts = QRadioButton('Only Charts', targetWindow)
		self.onlyCharts.move(rX, thingsY)

		thingsY += 30

		self.onlySongs = QRadioButton('Only Audio', targetWindow)
		self.onlySongs.move(rX, thingsY)

		thingsY += 30

		self.onlyChars = QRadioButton('Only Characters', targetWindow) # not to be confused with onlyCharts
		self.onlyChars.move(rX, thingsY)
		self.onlyChars.resize(400, 30)

		thingsY += 30

		self.onlyStages = QRadioButton('Only Stages', targetWindow)
		self.onlyStages.move(rX, thingsY)

		thingsY += 30

		self.fullMod = QRadioButton('Full Mod', targetWindow)
		self.fullMod.move(rX, thingsY)
		self.fullMod.setChecked(True) # Default

		thingsY += 30

		self.iChoose = QRadioButton('Custom', targetWindow)
		self.iChoose.move(rX, thingsY)

		self.onlyCharts.toggled.connect(self.radioCheck)
		self.onlySongs.toggled.connect(self.radioCheck)
		self.onlyChars.toggled.connect(self.radioCheck)
		self.onlyStages.toggled.connect(self.radioCheck)
		self.fullMod.toggled.connect(self.radioCheck)
		self.iChoose.toggled.connect(self.radioCheck)

		## Section 3, Options
		sX = int(targetWindow.width() / 2)

		_catItemLeftSpacing = 15 # Categorized group padding-left.

		sSX = sX + _catItemLeftSpacing

		_newCheckbox = 20 # A checkbox, categorized or not.
		_newCheckboxInCat = 20 # A checkbox inside a categorized group.
		_newCheckboxAfterCat = 30 # A checkbox after a categorized group of checkboxes.
		_spacingBelowLabel = 40 # A checkbox below a label.
		_defaultYPos = baseLineY + 40

		_currentYPos = _defaultYPos

		self.optionsLabel = QLabel("Options", targetWindow)
		self.optionsLabel.move(sX, _currentYPos)
		self.optionsLabel.resize(220, 30)

		_currentYPos += _spacingBelowLabel

		self.charts = QCheckBox("Charts", targetWindow)
		self.charts.move(sX, _currentYPos)
		self.charts.setToolTip("Select all charts in the \"/data/\" directory of your mod and convert them.")

		self.charts.stateChanged.connect(self.chartsEventsSection)

		_currentYPos += _newCheckboxInCat

		self.events = QCheckBox("Events", targetWindow)
		self.events.move(sSX, _currentYPos)
		self.events.setToolTip("Adds minimal support for events: \"Play Animation\", \"Alt Animation\" notes and \"Change Character\" (Creates a module file at the root of your mod).")

		_currentYPos += _newCheckboxAfterCat

		self.songs = QCheckBox("Audio", targetWindow)
		self.songs.move(sX, _currentYPos)
		self.songs.setToolTip("Select audio in different directories of your mod and copy them.")

		self.songs.stateChanged.connect(self.songsSection)

		_currentYPos += _newCheckboxInCat

		self.insts = QCheckBox("Instrumentals", targetWindow)
		self.insts.move(sSX, _currentYPos)
		self.insts.setToolTip("Copy over \"Inst.ogg\" files.")

		_currentYPos += _newCheckboxInCat

		self.voices = QCheckBox("Voices", targetWindow)
		self.voices.move(sSX, _currentYPos)
		self.voices.setToolTip("Copy over \"Voices.ogg\" files.")

		_currentYPos += _newCheckboxInCat

		self.music = QCheckBox("Music", targetWindow)
		self.music.move(sSX, _currentYPos)
		self.music.setToolTip("Copies over files in the \"music\" directory of your mod.")

		_currentYPos += _newCheckboxInCat

		self.sounds = QCheckBox("Sounds", targetWindow)
		self.sounds.move(sSX, _currentYPos)
		self.sounds.setToolTip("Copies over files and folders in the \"sounds\" directory of your mod.")
		
		_currentYPos += _newCheckboxInCat

		# Is available just not for avoiding error :D
		self.vocalsplit = QCheckBox("Vocal Split", targetWindow)
		self.vocalsplit.move(sSX, _currentYPos)
		self.vocalsplit.setToolTip("Splits \"Voices.ogg\" files into two files (\"Voices-opponent.ogg\" and \"Voices-player.ogg\") using their charts. This requires ffmpeg in PATH, and Charts enabled.")

		_currentYPos += _newCheckboxAfterCat

		self.chars = QCheckBox("Characters", targetWindow)
		self.chars.move(sX, _currentYPos)
		self.chars.setToolTip("Select all characters in the \"/characters/\" directory of your mod and convert them.")

		self.chars.stateChanged.connect(self.characterSection)

		_currentYPos += _newCheckboxInCat

		self.icons = QCheckBox("Health Icons", targetWindow)
		self.icons.move(sSX, _currentYPos)
		self.icons.setToolTip("Copies over all of your character icon .png files from the \"/images/icons/\" directory of your mod. This also generates Freeplay Icons (These require characters enabled).")

		_currentYPos += _newCheckboxInCat

		self.jsons = QCheckBox(".json files", targetWindow)
		self.jsons.move(sSX, _currentYPos)
		self.jsons.setToolTip("Converts your character's .json files to the appropiate format.")

		_currentYPos += _newCheckboxInCat

		self.charassets = QCheckBox("Assets", targetWindow)
		self.charassets.move(sSX, _currentYPos)
		self.charassets.setToolTip("Copies over your .png and .xml files from the \"/images/characters/\" directory of your mod.")

		_currentYPos = _defaultYPos
		_currentYPos += _spacingBelowLabel

		sX += 150
		sSX = sX + _catItemLeftSpacing

		self.weeks = QCheckBox("Weeks", targetWindow)
		self.weeks.move(sX, _currentYPos)
		self.weeks.setToolTip("Select week conversions.")

		self.weeks.stateChanged.connect(self.weekSection)

		_currentYPos += _newCheckboxInCat

		self.props = QCheckBox("Menu Characters (Props)", targetWindow)
		self.props.move(sSX, _currentYPos)
		self.props.resize(400, 30)
		self.props.setToolTip("Converts your menu character .json files from the \"/images/menucharacters/\" directory of your mod to the appropiate format.")

		_currentYPos += _newCheckboxInCat

		self.titles = QCheckBox("Week Images (Titles)", targetWindow)
		self.titles.move(sSX, _currentYPos)
		self.titles.resize(400, 30)
		self.titles.setToolTip("Copies over your .png files from the \"/images/storymenu/\" directory of your mod.")

		_currentYPos += _newCheckboxInCat

		self.levels = QCheckBox("Levels", targetWindow)
		self.levels.move(sSX, _currentYPos)
		self.levels.setToolTip("Converts your week .json files from the \"/weeks/\" directory of your mod to the appropiate format.")

		_currentYPos += _newCheckboxAfterCat

		self.stages = QCheckBox("Stages", targetWindow)
		self.stages.move(sX, _currentYPos)
		self.stages.setToolTip("Converts stage .jsons from the \"/stages/\" directory of your mod and parses the .lua files to asign props.")

		_currentYPos += _newCheckbox

		self.meta = QCheckBox("Pack Meta", targetWindow)
		self.meta.move(sX, _currentYPos)
		self.meta.setToolTip("Converts your \"pack.json\" to the appropiate format, and copies your \"pack.png\" file.")

		_currentYPos += _newCheckbox

		self.images = QCheckBox("Images", targetWindow)
		self.images.move(sX, _currentYPos)
		self.images.setToolTip("Copies over your .png and .xml files from the \"/images/\" directory of your mod.")

		self.convert = QPushButton("Convert", targetWindow)
		self.convert.move((targetWindow.width() - 20) - self.convert.width(), (targetWindow.logsLabel.y() - 20) - self.convert.height())
		self.convert.clicked.connect(self.convertCallback)

		self.radioCheck(True, True)

		self.widgetsList += [
			self.modLabel,
			self.baseGameLabel,
			self.findModButton,
			self.findBaseGameButton,
			self.modLineEdit,
			self.baseGameLineEdit,
			self.defaultsLabel,
			self.onlyChars,
			self.onlySongs,
			self.onlyChars,
			self.onlyCharts,
			self.onlyStages,
			self.fullMod,
			self.iChoose,
			self.optionsLabel,
			self.charts,
			self.events,
			self.songs,
			self.insts,
			self.voices,
			self.music,
			self.sounds,
			self.vocalsplit,
			self.chars,
			self.icons,
			self.jsons,
			self.charassets,
			self.weeks,
			self.props,
			self.titles,
			self.levels,
			self.stages,
			self.meta,
			self.images,
			self.convert
		]

		#self.hideAll()

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
		sender = self.senderWindow.sender()
		if check:
			if sender == self.fullMod or default:
				# Set enabled after to avoid conflicts with other stateChanged callbacks
				self.allToDefaults()
			if sender == self.onlyCharts:
				self.allToDefaults(False)

				self.charts.setEnabled(True)
				self.charts.setChecked(True)
				self.events.setChecked(True)
			if sender == self.onlySongs:
				self.allToDefaults(False)

				self.songs.setEnabled(True)
				self.songs.setChecked(True)

				self.insts.setChecked(True)
				self.voices.setChecked(True)
				self.vocalsplit.setChecked(_vocalSplitEnabledByDefault)
				self.music.setChecked(True)
				self.sounds.setChecked(True)
			if sender == self.onlyChars:
				self.allToDefaults(False)

				self.chars.setEnabled(True)
				self.chars.setChecked(True)

				self.icons.setChecked(True)
				self.jsons.setChecked(True)
				self.charassets.setChecked(True)
			if sender == self.onlyStages:
				self.allToDefaults(False)

				self.stages.setEnabled(True)
				self.stages.setChecked(True)
			if sender == self.iChoose:
				self.allToDefaults(True, True)
	
	def chartsEventsSection(self, state):
		self.events.setEnabled(state == 2)

	def songsSection(self, state):
		self.insts.setEnabled(state == 2)
		self.voices.setEnabled(state == 2)
		self.vocalsplit.setEnabled(_vocalSplitEnabledByDefault and state == 2)
		self.sounds.setEnabled(state == 2)
		self.music.setEnabled(state == 2)

	def characterSection(self, state):
		self.icons.setEnabled(state == 2)
		self.jsons.setEnabled(state == 2)
		self.charassets.setEnabled(state == 2)

	def weekSection(self, state):
		self.props.setEnabled(state == 2)
		self.titles.setEnabled(state == 2)
		self.levels.setEnabled(state == 2)

	def findMod(self):
		modFolder = QFileDialog.getExistingDirectory(self.senderWindow, "Select Mod Folder")
		self.modLineEdit.setText(modFolder)

	def findBaseGame(self):
		baseGameFolder = QFileDialog.getExistingDirectory(self.senderWindow, "Select Base Game Folder")
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
			open(_defaultsFile, 'w').write(f'{psych_mod_folder_path}\n{result_path}\n\nLAST LOG: {log.logMemory.current_log_file}\n======================\nOPTIONS:{optionsParsed}')
		except Exception as e:
			logging.error(f'Problems with your save file: {e}')
			self.senderWindow.throwError(f'Problems on your save file! {e}')

		if psych_mod_folder_path != None and result_path != None:
			# try:
			main.convert(psych_mod_folder_path, result_path, options)
			# except Exception as e:
				# self.throwError('Exception ocurred', f'{e}')
				# This is kinda(?) unfinished
		else:
			logging.warn('Select an input folder or output folder first!')

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

		self.setWindowTitle(f"FNF Porter {_windowTitleSuffix}")
		wid = 750
		hei = 750

		self.setFixedSize(QSize(wid, hei))
		self.setMinimumSize(QSize(wid, hei))
		self.setMaximumSize(QSize(wid, hei))
		
		pixmap = QPixmap()
		pixmap.loadFromData(icon)
		self.setWindowIcon(QIcon(pixmap))

		self.logsLabel = QTextBrowser(self)
		self.logsLabel.resize(self.width() - 40, 270)
		self.logsLabel.move(20, self.height() - (self.logsLabel.height() + 20))

		font = QFont()
		font.setFamily(u"Consolas")
		font.setBold(True)
		font.setWeight(75)

		self.logsLabel.setFont(font)

		self.psychToBaseUI = PsychToBaseUI(self)
		self.homePageUI = HomePageUI(self)
		self.vocalSplitUI = VocalSplitUI(self)

		self.stateList = [self.homePageUI, self.psychToBaseUI, self.vocalSplitUI]

		self.goToState('home')

	def goToStateWithConversionTuple(self, conversion):
		states = {
			('Psych Engine', 'Base Game'): 'psych2base'
		}

		if conversion in states:
			self.goToState(states[conversion])

	def goToState(self, stateId = ''):
		#print(stateId)

		for state in self.stateList:
			state.hideAll()
			if state.stateId == stateId:
				state.showAll()
	
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
