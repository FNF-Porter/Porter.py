import time

session_logs = ['=== CONVERTER LOGS ===']

def trace(log_file, log_text):
	session_logs.append(f'[{log_file}] [{int(time.time())}] {log_text}')

def save():
	log_file = f'log_{int(time.time())}.txt'
	trace('log.py', f'Saving logs to {log_file}')

	with open(log_file, 'w') as log:
		log.write('\n'.join(session_logs))

	print(session_logs)