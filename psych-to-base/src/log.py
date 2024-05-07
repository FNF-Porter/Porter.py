"""Utility tool for configuring the logger"""

import logging

from time import strftime
from os import mkdir

def setup() -> logging.RootLogger:
	"""instance of Logger module, will be used for logging operations"""
	
	# logger config
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# log format
	log_format = logging.Formatter("%(asctime)s | %(filename)s:%(lineno)d | %(message)s", "%H:%M:%S")

	try: mkdir("logs")
	except: pass

	# file handler
	file_handler = logging.FileHandler(f"""logs/{strftime("%Y-%m-%d_%H'%M'%S")}.log""")
	file_handler.setFormatter(log_format)

	logger.handlers.clear()
	logger.addHandler(file_handler)

	logger.info("Logger initialized!")

	return logger