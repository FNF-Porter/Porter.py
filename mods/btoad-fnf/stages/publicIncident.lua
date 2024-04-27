function onCreatePost()
	setProperty('camHUD.alpha', 0.82)
	-- people ew
	makeAnimatedLuaSprite('boof', 'pi/boof', 500, 630);
	addAnimationByPrefix('boof','oof instance','oof instance',24,true)
	setScrollFactor('boof', 1, 1);
	scaleObject('boof', 1.4, 1.4)

	makeAnimatedLuaSprite('sinn', 'pi/sinn', 1200, 530);
	addAnimationByPrefix('sinn','sinn instance','sinn instance',24,true)
	setScrollFactor('sinn', 1, 1);
	scaleObject('sinn', 1.4, 1.4)

	makeAnimatedLuaSprite('grunt', 'pi/grunt', -160, 420);
	addAnimationByPrefix('grunt','fred instance','fred instance',24,true)
	setScrollFactor('grunt', 1, 1);
	scaleObject('grunt', 1.4, 1.4)

	makeAnimatedLuaSprite('niko', 'pi/niko', 200, 300);
	addAnimationByPrefix('niko','niko instance','niko instance',24,true)
	setScrollFactor('niko', 1, 1);
	scaleObject('niko', 1.4, 1.4)

	makeAnimatedLuaSprite('flip', 'pi/flip', 600, 300);
	addAnimationByPrefix('flip','flip bop instance','flip bop instance',24,true)
	setScrollFactor('flip', 1, 1);
	scaleObject('flip', 1.4, 1.4)

	makeLuaSprite('shygee', 'pi/Shygee', 50, 350);
	setScrollFactor('Shygee', 1, 1);
	scaleObject('shygee', 0.09, 0.09)

	makeLuaSprite('bgBoppa1', 'pi/bgBoppa1', 430, 300);
	setScrollFactor('bgBoppa1', 1, 1);
	scaleObject('bgBoppa1', 0.6, 0.6)

	-- misc
	makeLuaSprite('bg', 'pi/bg', -500, 0);
	setScrollFactor('bg', 1, 1);
	scaleObject('bg', 1.7, 1.7)

	makeLuaSprite('gp', 'pi/garticPhone', 30, 10);
	setObjectCamera('gp', 'camOther')
	scaleObject('gp', 0.05, 0.05)

	makeLuaSprite('garticFlashback', 'pi/garticFlashback', 0, 0);
	setObjectCamera('garticFlashback', 'camHUD');
	scaleObject('garticFlashback', 1.28, 1.23)

	--add sprites
	addLuaSprite('bg');
	addLuaSprite('shygee');
	addLuaSprite('bgBoppa1');
	addLuaSprite('sinn', true);
	addLuaSprite('boof', true);
	addLuaSprite('flip', true);
	addLuaSprite('niko', true);
	addLuaSprite('grunt', true);
	addLuaSprite('gp');
	addLuaSprite('garticFlashback');

	setProperty('garticFlashback.alpha', 0);
end

function onStepHit()
	if curStep == 2080 then
		doTweenAlpha('gartic', 'garticFlashback', 1, 2, 'linear')
	end
end