function onCreate()
    -- Cloud Objects
    makeLuaSprite('cloud', 'btoadBG/cloud', -200, -150);
    setScrollFactor('cloud', 0.9, 0.9);
    scaleObject('cloud', 1.1, 1.1);

    makeLuaSprite('cloud2', 'btoadBG/cloud_2', 700, -200);
    setScrollFactor('cloud2', 0.9, 0.9);
    scaleObject('cloud2', 1.1, 1.1);

    makeLuaSprite('cloud3', 'btoadBG/cloud_3', 1300, -100);
    setScrollFactor('cloud_3', 0.9, 0.9);
    scaleObject('cloud3', 1.1, 1.1);

    -- Background objects
    makeLuaSprite('sky', 'btoadBG/sky', -350, -150);
    setScrollFactor('sky', 0.9, 0.9);
    scaleObject('sky', 1.25, 1.25);

    makeLuaSprite('background', 'btoadBG/background', -350, -150);
    setScrollFactor('background', 0.5, 0.93);
    scaleObject('background', 1.2, 1.2);

    makeLuaSprite('back', 'btoadBG/back', -350, -200);
    setScrollFactor('back', 0.9, 0.85);
    scaleObject('back', 1.2, 1.2);

    -- Floor
    makeLuaSprite('floor', 'btoadBG/floor', -550, 650);
    setScrollFactor('floor', 1, 1);
    scaleObject('floor', 1.4, 1.4);

    -- Foreground Objects
    makeLuaSprite('foreground', 'btoadBG/foreground', -400, 400);
    setScrollFactor('foreground', 1.1, 1.1);
    scaleObject('foreground', 1.3, 1.3);

    makeLuaSprite('mushroomFG1', 'btoadBG/foreground_mushroom', 100, 600);
    setScrollFactor('mushroomFG1', 1.25, 1.25);
    scaleObject('mushroomFG1', 0.9, 0.9);

    makeLuaSprite('mushroomFG2', 'btoadBG/foreground_mushroom_2', 1450, 500);
    setScrollFactor('mushroomFG2', 1.25, 1.25);
    scaleObject('mushroomFG2', 0.9, 0.9);

    -- Add Lua Sprites
    -- Behind Characters
    addLuaSprite('sky');
    addLuaSprite('cloud');
    addLuaSprite('cloud2');
    addLuaSprite('cloud3');
    addLuaSprite('background');
    addLuaSprite('back');
    addLuaSprite('floor');
    -- In front of Characters
    addLuaSprite('foreground', true);
    addLuaSprite('mushroomFG1', true);
    addLuaSprite('mushroomFG2', true);

    -- Performance
    close(true);
end