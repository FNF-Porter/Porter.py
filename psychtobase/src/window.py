from base64 import b64decode
import psychtobase.main as main
import logging
import psychtobase.src.Constants as Constants

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QLabel, QLineEdit, QPushButton, QFileDialog, QDialog, QVBoxLayout

#the icon, in base64 (because its easier to compile)
image_bytes = b64decode("iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAC4jAAAuIwF4pT92AAADS0lEQVR42u1a0Y3bMAyVDI/RLRSgQ9wCnUBGh+hXhyisCW6BDlEgRhcqwEYX6SqrkkVR0llxTMCHw+WchI+P5CNlxk7LN7gC6OsIvgylQDw1AC4bYL4+JwDvJgQ8NwCRlNDM6JkdQ+03jBXIXkHgzQvgsqw+g0+XYzCAX/gaPLU8ZBHk1XLeBUAKHGiHqQF+9CNs6FE3kCIixfzmj/4xz3Kb/gE29MSEgeA8WOdRuR94vScmjCU3z0LgU8RjggHyrqHYvVNMi+obAPul0Y5n2B7OZ6UAyGuZ8xupsrD9ZPTwoZHXIESAmIU8hhQ+7DA0LRWVXkcs4Dkp0KIAWmDVMvEuGeA6X50JjyqFa4HQA5hDTvSfugjWjJ6+171/r/wvlsKtQYONPSP3Fi3Vu8CPz9/Y7z+fkimA6Qopx30GQMaCtRSIsaeI5zrv/D83YNStAXZKewADA0YfDKAWSCg7WwBGWPAkAdD5aTZAbLUIcZy1dYDiuM1/SvSm/1ftoMW0ytg4jbEC6H1JuwbjkYg30wsT4TxBmo0TBogxI1JWHGG6CeRE3xYwy4Kp0iGKBiIFwkCgLLa9+tdm62tleo/z5ef9KmLAelRdHPqrLWasQEGC16cS9Hd2hq7AhOQ+KBgQ3feDBjtGbHcYC9+43mLiVgPM2jG/k0wXJol1IwjA11/fGYUZ1I2OLnqSCKgqPGwtFkJavFg9HlptI0EB3yFMRFWFk+bm06B0akNMq+tWJb3TohQQrvMJsOq2wX+DguBICYvTBDcQ3oDwnElFWRZqhmoMcFMhUN1ha2z1o2+dss77bFAVH7IoOxdwWBBigqa8dZwy6ISiqyo/YUICAKSMLiS2HA29JjNOilWDx2tIAHClkukQAyLwd45lgf7dXmgFO13g9YUzfVWtAS4ImgUhhzG0vxU+sgD6UCmMUHLoXPcLZmxik4UPUsyIlGkykb3PCQjAsJ0hV+66zm99VhMhZGZ7HtMBOS2xVr/fTQmWRL0l9ZsDYFgArdON6nhTAAI1gPOGB6FbjqdY17IIBlmRVH/3lgi1Ir4LADnAxEBJAYGlezcAuPIZqyixcprqfPkwVFIkFe25QOMUJnCPcqx32mmnnXbaaaedto/9BWaMwpiIwnWtAAAAAElFTkSuQmCC")
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
		pixmap.loadFromData(image_bytes)
		self.setWindowIcon(QIcon(pixmap))

		self.exec()

	def on_button_clicked(self):
		self.input_values = [input.text() for input in self.inputs]
		# print(self.input_values)

		self.close()
		
class Window(QMainWindow):
	def on_worker_finished(self):
		print("Long task finished.")

	def __init__(self):
		super().__init__()

		self.setWindowTitle("FNF Porter v0.1")
		
		self.setMinimumSize(QSize(750, 200))
		
		pixmap = QPixmap()
		pixmap.loadFromData(image_bytes)
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

		self.modLineEdit = QLineEdit(self)
		self.baseGameLineEdit = QLineEdit(self)
		self.modLineEdit.move((self.findModButton.x() - 20) - 400, 20)
		self.baseGameLineEdit.move((self.findBaseGameButton.x() - 20) - 400, 60)
		self.modLineEdit.resize(400, 30)  # Adjust the size as needed
		self.baseGameLineEdit.resize(400, 30)  # Adjust the size as needed

		self.convert = QPushButton("Convert", self)
		self.convert.move((self.width() - 20) - self.convert.width(), (self.height() - 20) - self.convert.height())
		self.convert.clicked.connect(self.convertCallback)

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
		if psych_mod_folder_path != None and result_path != None:
			main.convert(psych_mod_folder_path, result_path)
		else: prompt('','','ERROR','Please select mod folders!')

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