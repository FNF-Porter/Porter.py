--[[ github.com/cyn0x8/neocam ]]

-- global vars

locked_pos = false
pos_speed = 8

note_offset = true
offset_radius = 8
shake_fps = 24

locked_zoom = false
zoom_speed = 2

freeze = false

-- internal vars

local min = math.min
local max = math.max
local function lerp(start, goal, alpha) return start + (goal - start) * alpha end
local function trim(s) return s:match("^%s*(.-)%s*$") end
local function get_cam(cam)
	cam = trim(cam):lower()
	return (cam == "h" or cam == "hud" or cam == "camhud") and "h" or "g"
end

local targets = {}
local cur = {x = 0, y = 0}
local offset = {{x = 0, y = 0}, {x = 0, y = 0}}
local shaking = {g = {x = 0, y = 0}, h = {x = 0, y = 0}, t = 0}
local zooms = {g = 1, h = 1}
local bumping = {mod = 4, a = {g = 1, h = 2}}

-- global functions

function set_target(tag, x, y)
	targets[trim(tag)] = {
		x = tonumber(x) or 0,
		y = tonumber(y) or 0
	}
end

function focus(tag, duration, ease, lock)
	local target = targets[trim(tag)]
	if target then
		if lock == false then
			locked_pos = lock
		end
		
		if not locked_pos then
			if lock == true then
				locked_pos = lock
			end
			
			duration = tonumber(duration) or 0
			ease = ease or "linear"
			
			if duration <= 0.01 then
				cancelTween("ncfx")
				cancelTween("ncfy")
				setProperty("ncf.x", target.x)
				setProperty("ncf.y", target.y)
			else
				doTweenX("ncfx", "ncf", target.x, duration, ease)
				doTweenY("ncfy", "ncf", target.y, duration, ease)
			end
		end
	end
end

function snap_target(tag)
	local target = targets[trim(tag)]
	if target then
		cur = {
			x = target.x,
			y = target.y
		}
		
		setProperty("camGame.scroll.x", cur.x - screenWidth / 2)
		setProperty("camGame.scroll.y", cur.y - screenHeight / 2)
		setProperty("ncf.x", cur.x)
		setProperty("ncf.y", cur.y)
	end
end

function shake(cam, x, y, duration, ease)
	cam = get_cam(cam)
	duration = tonumber(duration) or 0
	ease = ease or "linear"
	
	x = tonumber(x)
	if x then
		shaking[cam].x = x * (getRandomInt(1, 2) * 2 - 3)
		
		cancelTween("ncs" .. cam .. "x")
		setProperty("ncs" .. cam .. ".x", x)
		
		if duration > 0.01 and x ~= 0 then
			doTweenX("ncs" .. cam .. "x", "ncs" .. cam, 0, duration, ease)
		end
	end
	
	y = tonumber(y)
	if y then
		shaking[cam].y = y * (getRandomInt(1, 2) * 2 - 3)
		
		cancelTween("ncs" .. cam .. "y")
		setProperty("ncs" .. cam .. ".y", y)
		
		if duration > 0.01 and y ~= 0 then
			doTweenY("ncs" .. cam .. "y", "ncs" .. cam, 0, duration, ease)
		end
	end
end

function bump(cam, amount)
	cam = get_cam(cam)
	amount = tonumber(amount) or 0
	
	zooms[cam] = zooms[cam] + amount * 0.015
end

function bump_speed(modulo, amount_game, amount_hud)
	bumping = {
		mod = tonumber(modulo) or 4,
		a = {
			g = tonumber(amount_game) or 1,
			h = tonumber(amount_hud) or 2
		}
	}
end

function zoom(cam, amount, duration, ease, lock)
	if lock == false then
		locked_zoom = lock
	end
	
	if not locked_zoom then
		if lock == true then
			locked_zoom = lock
		end
		
		cam = get_cam(cam)
		amount = max(tonumber(amount) or (cam == "g" and getProperty("defaultCamZoom") or 1), 0)
		duration = duration or 0
		ease = ease or "linear"
		
		if duration <= 0.01 then
			cancelTween("ncz" .. cam)
			setProperty("ncz" .. cam .. ".x", amount)
		else
			doTweenX("ncz" .. cam, "ncz" .. cam, amount, duration, ease)
		end
	end
end

function snap_zoom(cam, amount)
	cam = get_cam(cam)
	amount = max(tonumber(amount) or (cam == "g" and getProperty("defaultCamZoom") or 1), 0)
	
	zooms[cam] = amount
	cancelTween("ncz" .. cam)
	setProperty("ncz" .. cam .. ".x", amount)
end

-- internal functions

function onCreate()
	runHaxeCode([[
		function assert_gf() {
			return game.gf != null;
		}
	]])
end

function onCreatePost()
	if not targets.opp then
		set_target("opp",
			getMidpointX("dad") + 150 + getProperty("dad.cameraPosition[0]") + getProperty("opponentCameraOffset[0]"),
			getMidpointY("dad") - 100 + getProperty("dad.cameraPosition[1]") + getProperty("opponentCameraOffset[1]")
		)
	end
	
	if not targets.plr then
		set_target("plr",
			getMidpointX("boyfriend") - 100 - getProperty("boyfriend.cameraPosition[0]") + getProperty("boyfriendCameraOffset[0]"),
			getMidpointY("boyfriend") - 100 + getProperty("boyfriend.cameraPosition[1]") + getProperty("boyfriendCameraOffset[1]")
		)
	end
	
	if not targets.center then
		set_target("center",
			(targets.opp.x + targets.plr.x) / 2,
			(targets.opp.y + targets.plr.y) / 2
		)
	end
	
	if runHaxeFunction("assert_gf") and not targets.gf then
		set_target("gf",
			getMidpointX("gf") + getProperty("gf.cameraPosition[0]") + getProperty("girlfriendCameraOffset[0]"),
			getMidpointY("gf") + getProperty("gf.cameraPosition[1]") + getProperty("girlfriendCameraOffset[1]")
		)
	end
	
	makeLuaSprite("ncf", "", 0, 0)
	snap_target("center")
	setProperty("isCameraOnForcedPos", true)
	
	makeLuaSprite("ncsg", "", 0, 0)
	makeLuaSprite("ncsh", "", 0, 0)
	
	zooms.g = getProperty("defaultCamZoom")
	makeLuaSprite("nczg", "", zooms.g, 0)
	makeLuaSprite("nczh", "", 1, 0)
