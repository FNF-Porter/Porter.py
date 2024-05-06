import time

session_logs = []

def log_line(log_file, log_text):
    session_logs.append(f'\n[{log_file}] [{int(time.time())}] {log_text}')

def save_log():
    log_file = f'log_{int(time.time())}.txt'
    log_line('log.py', f'Saving logs to {log_file}')

    # with open(log_file, 'w') as log:
    # log.write(logs)

    print(session_logs)