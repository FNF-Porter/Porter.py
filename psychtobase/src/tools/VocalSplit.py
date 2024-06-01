import logging
from pathlib import Path
import numpy as np

from pydub import AudioSegment
import platform

def assignFfmpeg(audiosegment:AudioSegment):
    if platform.system() == 'Windows':
        ffmpeg_path = Path('ffmpeg.exe')

        if Path.exists(ffmpeg_path):
            ffmpeg_to_use = str(ffmpeg_path.resolve()).replace('\\', '/').replace('.exe', '')
            print('FFmpeg for AudioSegment: ' + ffmpeg_to_use)
            audiosegment.converter = ffmpeg_to_use
        else:
            logging.warn('FFmpeg path does not exist')
    else:
        logging.info('No effect, your platform is not Windows:' + platform.system())

def assignFfmpegBulk(audiosegments:list):
    for audiosegment in audiosegments:
        assignFfmpeg(audiosegment)

def vocalsplit(chart, bpm, origin, path, key, characters):
    beatLength = (60 / bpm) * 1000
    stepLength = beatLength / 4
    sectionLength = beatLength * 4

    bf = characters[0]
    dad = characters[1]

    songSteps = 0
    lastSteps = 0
    sectionDirs = []

    for section in chart:
        if section.get('changeBPM', False):
            logging.info(f'{key}: BPM Change ({section.get("bpm")}) at {songSteps} steps')
            beatLength = (60 / section.get('bpm', 1)) * 1000
            lastSteps = songSteps
            songSteps = 0
            stepLength = beatLength / 4

        songTime = lastSteps + (songSteps * stepLength)
        mustHit = section['mustHitSection']
        isDuet = section['isDuet']

        # print('Section at', songTime)
        # print('Must Hit', mustHit)
        # print('Duet', isDuet)

        sectionDirs.append([songTime, mustHit, isDuet])

        songSteps += section.get('lengthInSteps', 16)

    assignFfmpegBulk([AudioSegment])

    originalVocals = AudioSegment.from_ogg(origin + "Voices.ogg")
    vocalsBF = AudioSegment.empty()
    vocalsOpponent = AudioSegment.empty()

    assignFfmpegBulk([vocalsBF, vocalsOpponent])

    arr = np.array(sectionDirs)

    arr = arr[arr[:,0].argsort()]
    arr = np.vstack([arr, [len(originalVocals), False, False]])

    for i in range(len(arr) - 1):
        section_start_time = int(arr[i, 0])
        next_section_time = int(arr[i + 1, 0])

        chunk = originalVocals[section_start_time:next_section_time]
        silence = AudioSegment.silent(duration=len(chunk))

        # assignFfmpeg(silence)

        if arr[i, 2] or arr[i, 1] == False:  # Duet or not must hit
            vocalsOpponent += chunk
            vocalsBF += silence
        else:
            vocalsBF += chunk
            vocalsOpponent += silence

    vocalsBF.export(path + f"Voices-{bf}.ogg", format="ogg")
    vocalsOpponent.export(path + f"Voices-{dad}.ogg", format="ogg")