end

function onSongStart()
	focus(gfSection and "gf" or (mustHitSection and "plr" or "opp"), 1.25, "cubeout")
	bump("game", bumping.a.g)
	bump("hud", bumping.a.h)
end

function onSectionHit()
	focus(gfSection and "gf" or (mustHitSection and "plr" or "opp"), 1.25, "cubeout")
end

function onStepHit()
	if curStep % (bumping.mod * 4) == 0 then
		bump("game", bumping.a.g)
		bump("hud", bumping.a.h)
	end
end

local function follow_note(dir)
	if not note_offset then
		offset[1] = {
			x = 0,
			y = 0
		}
	else
		local horizontal = dir == 0 or dir == 3
		offset[1] = {
			x = horizontal and (dir == 0 and -offset_radius or offset_radius) or 0,
			y = horizontal and 0 or (dir == 1 and offset_radius or -offset_radius)
		}
	end
end

function goodNoteHit(id, dir)
	if mustHitSection and not getPropertyFromGroup("notes.members", id, "noAnimation") then
		follow_note(dir)
	end
end

function opponentNoteHit(id, dir)
	if not mustHitSection and not getPropertyFromGroup("notes.members", id, "noAnimation") then
		follow_note(dir)
	end
end

local events = {
	nc_bump_speed = function(modulo, amounts)
		local amount_game, amount_hud = amounts:match("([^,]+),([^,]+)")
		bump_speed(modulo, amount_game, amount_hud)
	end,
	
	nc_bump = function(amount_game, amount_hud)
		bump("game", amount_game)
		bump("hud", amount_hud)
	end,
	
	nc_focus = function(tag, params)
		local duration, ease, lock = params:match("([^,]+),([^,]+),([^,]+)")
		focus(tag, duration, lock and (trim(lock):lower() == "true") or nil)
	end,
	
	nc_shake_game = function(pos, params)
		local x, y = params:match("([^,]+),([^,]+)")
		local duration, ease = params:match("([^,]+),([^,]+)")
		shake("game", x, y, duration, ease)
	end,
	
	nc_shake_hud = function(pos, params)
		local x, y = params:match("([^,]+),([^,]+)")
		local duration, ease = params:match("([^,]+),([^,]+)")
		shake("hud", x, y, duration, ease)
	end,
	
	nc_zoom_game = function(amount, params)
		local duration, ease, lock = params:match("([^,]+),([^,]+),([^,]+)")
		zoom("game", amount, duration, ease, lock and (trim(lock):lower() == "true") or nil)
	end,
	
	nc_zoom_hud = function(amount, params)
		local duration, ease, lock = params:match("([^,]+),([^,]+),([^,]+)")
		zoom("hud", amount, duration, ease, lock and (trim(lock):lower() == "true") or nil)
	end,
	
	nc_snap_zoom = function(cam, amount)
		snap_zoom(cam, amount)
	end,
}

function onEvent(tag, v1, v2)
	if events[tag] then
		events[tag](v1, v2)
	end
end

function onUpdatePost(elapsed)
	if not freeze then
		local alpha = min(max(elapsed * pos_speed, 0), 1)
		
		if not note_offset then
			offset[1] = {
				x = 0,
				y = 0
			}
		end
		
		offset[2] = {
			x = lerp(offset[2].x, offset[1].x, alpha),
			y = lerp(offset[2].y, offset[1].y, alpha)
		}
		
		shaking.t = shaking.t + elapsed
		if shaking.t > 1 / shake_fps then
			shaking = {
				g = {
					x = getRandomInt(-1, 1) * getProperty("ncsg.x"),
					y = getRandomInt(-1, 1) * getProperty("ncsg.y")
				},
				
				h = {
					x = getRandomInt(-1, 1) * getProperty("ncsh.x"),
					y = getRandomInt(-1, 1) * getProperty("ncsh.y")
				},
				
				t = shaking.t % (1 / shake_fps)
			}
		end
		
		cur = {
			x = lerp(cur.x, getProperty("ncf.x") + offset[2].x, alpha),
			y = lerp(cur.y, getProperty("ncf.y") + offset[2].y, alpha)
		}
		
		alpha = min(max(elapsed * zoom_speed, 0), 1)
		zooms.g = lerp(zooms.g, getProperty("nczg.x"), alpha)
		zooms.h = lerp(zooms.h, getProperty("nczh.x"), alpha)
		
		setProperty("camGame.followLerp", 0)
		
		setProperty("camGame.scroll.x", cur.x + shaking.g.x - screenWidth / 2)
		setProperty("camGame.scroll.y", cur.y + shaking.g.y - screenHeight / 2)
		setProperty("camGame.zoom", zooms.g)
		
		setProperty("camHUD.x", shaking.h.x)
		setProperty("camHUD.y", shaking.h.y)
		setProperty("camHUD.zoom", zooms.h)
	end
end

function onGameOverStart()
	freeze = true
end