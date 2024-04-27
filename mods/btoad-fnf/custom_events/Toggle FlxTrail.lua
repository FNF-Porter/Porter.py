local charManagement = {
	-- Currently WIP
	names = {'dad', 'gf', 'boyfriend'},
	singChecks = {}
}

---@param text1 any
---@param text2 any
---@param text3 any
---@param text4 any
---@param text5 any
local function subPrint(text1, text2, text3, text4, text5)
	debugPrint(text1, text2, text3, text4, text5)
end

---@param char string
---@return boolean
local function doesCharExist(char)
	for index, value in pairs(charManagement.names) do
		if char == value then
			return true
		-- else
		-- 	debugPrint('The character "' .. char .. '" does not exist in the rendered listing.')
		-- 	return false
		end
	end
end

local bigStuff = {}
for index, value in pairs(charManagement.names) do
	bigStuff = {
		-- Important Trail Things
		trailEnabled = {[value] = false},
		timerStarted = {[value] = false},
		curTrail = {[value] = 0},
		
		-- Color Stuff
		curColor = {[value] = 'ffffff'},
		isDefColor = {[value] = true},
		defaultColor = {[value] = 'ffffff'},
		
		-- Options
		colorSync = {[value] = false},
		velocityLooksCool = {[value] = false},
		flying = {[value] = false}
	}
end

local trail = {
	length = lowQuality and 3 or 5,
	delay = lowQuality and 0.03 or 0.05
}

local gfNote

local strumStuff = {
	opponent = {
		fromGetProperty = 'NOTE_assets',
		noDirectory = 'NOTE_assets'
	},
	player = {
		fromGetProperty = 'NOTE_assets',
		noDirectory = 'NOTE_assets'
	},
	arrowSkin = 'NOTE_assets'
}
local colorManagement = {
	opponent = {
		left = '',
		down = '',
		up = '',
		right = '',
		hasIdle = false,
		idle = '',
		state = {
			idle = '',
			['left'] = '',
			['down'] = '',
			['up'] = '',
			['right'] = ''
		}
	},
	player = {
		left = '',
		down = '',
		up = '',
		right = '',
		hasIdle = false,
		idle = '',
		state = {
			idle = '',
			['left'] = '',
			['down'] = '',
			['up'] = '',
			['right'] = ''
		}
	}
}

function onCreatePost()
	strumStuff.arrowSkin = getPropertyFromClass('PlayState', 'SONG.strumStuff.arrowSkin')
	strumStuff.arrowSkin = ((strumStuff.arrowSkin == nil or strumStuff.arrowSkin == '' or strumStuff.arrowSkin == 'SONG.strumStuff.arrowSkin') and 'NOTE_assets' or strumStuff.arrowSkin)
	if (strumStuff.opponent.fromGetProperty == '' or strumStuff.opponent.fromGetProperty == nil) or (strumStuff.arrowSkin == '' or strumStuff.arrowSkin == nil) then
		strumStuff.opponent.noDirectory = 'NOTE_assets'
	end
	if (strumStuff.player.fromGetProperty == '' or strumStuff.player.fromGetProperty == nil) or (strumStuff.arrowSkin == '' or strumStuff.arrowSkin == nil) then
		strumStuff.player.noDirectory = 'NOTE_assets'
	end

	for index, value in pairs(charManagement.names) do
		triggerEvent('Change FlxTrail Color', value, 'default')
	end
end

