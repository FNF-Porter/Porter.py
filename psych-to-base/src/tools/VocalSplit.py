import json
import sys
from pydub import AudioSegment
import numpy as np

chart = {}
chartFile = sys.argv[1]
with open(chartFile, 'r') as file:
    chart = json.loads(file.read())['song']

bpm = chart['bpm']
beatLength = (60 / bpm) * 1000
stepLength = beatLength / 4
sectionLength = beatLength * 4

print('BPM', bpm)
print('Sections', sectionLength, 'ms')
print('Beats', beatLength, 'ms')
print('Steps', stepLength, 'ms')

songSteps = 0
lastSteps = 0
sectionDirs = []

for section in chart['notes']:
    if section.get('changeBPM', None) != None:
        print('BPM Change')
        beatLength = (60 / section.get('bpm', 1)) * 1000
        lastSteps = songSteps
        songSteps = 0
        stepLength = beatLength / 4

    songTime = lastSteps + (songSteps * stepLength)
    mustHit = section['mustHitSection']
    isDuet = False

    for note in section['sectionNotes']:
        if note[1] > 3:
            isDuet = True

    # print('Section at', songTime)
    # print('Must Hit', mustHit)
    # print('Duet', isDuet)

    sectionDirs.append([songTime, mustHit, isDuet])

    songSteps += section['lengthInSteps']

originalVocals = AudioSegment.from_ogg("Voices.ogg")
vocalsBF = AudioSegment.empty()
vocalsOpponent = AudioSegment.empty()

arr = np.array(sectionDirs)

arr = arr[arr[:,0].argsort()]
arr = np.vstack([arr, [len(originalVocals), False, False]])

for i in range(len(arr) - 1):
    section_start_time = int(arr[i, 0])
    next_section_time = int(arr[i + 1, 0])

    chunk = originalVocals[section_start_time:next_section_time]
    silence = AudioSegment.silent(duration=len(chunk))

    if arr[i, 2] or arr[i, 1] == False:  # Duet or not must hit
        vocalsOpponent += chunk
        vocalsBF += silence
    else:
        vocalsBF += chunk
        vocalsOpponent += silence

vocalsBF.export("Voices-Player.ogg", format="ogg")
vocalsOpponent.export("Voices-Opponent.ogg", format="ogg")
