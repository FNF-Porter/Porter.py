-- Event notes hooks
function onEvent(name, value1)
	if name == 'Add Overlay' then
		makeLuaSprite(value1, value1, 0, 0)
		setProperty(value1.alpha, 1);
		addLuaSprite(value1, true)
		setObjectCamera(value1, 'hud')
	end
end