function onUpdatePost()
	local fileDirectory = 'custom_events/FlxTrail Stuff/'
	for index, value in pairs(charManagement.names) do
		if flashingLights == false then
			bigStuff.velocityLooksCool[value] = false
		end
		bigStuff.defaultColor[value] = rgbToHex(getProperty(value .. '.healthColorArray'))
		if bigStuff.isDefColor[value] then
			bigStuff.curColor[value] = bigStuff.defaultColor[value]
		end
	end

	-- Opponent Strums
	for i = 0, getProperty('opponentStrums.length')-1 do
		strumStuff.opponent.fromGetProperty = getPropertyFromGroup('opponentStrums', i, 'texture')
		strumStuff.opponent.noDirectory = strumStuff.opponent.fromGetProperty:gsub('.+/', '')
	end
	if (strumStuff.opponent.fromGetProperty == '' or strumStuff.opponent.fromGetProperty == nil) then
		strumStuff.opponent.noDirectory = strumStuff.arrowSkin
	end
	local opponentTxt = readFileLines(fileDirectory .. 'notes/' .. strumStuff.opponent.noDirectory .. '.txt')
	
	colorManagement.opponent.left = opponentTxt[1]
	colorManagement.opponent.down = opponentTxt[2]
	colorManagement.opponent.up = opponentTxt[3]
	colorManagement.opponent.right = opponentTxt[4]
	colorManagement.opponent.hasIdle = toboolean(opponentTxt[5])
	colorManagement.opponent.idle = opponentTxt[6]
	
	if checkFileExists(fileDirectory .. 'notes/' .. strumStuff.opponent.noDirectory .. '.txt') then
		colorManagement.opponent.state.idle = colorManagement.opponent.idle
		colorManagement.opponent.state['left'] = colorManagement.opponent.left
		colorManagement.opponent.state['down'] = colorManagement.opponent.down
		colorManagement.opponent.state['up'] = colorManagement.opponent.up
		colorManagement.opponent.state['right'] = colorManagement.opponent.right
	else
		colorManagement.opponent.state.idle = (gfNote and bigStuff.defaultColor['gf'] or bigStuff.defaultColor['dad'])
		colorManagement.opponent.state['left'] = 'c24b99'
		colorManagement.opponent.state['down'] = '00ffff'
		colorManagement.opponent.state['up'] = '12fa05'
		colorManagement.opponent.state['right'] = 'f9393f'
	end
	
	if colorManagement.opponent.state.idle == 'default' then
		colorManagement.opponent.state.idle = (gfNote and bigStuff.defaultColor['gf'] or bigStuff.defaultColor['dad'])
	end
	
	-- Player Strums
	for i = 0, getProperty('playerStrums.length')-1 do
		strumStuff.player.fromGetProperty = getPropertyFromGroup('playerStrums', i, 'texture')
		strumStuff.player.noDirectory = strumStuff.player.fromGetProperty:gsub('.+/', '')
	end
	if (strumStuff.player.fromGetProperty == '' or strumStuff.player.fromGetProperty == nil) then
		strumStuff.player.noDirectory = strumStuff.arrowSkin
	end
	local playerTxt = readFileLines(fileDirectory .. 'notes/' .. strumStuff.player.noDirectory .. '.txt')
	colorManagement.player.left = playerTxt[1]
	colorManagement.player.down = playerTxt[2]
	colorManagement.player.up = playerTxt[3]
	colorManagement.player.right = playerTxt[4]
	colorManagement.player.hasIdle = toboolean(playerTxt[5])
	colorManagement.player.idle = playerTxt[6]

	if checkFileExists(fileDirectory .. 'notes/' .. strumStuff.player.noDirectory .. '.txt') then
		colorManagement.player.state.idle = colorManagement.player.idle
		colorManagement.player.state['left'] = colorManagement.player.left
		colorManagement.player.state['down'] = colorManagement.player.down
		colorManagement.player.state['up'] = colorManagement.player.up
		colorManagement.player.state['right'] = colorManagement.player.right
	else
		colorManagement.player.state.idle = (gfNote and bigStuff.defaultColor['gf'] or bigStuff.defaultColor['boyfriend'])
		colorManagement.player.state['left'] = 'c24b99'
		colorManagement.player.state['down'] = '00ffff'
		colorManagement.player.state['up'] = '12fa05'
		colorManagement.player.state['right'] = 'f9393f'
	end

	if colorManagement.player.state.idle == 'default' then
		colorManagement.player.state.idle = (gfNote and bigStuff.defaultColor['gf'] or bigStuff.defaultColor['boyfriend'])
	end

	local function getCurAnim(char)
		return getProperty(char .. '.animation.curAnim.name')
	end
	local function getIdleSuffix(char)
		return getProperty(char .. '.idleSuffix')
	end

	if colorManagement.opponent.hasIdle and bigStuff.colorSync['dad'] then
		if getCurAnim('dad') == 'idle' .. getIdleSuffix('dad') or getCurAnim('dad') == 'danceLeft' .. getIdleSuffix('dad') or getCurAnim('dad') == 'danceRight' .. getIdleSuffix('dad') then
			triggerEvent('Change FlxTrail Color', 'dad', colorManagement.opponent.state.idle)
		end
	end
	if (colorManagement.opponent.hasIdle or colorManagement.player.hasIdle) and bigStuff.colorSync['gf'] then
		if getCurAnim('gf') == 'idle' .. getIdleSuffix('gf') or getCurAnim('gf') == 'danceLeft' .. getIdleSuffix('gf') or getCurAnim('gf') == 'danceRight' .. getIdleSuffix('gf') then
			triggerEvent('Change FlxTrail Color', 'gf', (colorManagement.player.state.idle or colorManagement.opponent.state.idle))
		end
	end
	if colorManagement.player.hasIdle and bigStuff.colorSync['boyfriend'] then
		if getCurAnim('boyfriend') == 'idle' .. getIdleSuffix('boyfriend') or getCurAnim('boyfriend') == 'danceLeft' .. getIdleSuffix('boyfriend') or getCurAnim('boyfriend') == 'danceRight' .. getIdleSuffix('boyfriend') then
			triggerEvent('Change FlxTrail Color', 'boyfriend', colorManagement.player.state.idle)
		end
	end
