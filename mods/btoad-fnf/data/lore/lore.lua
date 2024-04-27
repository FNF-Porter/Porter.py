local sqrt = math.sqrt
local sin = math.sin
local pi = math.pi
local abs = math.abs

--

local bopping = false
local side = 0

local default_zoom = 1

--

local function phone_ring()
	playAnim("gf", "ring-start", true)
	setProperty("gf.specialAnim", true)
	
	runTimer("ring-mid", 6 / 24)
end

--

function onCreatePost()
	setProperty("camGame.x", -10)
	setProperty("camGame.y", -10)
	setProperty("camGame.width", getProperty("camGame.width") + 20)
	setProperty("camGame.height", getProperty("camGame.height") + 20)
	
	setProperty("dadGroup.x", getProperty("dadGroup.x") + 10)
	setProperty("dadGroup.y", getProperty("dadGroup.y") - 20)
	
	setProperty("gfGroup.x", getProperty("gfGroup.x") - 10)
	setProperty("gfGroup.y", getProperty("gfGroup.y") + 50)
	
	setProperty("bfGroup.x", getProperty("bfGroup.x") + 90)
	setProperty("bfGroup.y", getProperty("bfGroup.y") + 10)
	
	callScript("data/lore/neocam", "set_target", {"init", 640, 435})
	callScript("data/lore/neocam", "snap_target", {"init"})
	
	default_zoom = getProperty("defaultCamZoom")
end

function onSongStart()
	setGlobalFromScript("data/lore/neocam", "pos_speed", 10)
	setGlobalFromScript("data/lore/neocam", "offset_radius", 6)
	setGlobalFromScript("data/lore/neocam", "zoom_speed", 2.5)
	callScript("data/lore/neocam", "bump_speed", {2, 0.75, 1.5})
	callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 1.25, "cubeout"})
	
	callScript("data/lore/neocam", "snap_target", {"init"})
	
	callScript("data/lore/neocam", "set_target", {"opp", 450, 430})
	callScript("data/lore/neocam", "set_target", {"plr", 890, 440})
	callScript("data/lore/neocam", "set_target", {"center", 670, 435})
	callScript("data/lore/neocam", "set_target", {"gf", 710, 420})
end

