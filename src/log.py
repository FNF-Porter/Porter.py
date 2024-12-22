"""Utility tool for configuring the logger"""

import logging
import sys
import webbrowser

from PyQt6.QtWidgets import QTextBrowser

from pathlib import Path
from time import strftime

_root:Path = Path("logs").resolve()
_file:Path = None

def getFile() -> Path:
	if _file:
		return _file

	return "File not found..."

class CustomHandler(logging.StreamHandler):
	def __init__(self, logsLabel:QTextBrowser = None):
		super().__init__()
		self.logsLabel:QTextBrowser = logsLabel

	def emit(self, record):
		log_entry = self.format(record)
		print(log_entry)

		if self.logsLabel:
			self.logsLabel.append(log_entry)

def setup() -> tuple:
	"Sets up a new Logger, which is used for advanced logging operations."

	global _file

	# Setup of some data variables

	_root.mkdir(exist_ok = True)
	time = strftime("%Y-%m-%d_%H-%M-%S")
	log_format = logging.Formatter("%(asctime)s: [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s", "%H:%M:%S")

	# Configuration
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# File Handling
	_file = _root.joinpath(f"fnf-porter-{time}.log")
	file_handler = logging.FileHandler(_file)
	file_handler.setFormatter(log_format)

	# Console Handling
	console_handler = CustomHandler()
	console_handler.setFormatter(log_format)

	logger.handlers.clear()
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	logger.info("Logger initialized!")

	return (logger, console_handler)

def open():
	"Opens current log file"

	try:
		logging.info(f'Attempting to open {_file.name}')

		if not _file.exists():
			raise FileNotFoundError("Log wasn't found!")

		webbrowser.open(_file)

	except Exception as e:
		logging.warning(f"UNABLE TO OPEN LOG! {type(e).__name__}: {e}")

def log_exception(exc_type, exc_value, exc_traceback):
	"Log uncaught exceptions."

	logger = logging.getLogger()
	if not issubclass(exc_type, KeyboardInterrupt):
		logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Configure global exception handler to use the logger

sys.excepthook = log_exception