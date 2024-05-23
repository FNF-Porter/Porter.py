from psychtobase.src import Utils, Constants, files, window 
import os, logging
from psychtobase.src.Paths import Paths

class ChartObject:
	"""
	A convenient way to store chart metadata.

	Args:
		path (str): The path where the song's chart data is stored.
	"""
	def __init__(self, path: str, output:str) -> None:
		self.songPath = path
		self.songNameRaw:str = os.path.basename(path)
		self.songNamePath = self.songNameRaw.replace(' ', '-').lower()
		self.outputpath = output

		self.startingBpm = 0

		self.sections = []

		self.difficulties:list = []
		self.metadata:dict = Constants.BASE_CHART_METADATA.copy()
		self.charts:dict = {}

		self.chart:dict = Constants.BASE_CHART.copy()

		self.initCharts()
		try:
			self.setMetadata()
		except:
			logging.error('Failed to set metadata')

		logging.info(f"Chart for {self.metadata.get('songName')} was created!")

	def initCharts(self):
		logging.info(f"Initialising charts for {self.songNameRaw}...")

		charts = self.charts

		difficulties = self.difficulties
		unorderedDiffs = set()

		dirFiles = os.listdir(self.songPath)
		chartFiles = []
		for _f in dirFiles:
			if not _f.endswith(".json"):
				continue
			if _f.endswith("events.json"):
				logging.warn(f'[{self.songNameRaw}] events.json not supported yet! Sorry!')
				continue

			chartFiles.append(_f)

		for file in chartFiles:
			fileName = file[:-5]
			nameSplit = fileName.split("-")
			nameLength = len(nameSplit)

			difficulty = "normal"

			if nameLength > 2:
				difficulty = nameSplit[-1]
			elif nameLength > 1 and fileName != self.songNameRaw:
				difficulty = nameSplit[1]

			filePath = Paths.join(self.songPath, fileName)
			fileJson = Paths.parseJson(filePath).get("song")

			if fileJson != None:
				unorderedDiffs.add(difficulty)
				charts[difficulty] = fileJson

		for difficulty in Constants.DIFFICULTIES:
			if difficulty in unorderedDiffs:
				difficulties.append(difficulty)
				unorderedDiffs.remove(difficulty)

		difficulties.extend(unorderedDiffs)
		del unorderedDiffs

		if len(difficulties) > 0:
			self.sampleChart = charts.get(difficulties[0])
		else:
			raise FileNotFoundError("Chart not found!")

	def setMetadata(self):
		# Chart used to get character data (ASSUMING all charts use the same characters and stages)
		sampleChart = self.sampleChart

		self.startingBpm = sampleChart.get('bpm')
		self.stepCrochet = 15000 / self.startingBpm
		
		metadata = self.metadata
		playData = metadata["playData"]
		characters = playData["characters"]

		metadata["songName"] = sampleChart.get("song").replace("-", " ").title()
		metadata["artist"] = 'Unknown Artist'

		logging.info(f"Initialising metadata for {self.metadata.get('songName')}...")

		characters["player"] = Utils.character(sampleChart.get("player1", "bf"))
		characters["girlfriend"] = Utils.character(sampleChart.get("gfVersion", sampleChart.get("player3", "gf")))
		characters["opponent"] = Utils.character(sampleChart.get("player2", "dad"))

		playData["difficulties"] = self.difficulties
		playData["stage"] = Utils.stage(sampleChart.get("stage", "mainStage"))

		metadata["ratings"] = {diff: 0 for diff in self.difficulties} # Ratings don't do much now so :P
		metadata["timeChanges"] = [Utils.timeChange(0, self.startingBpm, 4, 4, 0, [4]*4)]

	def convert(self):
		logging.info(f"Chart conversion for {self.metadata.get('songName')} started!")
		prevMustHit = self.sampleChart["notes"][0].get("mustHitSection", True)
		prevTime = 0
		self.chart["events"] = [Utils.focusCamera(0, prevMustHit)]
		events = self.chart["events"]

		firstChart = True

		for diff, cChart in self.charts.items():
			# cChart - convert Chart
			self.chart["scrollSpeed"][diff] = cChart.get("speed")
			self.chart["notes"][diff] = []

			notes = self.chart["notes"][diff]
			steps = 0

			for section in cChart.get("notes"):
				mustHit = section.get("mustHitSection", True)
				isDuet = False

				for note in section.get("sectionNotes"):
					strumTime = note[0]
					noteData = note[1]
					length = note[2]

					if not mustHit:
						noteData = (noteData + 4) % 8 # We're shifting the notes! Basic arithmetic operations 🤓

						if not isDuet and noteData < 4:
							isDuet = True

					notes.append(Utils.note(strumTime, noteData, length))

				if firstChart:
					lengthInSteps = section.get("lengthInSteps", section.get("sectionBeats", 4) * 4)
					sectionBeats = section.get("sectionBeats", lengthInSteps / 4)
					bpm = section.get('bpm', self.startingBpm)
					changeBPM = section.get('changeBPM', False)

					self.sections.append({
						'mustHitSection': mustHit,
						'isDuet': isDuet,
						'lengthInSteps': lengthInSteps,
						'bpm': bpm,
						'changeBPM': changeBPM
					})

					if (prevMustHit != mustHit):
						events.append(Utils.focusCamera(prevTime + steps * self.stepCrochet, mustHit))
						prevMustHit = mustHit

					steps += lengthInSteps

					if changeBPM:
						prevTime += steps * self.stepCrochet
						self.metadata["timeChanges"].append(Utils.timeChange(prevTime, bpm, sectionBeats, sectionBeats, 0, [sectionBeats]*4))
						self.stepCrochet = 15000 / bpm
						steps = 0
				
			firstChart = False

		logging.info(f"Chart conversion for {self.metadata.get('songName')} was completed!")

	def save(self):
		folder = os.path.join(Constants.FILE_LOCS.get('CHARTFOLDER')[1], self.songNamePath)
		saveDir = f'{self.outputpath}{folder}'
		files.folderMake(saveDir)

		savePath = Paths.join(saveDir, f'{self.songNamePath}-metadata')
		Paths.writeJson(savePath, self.metadata, 2)

		savePath = Paths.join(saveDir, f'{self.songNamePath}-chart')
		Paths.writeJson(savePath, self.chart, 2)

		logging.info(f"[{self.songNamePath}] Saving {self.metadata.get('songName')} to {saveDir}")