end

function onEvent(name, value1, value2)
	if name == 'Toggle FlxTrail' then
		for index, value in pairs(charManagement.names) do
			if doesCharExist(value) then
				if value1 == value then
					local theChar = value1
					if value2 == 'on' then
						if not bigStuff.timerStarted[theChar] then
							runTimer('timerTrail' .. theChar, trail.delay, 0)
							bigStuff.timerStarted[theChar] = true
						end
						if not bigStuff.trailEnabled[theChar] then
							bigStuff.trailEnabled[theChar] = true
							bigStuff.curTrail[theChar] = 0
						end
					elseif value2 == 'off' then
						bigStuff.trailEnabled[theChar] = false
						for i = daThings.num - trail.length, daThings.num do
							removeLuaSprite('trailFrame' .. theChar .. i, true)
						end
					end
				end
			end
		end
	end
	
	if name == 'Toggle FlxTrail Options' then
		local valueContents = {v1 = {}, v2 = {}}
		valueContents.v1 = Split(value1, ',')
		valueContents.v2 = Split(value2, ',')
		
		if valueContents.v1[1] ~= 'config' then
			for index, value in pairs(charManagement.names) do
				if doesCharExist(value) then
					if valueContents.v1[1] == value then
						local theChar = valueContents.v1[1]
						if valueContents.v1[2] == 'colorsync' then
							if valueContents.v2[1] == 'on' then
								bigStuff.colorSync[theChar] = true
							elseif valueContents.v2[1] == 'off' then
								bigStuff.colorSync[theChar] = false
							end
						end
						
						if valueContents.v1[2] == 'blur' then
							if valueContents.v2[1] == 'on' then
								bigStuff.velocityLooksCool[theChar] = true
							elseif valueContents.v2[1] == 'off' then
								bigStuff.velocityLooksCool[theChar] = false
							end
						end
						
						if valueContents.v1[2] == 'fly' then
							if valueContents.v2[1] == 'on' then
								bigStuff.flying[theChar] = true
							elseif valueContents.v2[1] == 'off' then
								bigStuff.flying[theChar] = false
							end
						end
					end
				end
			end
		else
			if valueContents.v1[2] == 'fly' then
				valueContents.v2[3] = noteStuffs.distance
				valueContents.v2[4] = noteStuffs.duration
				valueContents.v2[5] = noteStuffs.ease
			end
		end
	end
	
	if name == 'Change FlxTrail Color' then
		for index, value in pairs(charManagement.names) do
			if doesCharExist(value) then
				if value1 == value then
					local theChar = value1
					if value2 == 'default' then
						bigStuff.isDefColor[theChar] = true
					elseif value2 ~= 'default' then
						bigStuff.isDefColor[theChar] = false	
						bigStuff.curColor[theChar] = ((value2 == '' or value2 == nil) and bigStuff.curColor[theChar] or value2)
					end
				end
			end
		end
	end
end

function onTimerCompleted(tag, loops, loopsLeft)
	for index, value in pairs(charManagement.names) do
		if tag == 'timerTrail' .. value then
			createTrailFrame(value)
		end
	end
end

