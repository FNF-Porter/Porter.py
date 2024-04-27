function onUpdate(elapsed)
    songPos = getSongPosition()
    local currentBeat = (songPos/5000)*(curBpm/60)
    
    --Player Notes
    
    noteTweenY('defaultPlayerStrumY0', 4, defaultPlayerStrumY0 - 40*math.sin((currentBeat+4*0.25)*math.pi), 0.1)
    noteTweenY('defaultPlayerStrumY1', 5, defaultPlayerStrumY1 - 40*math.sin((currentBeat+5*0.25)*math.pi), 0.1)
    noteTweenY('defaultPlayerStrumY2', 6, defaultPlayerStrumY2 - 40*math.sin((currentBeat+6*0.25)*math.pi), 0.1)
    noteTweenY('defaultPlayerStrumY3', 7, defaultPlayerStrumY3 - 40*math.sin((currentBeat+7*0.25)*math.pi), 0.1)
    
    --Opponent Notes
    
    noteTweenY('defaultOpponentStrumY0', 0, defaultOpponentStrumY0 + 40*math.sin((currentBeat+0*0.25)*math.pi), 0.1)
    noteTweenY('defaultOpponentStrumY1', 1, defaultOpponentStrumY1 + 40*math.sin((currentBeat+1*0.25)*math.pi), 0.1)
    noteTweenY('defaultOpponentStrumY2', 2, defaultOpponentStrumY2 + 40*math.sin((currentBeat+2*0.25)*math.pi), 0.1)
    noteTweenY('defaultOpponentStrumY3', 3, defaultOpponentStrumY3 + 40*math.sin((currentBeat+3*0.25)*math.pi), 0.1)
end

function round(x, n) --https://stackoverflow.com/questions/18313171/lua-rounding-numbers-and-then-truncate
	--Stupid accuracy (i hate it).
    n = math.pow(10, n or 0)
    x = x * n
    if x >= 0 then x = math.floor(x + 0.5) else x = math.ceil(x - 0.5) end
    return x / n
end

function onStepHit()
    if curStep > 1 then
        setProperty('health', 1)
        setProperty('iconP2.x', 510)
        setProperty('iconP1.x', 620)
    end
    if curStep == 1 then
        doTweenAlpha('epicTween', 'healthBar', 0, 2, 'linear')
        doTweenAlpha('epicTween2', 'healthBarBG', 0, 2, 'linear')
    end
end

function noteMiss()
    if curStep > 1 then
        setProperty('health', -500)
    end
end