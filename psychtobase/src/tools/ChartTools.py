from src import Utils, Constants, files, window 
import logging
from pathlib import Path
from src.Paths import Paths
from copy import deepcopy

class ChartObject:
	"""
	A convenient way to store chart metadata.

	Args:
		path (str): The path where the song's chart data is stored.
		output (str): The path where you want to save the song.
	"""
	def __init__(self, path: str, output:str, EventsYesOrNO:bool) -> None:
		self.songPath = Path(path)
		self.savePath = Path(output)

		self.songFile = self.songPath.name
		self.songName = self.songFile.replace("-", " ")

		self.startingBpm = 0
		self.sections = []

		self.metadata:dict = deepcopy(Constants.BASE_CHART_METADATA)
		self.charts:dict = {}
		self.difficulties:list = []

		self.chart:dict = deepcopy(Constants.BASE_CHART)
		self.chart["events"] = []

		self.shouldConvertEvents = EventsYesOrNO # Unhinged variable name cuz were using so many variables

		self.initCharts()

		try:
			self.setMetadata()
		except:
			logging.error('Failed to set metadata')

		logging.info(f"Chart for {self.metadata.get('songName')} was created!")

	def initCharts(self):
		logging.info(f"Initialising charts for {self.songName}...")

		charts = self.charts

		difficulties = self.difficulties
		unorderedDiffs = set()

		for file in self.songPath.iterdir():

			if file.suffix == ".json":
				if file.stem == "events" and self.shouldConvertEvents:
					self.convertEvents(file)
					continue
			else:
				# If file isn't json: skip
				continue

			fileName = file.stem
			nameSplit = fileName.split("-")
			nameLength = len(nameSplit)

			difficulty = "normal"

			if nameLength > 2:
				difficulty = nameSplit[-1]
			elif nameLength > 1 and fileName != self.songFile:
				difficulty = nameSplit[1]

			filePath = self.songPath / fileName
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

		self.songName = metadata["songName"] = sampleChart.get("song").replace("-", " ").title()
		metadata["artist"] = 'Unknown Artist'

		logging.info(f"Initialising metadata for {self.metadata.get('songName')}...")

		characters["player"] = Utils.character(sampleChart.get("player1", "bf"))
		characters["girlfriend"] = Utils.character(sampleChart.get("gfVersion", sampleChart.get("player3", "gf")))
		characters["opponent"] = Utils.character(sampleChart.get("player2", "dad"))

		playData["difficulties"] = self.difficulties
		playData["stage"] = Utils.stage(sampleChart.get("stage", "mainStage"))

		metadata["ratings"] = {diff: 0 for diff in self.difficulties} # Ratings don't do much now so :P
		metadata["timeChanges"] = [Utils.timeChange(0, self.startingBpm, 4, 4, 0, [4]*4)]

	def convertEvents(self, file):
		logging.info(f"Events conversion for {self.songName} started!")

		file = file.with_suffix('')
		fileJson = Paths.parseJson(file)
		events_data = fileJson.get("song", {}).get("events", [])

		# Sometimes numbers are used instead of names
		target_nums = {
        	"0": "bf",
        	"1": "dad",
        	"2": "gf"
    	}

		for event in events_data:
			time = event[0]
			event_type = event[1][0][0]

			if event_type == "Play Animation":
				anim = event[1][0][1]
				target = event[1][0][2].lower() # When the game is stupid and doesn't like capitalization
				if str(target) in target_nums:
					target = target_nums[str(target)]
				else:
					target = target.lower()
				self.chart["events"].append(Utils.playAnimation(time, target, anim, True))
			elif event_type == "Change Character":
				target = event[1][0][1].lower()
				char = event[1][0][2]
				if str(target) in target_nums:
					target = target_nums[str(target)]
				else:
					target = target.lower()
				self.chart["events"].append(Utils.changeCharacter(time, target, char))
			else:
				logging.warn(f"Conversion for event {event_type} is not implemented!")

		logging.info(f"Events conversion for {self.songName} complete!")

	def convert(self):
		logging.info(f"Chart conversion for {self.metadata.get('songName')} started!")

		prevMustHit = self.sampleChart["notes"][0].get("mustHitSection", True)
		prevTime = 0

		events = self.chart["events"]
		events.append(Utils.focusCamera(0, prevMustHit))

		existing_events = set()

		for i, (diff, cChart) in enumerate(self.charts.items()):
			# cChart - convert Chart
			self.chart["scrollSpeed"][diff] = cChart.get("speed")
			notes = self.chart["notes"][diff] = []

			steps = 0

			prev_notes = set()
			total_duplicates = 0

			for section in cChart.get("notes"):
				mustHit = section.get("mustHitSection", True)
				isDuet = False

				for note in section.get("sectionNotes"):
					strumTime = note[0]
					noteData = note[1]
					length = note[2]

					if noteData < 0 and self.shouldConvertEvents: # Event notes (not yet supported, simply skipping them to keep the chart valid)
						logging.warn(f'Tried converting legacy event "{length}". Legacy events are currently not supported. Sorry!')
						continue

					if not mustHit:
						noteData = (noteData + 4) % 8 # We're shifting the notes! Basic arithmetic operations 🤓

						if not isDuet and noteData < 4:
							isDuet = True

					# Backhands any dupe notes as Psych engine handles this in PlayState, base game doesn't
					is_duplicate = any(
						abs(existing_note[0] - strumTime) < 1 and existing_note[1] == noteData
						for existing_note in prev_notes
					)

					if is_duplicate:
						total_duplicates += 1
						continue

					prev_notes.add((strumTime, noteData))

					# Alt Singing Animation implementation using Play Animations!
					if len(note) > 3 and note[3] == "Alt Animation": # Note types do not count as events, so they WILL be converted 🤓
						target = "player" if noteData in range(4) else "opponent"
						if noteData in [0, 4]:
							anim = "singLEFT-alt"
						elif noteData in [1, 5]:
							anim = "singDOWN-alt"
						elif noteData in [2, 6]:
							anim = "singUP-alt"
						elif noteData in [3, 7]:
							anim = "singRIGHT-alt"
						play_animation = (strumTime, target, anim)

						if play_animation not in existing_events:
							events.append(Utils.playAnimation(strumTime, target, anim, False))
							existing_events.add(play_animation)

					notes.append(Utils.note(noteData, length, strumTime))

				if i == 0:
					# Genius
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

			if total_duplicates > 0:
				logging.warn(f"We found {total_duplicates} duplicate notes in '{diff}' difficulty data! Notes were successfully removed.")

        # Process events within the chart file becuz fuck us
		if self.shouldConvertEvents:
			# Sometimes numbers are used instead of names
			target_nums = {
        		"0": "bf",
        		"1": "dad",
        		"2": "gf"
    		}
			if "events" in cChart:
				for event in cChart["events"]:
					time = event[0]

					all_events = event[1]

					for stacked_event in all_events:
						event_type = stacked_event[0]

						if event_type == "Play Animation":
							anim = stacked_event[1]
							target = stacked_event[2].lower()

							if str(target) in target_nums:
								target = target_nums[str(target)]
							else:
								target = target.lower()

							play_animation = (time, target, anim, True)

							if play_animation not in existing_events:
								events.append(Utils.playAnimation(time, target, anim, True))
								existing_events.add(play_animation)
						elif event_type == "Change Character":
							target = stacked_event[1].lower()
							char = stacked_event[2]

							if str(target) in target_nums:
								target = target_nums[str(target)]
							else:
								target = target.lower()

							change_character = (time, target, char)

							if change_character not in existing_events:
								events.append(Utils.changeCharacter(time, target, char))
								existing_events.add(change_character)
						else:
							logging.warn(f"Conversion for event {event_type} is not implemented!")

		logging.info(f"Chart conversion for {self.metadata.get('songName')} was completed!")

	def save(self):
		# In case there were issues in how the Song was previously named, we save it under a new name!
		newSongFile = Utils.formatToSongPath(self.songName)

		folder = Path(Constants.FILE_LOCS.get('CHARTFOLDER')[1]) / newSongFile
		saveDir = f'{self.savePath}{folder}'
		files.folderMake(saveDir)

		output = Paths.join(saveDir, f'{self.songFile}-metadata')
		Paths.writeJson(output, self.metadata, 2)

		output = Paths.join(saveDir, f'{newSongFile}-chart')
		Paths.writeJson(output, self.chart, 2)

		logging.info(f"[{newSongFile}] Saving {self.songName} to {saveDir}")