daThings = {
	num = 0,
	color = 'ffffff',
	image = 'characters/BOYFRIEND',
	frame = 'boyfriend idle dance',
	x = 0,
	y = 0,
	scaleX = 0,
	scaleY = 0,
	scrollX = 0,
	scrollY = 0,
	offsetX = 0,
	offsetY = 0,
	originX = 0,
	originY = 0,
	accelerationX = 0,
	accelerationY = 0,
	flipX = false,
	flipY = false,
	alpha = 0.6,
	visible = true,
	-- cameras = 'camGame',
	antialiasing = false
}

---@param char string
---@return number
local function getThingOrder(char)
	return getObjectOrder(char .. ((char == 'dad' or char == 'gf' or char == 'boyfriend') and 'Group' or ''))
end

---@param tag string
function createTrailFrame(tag)
	if bigStuff.trailEnabled[tag] then
		daThings.num = bigStuff.curTrail[tag]
		bigStuff.curTrail[tag] = bigStuff.curTrail[tag] + 1
		if bigStuff.curColor[tag] == 'default' then
			bigStuff.curColor[tag] = bigStuff.defaultColor[tag]
		end
		daThings.color = getColorFromHex(bigStuff.curColor[tag])
		daThings.image = getProperty(tag .. '.imageFile')
		daThings.frame = getProperty(tag .. '.animation.frameName')
		daThings.x = getProperty(tag .. '.x')
		daThings.y = getProperty(tag .. '.y')
		daThings.scaleX = getProperty(tag .. '.scale.x')
		daThings.scaleY = getProperty(tag .. '.scale.y')
		daThings.scrollX = getProperty(tag .. '.scrollFactor.x')
		daThings.scrollY = getProperty(tag .. '.scrollFactor.y')
		daThings.offsetX = getProperty(tag .. '.offset.x')
		daThings.offsetY = getProperty(tag .. '.offset.y')
		daThings.originX = getProperty(tag .. '.origin.x')
		daThings.originY = getProperty(tag .. '.origin.y')
		daThings.accelerationX = getProperty(tag .. '.acceleration.x')
		daThings.accelerationY = getProperty(tag .. '.acceleration.y')
		daThings.flipX = getProperty(tag .. '.flipX')
		daThings.flipY = getProperty(tag .. '.flipY')
		daThings.alpha = getProperty(tag .. '.alpha')
		daThings.visible = getProperty(tag .. '.visible')
		-- daThings.cameras = getProperty(tag .. '.cameras[0]')
		daThings.antialiasing = getProperty(tag .. '.antialiasing')
	end
	
	if daThings.num - trail.length + 1 >= 0 and trailTag.erased == false then
		for i = (daThings.num - trail.length + 1), (daThings.num - 1) do
			setProperty('trailFrame' .. tag .. i .. '.alpha', getProperty('trailFrame' .. tag .. i .. '.alpha') - (trail.length * 0.01))
		end
	end
	
	if daThings.image ~= '' or daThings.image ~= nil then
		trailTag = {
			TAG = tag,
			name = 'trailFrame' .. tag,
			full = 'trailFrame' .. tag .. daThings.num,
			erased = false
		}
		local velocityStuffs = {
			lowQuality and getRandomInt(-50, 50) or getRandomFloat(-100, 100),
			lowQuality and getRandomInt(-50, 50) or getRandomFloat(-100, 100)
		}
		makeAnimatedLuaSprite(trailTag.full, daThings.image, daThings.x, daThings.y)
		setPropertyXY(trailTag.full .. '.scale', daThings.scaleX, daThings.scaleY)
		setScrollFactor(trailTag.full, daThings.scrollX, daThings.scrollY)
		setPropertyXY(trailTag.full .. '.offset', daThings.offsetX, daThings.offsetY)
		setPropertyXY(trailTag.full .. '.origin', daThings.originX, daThings.originY)
		setPropertyXY(trailTag.full .. '.acceleration', daThings.accelerationX, daThings.accelerationY)
		setProperty(trailTag.full .. '.flipX', daThings.flipX)
		setProperty(trailTag.full .. '.flipY', daThings.flipY)
		setProperty(trailTag.full .. '.alpha', daThings.alpha - 0.4)
		setProperty(trailTag.full .. '.visible', daThings.visible)
		-- setProperty(trailTag.full .. '.cameras[0]', daThings.cameras)
		setProperty(trailTag.full .. '.antialiasing', daThings.antialiasing)
		setProperty(trailTag.full .. '.color', daThings.color)
		setPropertyXY(trailTag.full .. '.velocity', bigStuff.velocityLooksCool[tag] and velocityStuffs[1] or 0, bigStuff.velocityLooksCool[tag] and velocityStuffs[2] or 0)
		setObjectOrder(trailTag.full, getThingOrder(tag) + 0.1)
		setBlendMode(trailTag.full, 'add')
		addAnimationByPrefix(trailTag.full, 'stuff', daThings.frame, 0, false)
		addLuaSprite(trailTag.full, false)

		removeLuaSprite('trailFrame' .. tag .. (daThings.num - trail.length), true)
		if getProperty(trailTag.full .. '.alpha') <= (lowQuality and (daThings.alpha - 0.55) or 0) or getProperty(trailTag.full .. '.visible') == false then
			removeLuaSprite(trailTag.full, true)
			trailTag.erased = true
		else
			trailTag.erased = false
		end
	end
