function onCreate()
	-- background shit
	makeLuaSprite('back', 'boil/hell_back', -700, -500);
	scaleObject('back', 1.5, 1.5);
	setScrollFactor('back', 1, 1);

	makeLuaSprite('lava1', 'boil/hell_lava_1', -500, -500);
	scaleObject('lava1', 1.5, 1.5);
	setScrollFactor('lava1', 1, 1);

	makeLuaSprite('lava2', 'boil/hell_lava_2', 875, -500);
	scaleObject('lava2', 1.5, 1.5);
	setScrollFactor('lava2', 1, 1);

	makeLuaSprite('rock1', 'boil/hell_rock_1', -375, 650);
	scaleObject('rock1', 1.5, 1.5);
	setScrollFactor('rock1', 1, 1);

	makeLuaSprite('rock2', 'boil/hell_rock_2', 875, 650);
	scaleObject('rock2', 1.5, 1.5);
	setScrollFactor('rock2', 1, 1);

	makeLuaSprite('platform2', 'LAVA OVERLAY IN GAME', -700, -300);
    scaleObject('platform2', 1.5, 1.5)

	makeAnimatedLuaSprite('bubbles', 'firebubbles', -200, 400)
	addAnimationByPrefix('bubbles', 'woah', 'Fire Overlay', 24, true)
	objectPlayAnimation('bubbles', 'woah', false)

	addLuaSprite('back');
	addLuaSprite('lava1');
	addLuaSprite('lava2');
	addLuaSprite('rock1');
	addLuaSprite('rock2');
	addLuaSprite('platform2', true)
	addLuaSprite('bubbles', true)
end

function onStepHit()
    if curStep == 1568 then
	makeLuaSprite('grid', 'grid', -100, 0);
    addLuaSprite('grid',true)
    setObjectCamera('grid', 'hud')
    scaleObject('grid', 0.6, 0.6)
    doTweenAlpha('woah2', 'grid', 0.5, 0.5, 'linear')
    setBlendMode('grid', 'add')
    end
end