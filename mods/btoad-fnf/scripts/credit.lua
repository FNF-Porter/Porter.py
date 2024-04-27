function onCreate()
    makeLuaSprite('backk', 'introcard/back', -1000, 150)
    setObjectCamera('backk', 'camOther')
    scaleObject('backk', 0.6, 0.6)
    addLuaSprite('backk')

    makeLuaSprite('songName', 'introcard/'..songName, -1000, 150)
    setObjectCamera('songName', 'camOther')
    scaleObject('songName', 0.6, 0.6)
    addLuaSprite('songName')
end

function onSongStart()
    doTweenX('epicTweenZ', 'backk', 0, 1, 'linear')
    doTweenX('epicTweenZn', 'songName', 0, 1, 'linear')
    runTimer('fade', 3)
end

function onTimerCompleted(fade)
    doTweenAlpha('epicTweenZ2', 'backk', 0, 1, 'linear')
    doTweenAlpha('epicTweenZn2', 'songName', 0, 1, 'linear')
end