end

---@param variable string
---@param valueX any
---@param valueY any
function setPropertyXY(variable, valueX, valueY)
	setProperty(variable .. '.x', valueX)
	setProperty(variable .. '.y', valueY)
end

noteStuffs = {
	directions = {'left', 'down', 'up', 'right'},
	distance = 100,
	duration = 0.7,
	ease = 'elasticOut'
}

local function noteDataConverter(noteData, maniaVar) -- thinking of using
	if maniaVar == 1 then
		if noteData == 0 then return 2 end

	elseif maniaVar == 2 then
		if noteData == 0 then return 1 end
		if noteData == 1 then return 2 end

	elseif maniaVar == 3 then
		if noteData == 0 then return 0 end
		if noteData == 1 then return 2 end
		if noteData == 2 then return 3 end

	elseif maniaVar == 4 or maniaVar == nil then
		-- if noteData == 0 then return 0 end
		-- if noteData == 1 then return 1 end
		-- if noteData == 2 then return 2 end
		-- if noteData == 3 then return 3 end
		return noteData

	elseif maniaVar == 5 then
		if noteData == 0 then return 0 end
		if noteData == 1 then return 1 end
		if noteData == 2 then return 2 end
		if noteData == 3 then return 2 end
		if noteData == 4 then return 3 end

	elseif maniaVar == 6 then
		if noteData == 0 then return 0 end
		if noteData == 1 then return 2 end
		if noteData == 2 then return 3 end
		if noteData == 3 then return 0 end
		if noteData == 4 then return 1 end
		if noteData == 5 then return 3 end

	elseif maniaVar == 7 then
		if noteData == 0 then return 0 end
		if noteData == 1 then return 2 end
		if noteData == 2 then return 3 end
		if noteData == 3 then return 2 end
		if noteData == 4 then return 0 end
		if noteData == 5 then return 1 end
		if noteData == 6 then return 3 end

	elseif maniaVar == 8 then
		if noteData == 0 then return 0 end
		if noteData == 1 then return 1 end
		if noteData == 2 then return 2 end
		if noteData == 3 then return 3 end
		if noteData == 4 then return 0 end
		if noteData == 5 then return 1 end
		if noteData == 6 then return 2 end
		if noteData == 7 then return 3 end

	elseif maniaVar == 9 then
		if noteData == 0 then return 0 end
		if noteData == 1 then return 1 end
		if noteData == 2 then return 2 end
		if noteData == 3 then return 3 end
		if noteData == 4 then return 2 end
		if noteData == 5 then return 0 end
		if noteData == 6 then return 1 end
		if noteData == 7 then return 2 end
		if noteData == 8 then return 3 end
	end
end

-- dad
function opponentNoteHit(membersIndex, noteData, noteType, isSustainNote)
	gfNote = getPropertyFromGroup('notes', membersIndex, 'gfNote')
	if gfNote then
		gfNoteHit(membersIndex, noteData, noteType, isSustainNote, true, false)
	else
		if bigStuff.colorSync['dad'] then
			triggerEvent('Change FlxTrail Color', 'dad', colorManagement.opponent.state[noteStuffs.directions[noteData + 1]])
			changeTrailHSB('dad', membersIndex)
		end
		if bigStuff.flying['dad'] then
			flyCool('dad', noteData)
		end
	end
end

-- gf
function gfNoteHit(membersIndex, noteData, noteType, isSustainNote, dad, missed)
	if missed == false then
		if bigStuff.colorSync['gf'] then
			triggerEvent('Change FlxTrail Color', 'gf', dad and colorManagement.opponent.state[noteStuffs.directions[noteData + 1]] or colorManagement.player.state[noteStuffs.directions[noteData + 1]])
			changeTrailHSB('gf', membersIndex)
		end
		if bigStuff.flying['gf'] then
			flyCool('gf', noteData)
		end
	end
