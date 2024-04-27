function onCreatePost()
	-- background shit
	makeLuaSprite('paintBG', 'paintBG/paintnetBG', -900, -400);
	setScrollFactor('paintBG', 1, 1);
	scaleObject('paintBG', 1.7, 1.7)

	makeLuaSprite('paintFG', 'paintBG/paintnetFG', -900, -400);
	setScrollFactor('paintFG', 1, 1);
	scaleObject('paintFG', 1.7, 1.7)

	makeLuaSprite('eye', 'paintBG/Eye', 100, 700);
	setScrollFactor('eye', 1, 1);
	scaleObject('eye', 2.5, 2.5)

	makeLuaSprite('sponge', 'paintBG/ImSpongebob', 350, 0);
	setObjectCamera('sponge', 'camHUD')
	scaleObject('sponge', 1, 1)

	addLuaSprite('paintBG');
	addLuaSprite('paintFG', true);
	addLuaSprite('eye', true);
	addLuaSprite('sponge')
	-- event
	setProperty('camHUD.alpha', 0);
	setProperty('gf.alpha', 0);
	setProperty('dad.alpha', 0);
	setProperty('paintBG.alpha', 0);
	setProperty('paintFG.alpha', 0);
	setProperty('eye.alpha', 0)
	setProperty('sponge.visible', false)
end

function onCreate()
	setProperty('skipCountdown', true)
end


function onStepHit()
	if curStep == 1 then
		doTweenAlpha('epicTween', 'gf', 1, 5, 'linear')
	elseif curStep == 64 then
		doTweenAlpha('epicTween2', 'eye', 1, 10, 'linear')
	elseif curStep == 160 then
		setProperty('eye.visible', false)
		setProperty('dad.alpha', 1)
	elseif curStep == 178 then
		setProperty('paintBG.alpha', 1)
		setProperty('paintFG.alpha', 1)
	elseif curStep == 192 then
		doTweenAlpha('epicTween3', 'camHUD', 1, 5, 'linear')
	elseif curStep == 1008 then
		setProperty('sponge.visible', true)
		doTweenAlpha('epicTween4', 'sponge', 0, 1.5, 'linear')
	end
end