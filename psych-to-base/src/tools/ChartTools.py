from src import Utils, Constants
import os, json, logging

class ChartObject:
	"""
	A convenient way to store chart metadata.

	Args:
		path (str): The path where the song's chart data is stored.
	"""
	def __init__(self, path: str) -> None:
		self.songPath = path
		self.songName:str = os.path.basename(path)

		self.difficulties:list = []
		self.metadata:dict = Constants.BASE_CHART_METADATA.copy()
		self.psychCharts:dict = {}

		self.chart:dict = Constants.BASE_CHART.copy()

		self.initCharts()
		self.setMetadata()

		logging.info(f"Chart for {self.metadata.get('songName')} was created!")

	def initCharts(self):
		charts = self.psychCharts
		difficulties = self.difficulties

		unorderedDiffs = set()

		for file in os.listdir(self.songPath):
			if not file.endswith(".json"):
				continue
			
			fileName = file[:-5]
			splitFile = fileName.split("-")
			fileLen = len(splitFile)

			difficulty = "normal"

			if fileLen > 2:
				difficulty = splitFile[-1]
			elif fileLen > 1 and fileName != self.songName:
				difficulty = splitFile[1]

			with open(os.path.join(self.songName, file), "r") as f:
				fileJson = json.load(f).get("song")

				if fileJson == None:
					continue

				unorderedDiffs.add(difficulty)
				charts[difficulty] = fileJson

		for difficulty in Constants.DIFFICULTIES:
			if difficulty in unorderedDiffs:
				difficulties.append(difficulty)
				unorderedDiffs.remove(difficulty)

		difficulties.extend(unorderedDiffs)
		del unorderedDiffs

	def setMetadata(self):
		# Chart used to get character data (ASSUMING all charts use the same characters and stages)
		sampleChart = self.psychCharts.get(self.difficulties[0])
		metadata = self.metadata

		ratings:dict = {}

		for diff in self.difficulties:
			ratings[diff] = 0

		metadata["songName"] = sampleChart.get("song").replace("-", " ").title()

		metadata["playData"]["difficulties"] = self.difficulties
		metadata["playData"]["characters"]["player"] = Utils.character(sampleChart.get("player1"))
		metadata["playData"]["characters"]["girlfriend"] = Utils.character(sampleChart.get("gfVersion", sampleChart.get("player3")))
		metadata["playData"]["characters"]["opponent"] = Utils.character(sampleChart.get("player2"))
		metadata["playData"]["stage"] = Utils.stage(sampleChart.get("stage"))

		metadata["ratings"] = ratings
		metadata["timeChanges"].append(Utils.timeChange(0, sampleChart.get("bpm"), 4, 4, 0, [4, 4, 4, 4]))

		self.stepCrochet = 15000 / sampleChart.get("bpm")
		self.sampleChart = sampleChart

	def convert(self):
		logging.info(f"Chart conversion for {self.metadata.get('songName')} started!")

		for diff, chart in self.psychCharts.items():
			self.chart["scrollSpeed"][diff] = chart.get("speed")
			self.chart["notes"][diff] = []

			notes = self.chart["notes"][diff]

			for section in chart.get("notes"):
				mustHit = section["mustHitSection"]

				for note in section.get("sectionNotes"):
					if not mustHit: # gonna improve this tomorrow too lazy to think tonight
						if note[1] > 3:
							note[1] -= 4
						else:
							note[1] += 4

					notes.append(Utils.note(note[0], note[1], note[2]))

		events = self.chart["events"]
		prevMustHit = self.sampleChart["notes"][0]["mustHitSection"]
		events.append(Utils.focusCamera(0, prevMustHit))

		steps = 0

		for section in self.sampleChart.get("notes"):
			mustHit = section["mustHitSection"]
			if (prevMustHit != mustHit):
				events.append(Utils.focusCamera(steps * self.stepCrochet, mustHit))
				prevMustHit = mustHit

			steps += section["lengthInSteps"]

		logging.info(f"Chart conversion for {self.metadata.get('songName')} was completed!")

	def save(self):
		savePath = os.path.join("output", self.songName)

		with open(os.path.join(savePath, f'{self.songName}-metadata.json'), 'w') as f:
			json.dump(self.metadata, f, indent=2)

		with open(os.path.join(savePath, f'{self.songName}-chart.json'), 'w') as f:
			json.dump(self.chart, f, indent=2)

		logging.info(f"Saving {self.metadata.get('songName')} to {savePath}")