end

-- boyfriend
function goodNoteHit(membersIndex, noteData, noteType, isSustainNote)
	gfNote = getPropertyFromGroup('notes', membersIndex, 'gfNote')
	if gfNote then
		gfNoteHit(membersIndex, noteData, noteType, isSustainNote, false, false)
	else
		if bigStuff.colorSync['boyfriend'] then
			triggerEvent('Change FlxTrail Color', 'boyfriend', colorManagement.player.state[noteStuffs.directions[noteData + 1]])
			changeTrailHSB('boyfriend', membersIndex)
		end
		if bigStuff.flying['boyfriend'] then
			flyCool('boyfriend', noteData)
		end
	end
end

---@param tag string
---@param membersIndex number
function changeTrailHSB(tag, membersIndex)
	if lowQuality == false then
		local hue = getPropertyFromGroup('notes', membersIndex, 'colorSwap.hue')
		local saturation = getPropertyFromGroup('notes', membersIndex, 'colorSwap.saturation')
		local brightness = getPropertyFromGroup('notes', membersIndex, 'colorSwap.brightness')
		runHaxeCode([[
			var newTrailHSB]] .. membersIndex .. [[ = new ColorSwap();
			game.getLuaObject(']] .. (trailTag.name .. tag) .. [[').shader = newTrailHSB]] .. membersIndex .. [[.shader;
			colorSwap.hue = ]] .. hue .. [[;
			colorSwap.saturation = ]] .. saturation .. [[;
			colorSwap.brightness = ]] .. brightness .. [[;
		]])
	end
end

function noteRegistry(membersIndex, noteData, noteType, isSustainNote, tag, dad, missed)
	-- this will probably not even be used lmao
end

-- Custom Functions
---@param rgb table
---@return hex
function rgbToHex(rgb) -- https://www.codegrepper.com/code-examples/lua/rgb+to+hex+lua
	return string.format('%02x%02x%02x', math.floor(rgb[1]), math.floor(rgb[2]), math.floor(rgb[3]))
end -- color stuffs not by cherry anymore idr who tho

---@param directory string
---@return table.string
function readFileLines(directory)
	-- thx super
	local file = getTextFromFile(directory)
	local fLines = {}
	for i in string.gmatch(file, '([^\n]+)') do
		table.insert(fLines, i)
	end
	return fLines
end

---@param str string
---@return boolean
function toboolean(str) -- WORK DAMMIT
	-- maru thx
	local bool = false
	bool = (tostring(str:lower()) == 'true' and true or false)
	return bool
end

---@param tag string
---@param noteData number
function flyCool(tag, noteData)
	if trailTag.erased == false then
		-- For "bigStuff.flying"!
		if noteData == 0 then
			doTweenX('fly' .. tag .. 'left' .. daThings.num, 'trailFrame' .. tag .. daThings.num, getProperty(tag .. '.x') - noteStuffs.distance, noteStuffs.duration / playbackRate, noteStuffs.ease)
		elseif noteData == 1 then
			doTweenY('fly' .. tag .. 'down' .. daThings.num, 'trailFrame' .. tag .. daThings.num, getProperty(tag .. '.y') + noteStuffs.distance, noteStuffs.duration / playbackRate, noteStuffs.ease)
		elseif noteData == 2 then
			doTweenY('fly' .. tag .. 'up' .. daThings.num, 'trailFrame' .. tag .. daThings.num, getProperty(tag .. '.y') - noteStuffs.distance, noteStuffs.duration / playbackRate, noteStuffs.ease)
		elseif noteData == 3 then
			doTweenX('fly' .. tag .. 'right' .. daThings.num, 'trailFrame' .. tag .. daThings.num, getProperty(tag .. '.x') + noteStuffs.distance, noteStuffs.duration / playbackRate, noteStuffs.ease)
		end
	end
end

---@param s string
---@param delimiter string
---@return table.string
function Split(s, delimiter)
	-- cool stuff Unholy
	local result = {}
	for match in (s..delimiter):gmatch('(.-)'..delimiter) do
		table.insert(result, tostring(stringTrim(match)))
	end
	return result
end