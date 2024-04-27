function onCreate()
    -- Background objects
    makeLuaSprite('sky', 'btoadBG2/sky', -350, -150);
    setScrollFactor('sky', 0.9, 0.9);
    scaleObject('sky', 1.25, 1.25);

    makeLuaSprite('background', 'btoadBG2/background', -350, -150);
    setScrollFactor('background', 0.5, 0.93);
    scaleObject('background', 1.2, 1.2);

    makeLuaSprite('fireAA', 'btoadBG2/fireAA', -350, 500); -- minus100
    setScrollFactor('fireAA', 0.7, 0.9);
    scaleObject('fireAA', 1.2, 1.2);

    makeLuaSprite('back', 'btoadBG2/back', -350, -200);
    setScrollFactor('back', 0.9, 0.85);
    scaleObject('back', 1.2, 1.2);
    -- Floor
    makeLuaSprite('floor', 'btoadBG2/floor', -550, 650);
    setScrollFactor('floor', 1, 1);
    scaleObject('floor', 1.4, 1.4);

    makeLuaSprite('fireTop', 'btoadBG2/fireTop', -350, -200);
    setScrollFactor('fireTop', 0.9, 0.85);
    scaleObject('fireTop', 1.2, 1.2)

    -- Foreground Objects
    makeLuaSprite('foreground', 'btoadBG2/foreground', -400, 400);
    setScrollFactor('foreground', 0.9, 0.9);
    scaleObject('foreground', 1.3, 1.3);

    makeLuaSprite('mushroomFG1', 'btoadBG2/foreground_mushroom', 100, 600);
    setScrollFactor('mushroomFG1', 0.9, 0.9);
    scaleObject('mushroomFG1', 0.9, 0.9);

    makeLuaSprite('mushroomFG2', 'btoadBG2/foreground_mushroom_2', 1250, 500);
    setScrollFactor('mushroomFG2', 0.9, 0.9);
    scaleObject('mushroomFG2', 0.9, 0.9);

    makeLuaSprite('fireBottom', 'btoadBG2/fireBottom', -270, -180);
    setScrollFactor('fireBottom', 0.9, 0.85);
    scaleObject('fireBottom', 1.2, 1.2)

    makeLuaSprite('glow', 'btoadBG2/hglow', -270, -180);
    setScrollFactor('glow', 0.9, 0.85);
    scaleObject('glow', 1.2, 1.2)


    -- Add Lua Sprites
    -- Behind Characters
    addLuaSprite('sky');
    addLuaSprite('background');
    addLuaSprite('fireAA');
    addLuaSprite('back');
    addLuaSprite('floor');
    addLuaSprite('fireTop');
    -- In front of Characters
    addLuaSprite('foreground', true);
    addLuaSprite('mushroomFG1', true);
    addLuaSprite('mushroomFG2', true);
    addLuaSprite('fireBottom', true);
    addLuaSprite('glow', true);
end

function onStepHit()
	if curStep == 128 then
		doTweenY('move', 'fireAA', -100, 2, 'linear')
    end
end