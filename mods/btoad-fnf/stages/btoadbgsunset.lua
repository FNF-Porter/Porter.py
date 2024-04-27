function onCreate()
    -- Background objects
    makeLuaSprite('sky', 'btoadBGSunset/sky', -350, -150);
    setScrollFactor('sky', 0.9, 0.9);
    scaleObject('sky', 1.25, 1.25);

    makeLuaSprite('background', 'btoadBGSunset/background', -350, -50);
    setScrollFactor('background', 0.5, 0.93);
    scaleObject('background', 1.2, 1.2);

    makeLuaSprite('back', 'btoadBGSunset/back', -350, -100);
    setScrollFactor('back', 0.9, 0.85);
    scaleObject('back', 1.2, 1.2);

    -- Floor
    makeLuaSprite('floor', 'btoadBGSunset/floor', -550, 650);
    setScrollFactor('floor', 1, 1);
    scaleObject('floor', 1.4, 1.4);

    -- Foreground Objects
    makeLuaSprite('foreground', 'btoadBGSunset/foreground', -400, 500);
    setScrollFactor('foreground', 1.1, 1.1);
    scaleObject('foreground', 1.3, 1.3);

    makeLuaSprite('mushroomFG1', 'btoadBGSunset/foreground_mushroom', 100, 700);
    setScrollFactor('mushroomFG1', 1.1, 1.1);
    scaleObject('mushroomFG1', 0.9, 0.9);

    makeLuaSprite('mushroomFG2', 'btoadBGSunset/foreground_mushroom_2', 1450, 600);
    setScrollFactor('mushroomFG2', 1.1, 1.1);
    scaleObject('mushroomFG2', 0.9, 0.9);

    -- Add Lua Sprites
    -- Behind Characters
    addLuaSprite('sky');
    addLuaSprite('background');
    addLuaSprite('back');
    addLuaSprite('floor');
    -- In front of Characters
    addLuaSprite('foreground', true);
    addLuaSprite('mushroomFG1', true);
    addLuaSprite('mushroomFG2', true);
end

local tweenObjs = {"foreground", "mushroomFG1", "mushroomFG2"}; -- Easier to manage

function onStepHit()
    if curStep == 1952 then
        setProperty('sky.visible', false);
        setProperty('background.visible', false);
        setProperty('back.visible', false);
        setProperty('floor.visible', false);
        setProperty('foreground.visible', false);
        setProperty('mushroomFG1.visible', false);
        setProperty('mushroomFG2.visible', false)
    elseif curStep == 2224 then
        doTweenAlpha('epicTween1', 'gf', -1, 6, 'linear')
        doTweenAlpha('epicTween2', 'boyfriend', -1, 6, 'linear')
        doTweenAlpha('epicTween3', 'dad', -1, 6, 'linear')
    elseif curStep == 2246 then
        doTweenAlpha('epicTween4', 'camHUD', -1, 6, 'linear')
    end
end

function onEvent(n, v1)
    if n == "badapplelol" then
        if (v1 == 'a') then
            for obj=1, #tweenObjs do
                local objName = tweenObjs[obj];
                doTweenAlpha(objName.."alphatween", objName, 0, 0.37, 'circInOut');
            end
        elseif (v1 == 'b') then
            for obj=1, #tweenObjs do
                local objName = tweenObjs[obj];
                doTweenAlpha(objName.."alphatween", objName, 1, 0.37, 'circInOut');
            end
        end
    end
end

function onCreatePost()
    if getPropertyFromClass("backend.ClientPrefs", "data.shaders") then
        addHaxeLibrary("ShaderFilter", "openfl.filters");

        makeLuaSprite("die2");

        initLuaShader("bloom", 140);
        setSpriteShader("die2", "bloom");

        runHaxeCode([[
            game.camHUD.setFilters([new ShaderFilter(game.getLuaObject("die2").shader)]);
            game.camGame.setFilters([new ShaderFilter(game.getLuaObject("die2").shader)]);
        ]]);
    end
end

--[[
too much traces could slow down game for some devices  
function onUpdatePost()
  setShaderFloat("die2", "iTime", os.clock());
end--]]