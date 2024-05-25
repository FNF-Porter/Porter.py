"""Utility tool for configuring the logger"""

import logging
import src.window as window
import sys

from time import strftime
from pathlib import Path

class CustomHandler(logging.StreamHandler):
    def emit(self, record):
        log_entry = self.format(record)
        print(log_entry)
        window.window.logsLabel.append(log_entry)
        
class LogMem():
    def __init__(self, log):
        self.current_log_file = log
        
logMemory = LogMem('No file yet recorded')

def setup() -> logging.RootLogger:
	"""instance of Logger module, will be used for logging operations"""
	
	# logger config
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# log format
	log_format = logging.Formatter("%(asctime)s: [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s", "%H:%M:%S")

	try: Path("logs").mkdir(exist_ok=True)
	except: pass
     
	# file handler
	log_file = f"""logs/fnf-porter-{strftime("%Y-%m-%d_%H-%M-%S")}.log"""
	file_handler = logging.FileHandler(log_file)
	file_handler.setFormatter(log_format)
     
	logMemory.current_log_file = log_file

    # console handler
	console_handler = CustomHandler()
	console_handler.setFormatter(log_format)

	_GB_ToolID = ''

	logger.handlers.clear()
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	logger.info("Logger initialized!")

	return logger

def log_exception(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions."""
    logger = logging.getLogger()
    if not issubclass(exc_type, KeyboardInterrupt):
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Configure global exception handler to use the logger
sys.excepthook = log_exception