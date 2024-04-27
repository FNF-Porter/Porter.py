function onCreate()
	-- background shit
	makeLuaSprite('mushroom', 'mushroom', -600, -300);
	setScrollFactor('mushroom', 1, 1);

	addLuaSprite('mushroom', false);

	close(true); --For performance reasons, close this script once the stage is fully loaded, as this script won't be used anymore after loading the stage
end