local beat_stuff = {
	[64] = function()
		bopping = true
		
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.75, "cubeout"})
	end,
	
	[91] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.25, 0.5, "cubeout"})
	end,
	
	[92] = function()
		bopping = false
		
		callScript("data/lore/neocam", "bump_speed", {4, 0.75, 1.5})
	end,
	
	[96] = function()
		bopping = true
		
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.5, "cubeout"})
	end,
	
	[128] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 0.75, "cubeout"})
	end,
	
	[192] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.75, "cubeout"})
	end,
	
	[224] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 0.75, "cubeout"})
	end,
	
	[240] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.75, "cubeout"})
	end,
	
	[252] = function()
		bopping = false
	end,
	
	[256] = function()
		bopping = true
		
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 0.75, "cubeout"})
	end,
	
	[320] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.75, "cubeout"})
	end,
	
	[384] = function()
		bopping = false
		
		callScript("data/lore/neocam", "bump_speed", {2, 0.75, 1.5})
		
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 0.75, "cubeout"})
	end,
	
	[445] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.25, 0.5, "cubeout"})
	end,
	
	[446] = function()
		callScript("data/lore/neocam", "bump_speed", {4, 0.75, 1.5})
	end,
	
	[448] = function()
		bopping = true
		
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.5, "cubeout"})
	end,
	
	[475] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.25, 0.5, "cubeout"})
	end,
	
	[476] = function()
		bopping = false
		
		callScript("data/lore/neocam", "bump_speed", {4, 0.75, 1.5})
	end,
	
	[480] = function()
		bopping = true
		
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.5, "cubeout"})
	end,
	
	[512] = function()
		bopping = false
		
		callScript("data/lore/neocam", "focus", {"gf", 1.25, "cubeout", true})
		callScript("data/lore/neocam", "bump_speed", {2, 0.75, 1.5})
	end,
	
	[516] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.3, 10, "linear"})
		
		phone_ring()
	end,
	
	[524] = function()
		phone_ring()
	end,
	
	[532] = function()
		phone_ring()
	end,
	
	[540] = function()
		phone_ring()
	end,
	
	[543] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[544] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.75, "cubeout"})
	end,
	
	[548] = function()
		phone_ring()
	end,
	
	[556] = function()
		phone_ring()
	end,
	
	[564] = function()
		phone_ring()
	end,
	
	[568] = function()
		playAnim("gf", "singDOWN", true)
	end,
	
	[573] = function()
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.3, 0.5, "cubeout"})
	end,
	
	[576] = function()
		bopping = true
		
		callScript("data/lore/neocam", "focus", {"gf", 1.25, "cubeout", true})
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 0.5, "cubeout"})
	end,
	
	[604] = function()
		bopping = false
		
		callScript("data/lore/neocam", "bump_speed", {1, 0.75, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.3, 0.5, "cubeout"})
	end,
	
	[607] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[608] = function()
		bopping = true
		
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.5, "cubeout"})
	end,
	
	[656] = function()
		callScript("data/lore/neocam", "focus", {"gf", 1.25, "cubeout", true})
	end,
	
	[671] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[688] = function()
		callScript("data/lore/neocam", "focus", {"gf", 1.25, "cubeout", true})
	end,
	
	[703] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[704] = function()
		bopping = false
		
		callScript("data/lore/neocam", "bump_speed", {2, 0.75, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.1, 1.25, "cubeout"})
	end,
	
	[752] = function()
		callScript("data/lore/neocam", "focus", {"gf", 1.25, "cubeout", true})
	end,
	
	[763] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[764] = function()
		bopping = true
		
		callScript("data/lore/neocam", "focus", {"opp", 0.5, "cubeout", true})
		callScript("data/lore/neocam", "bump_speed", {1, 1, 1.5})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom + 0.25, 0.75, "cubeout"})
	end,
	
	[765] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[766] = function()
		callScript("data/lore/neocam", "focus", {"plr", 0.5, "cubeout", true})
	end,
	
	[767] = function()
		setGlobalFromScript("data/lore/neocam", "locked_pos", false)
	end,
	
	[768] = function()
		bopping = false
		
		callScript("data/lore/neocam", "focus", {"gf", 0.5, "cubeout", true})
		callScript("data/lore/neocam", "bump_speed", {4, 1.5, 2})
		callScript("data/lore/neocam", "zoom", {"game", default_zoom, 0.75, "cubeout"})
	end,
	
	[769] = function()
		callScript("data/lore/neocam", "bump_speed", {4, 0, 0})
	end
}

function onBeatHit()
	if beat_stuff[curBeat] then
		beat_stuff[curBeat]()
	end
	
	if bopping then
		side = curBeat % 2 == 0 and 1 or -1
	end
end

local timer_stuff = {
	["ring-mid"] = function()
		playAnim("gf", "ring-mid", true)
		setProperty("gf.specialAnim", true)
		setProperty("gf.skipDance", true)
		
		runTimer("ring-end", crochet / 1000 * 4 - 6 / 24)
	end,
	
	["ring-end"] = function()
		playAnim("gf", "ring-end", true)
		setProperty("gf.specialAnim", true)
		setProperty("gf.skipDance", false)
	end
}

function onTimerCompleted(tag)
	if timer_stuff[tag] then
		timer_stuff[tag]()
	end
end

function onUpdatePost(elapsed)
	if bopping then
		local song_pos = getSongPosition()
		
		local angle = sqrt(abs(sin(song_pos * pi / crochet))) * side
		setProperty("camGame.angle", angle / 3)
		setProperty("camHUD.angle", angle / 6)
	end
end