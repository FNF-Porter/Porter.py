"""Utility tool for configuring the logger"""

import logging

from time import strftime
from os import mkdir

class CustomHandler(logging.StreamHandler):
    def emit(self, record):
        log_entry = self.format(record)
        print(f'{log_entry}')

def setup() -> logging.RootLogger:
	"""instance of Logger module, will be used for logging operations"""
	
	# logger config
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# log format
	log_format = logging.Formatter("%(asctime)s: [%(filename)s] [%(levelname)s] %(message)s", "%H:%M:%S")

	try: mkdir("logs")
	except: pass
     
	# file handler
	file_handler = logging.FileHandler(f"""logs/fnf-porter{strftime("%Y-%m-%d_%H-%M-%S")}.log""")
	file_handler.setFormatter(log_format)

    # console handler
	console_handler = CustomHandler()
	console_handler.setFormatter(log_format)

	logger.handlers.clear()
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	logging.info(f"""Thanks for using FNF Porter!
	Created by Gusborg, BombasticTom, Tposejank, and Cobalt
	Download on Gamebanana: https://gamebanana.com/tools/""")
	logger.info("Logger initialized!")

	return logger