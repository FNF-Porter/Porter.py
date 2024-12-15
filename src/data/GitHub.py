import logging
import subprocess

from .. import Utils

REMOTE = "FNF-Porter/Porter.py"

def runGitCMD(*cmd: str, ret_code = "-"):
	fullCMD = ['git', *cmd]

	try:
		process = subprocess.run(fullCMD, capture_output = True, text = True, check = True)
		return process.stdout
	except Exception as e:
		logging.warning(f"Command {' '.join(fullCMD)} failed! [{type(e).__name__}: {e}]")
		return ret_code

def get_commit_hash() -> str:
	return runGitCMD('rev-parse', '--short', 'HEAD')

def get_version() -> str:
	return runGitCMD('rev-list', 'HEAD', '--count', ret_code = "0")

def page(*urlElements: str) -> str:
	"Returns a string of your URL"
	return Utils.createUrl("https://www.github.com", REMOTE, *urlElements)

def openInBrowser(*urlElements: str) -> str:
	"""
	Opens a github page from `REMOTE`.
	Returns a string of the URL
	"""
	return Utils.openUrl(page(*urlElements))