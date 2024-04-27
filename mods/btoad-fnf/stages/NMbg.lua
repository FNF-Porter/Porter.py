function onCreate()
    --bg
    makeLuaSprite('sky', 'NMbg/sky', -600, -200);
    setScrollFactor('sky', 1, 1);
    scaleObject('sky', 1.1, 1.1)

    makeLuaSprite('bg', 'NMbg/bg', -600, -200);
    setScrollFactor('bg', 1, 1);
    scaleObject('bg', 1.1, 1.1)

    makeLuaSprite('hole', 'NMbg/hole', 0, -350);
    setScrollFactor('hole', 1, 1);
    scaleObject('hole', 1.1, 1.1)

    --fg
    makeLuaSprite('fg', 'NMbg/fg', -600, -300);
    setScrollFactor('fg', 1, 1);
    scaleObject('fg', 1.1, 1.1)

    addLuaSprite('sky')
    addLuaSprite('bg')
    addLuaSprite('hole')
    --infront chars
    addLuaSprite('fg', true)

    startTween('cheese', 'hole', {angle = 2160}, 153, {ease = 'backOut'})
end