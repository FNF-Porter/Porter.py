function round(x, n) --https://stackoverflow.com/questions/18313171/lua-rounding-numbers-and-then-truncate
	--Stupid accuracy (i hate it).
    n = math.pow(10, n or 0)
    x = x * n
    if x >= 0 then x = math.floor(x + 0.5) else x = math.ceil(x - 0.5) end
    return x / n
end

function onStepHit()
    if curStep > 160 then
        setProperty('health', 1)
        setProperty('iconP2.x', 510)
        setProperty('iconP1.x', 620)
    end
    if curStep == 160 then
        doTweenAlpha('epicTween', 'healthBar', 0, 2, 'linear')
        doTweenAlpha('epicTween2', 'healthBarBG', 0, 2, 'linear')
    end
end

function noteMiss()
    if curStep > 160 then
        setProperty('health', -500)
    end
end