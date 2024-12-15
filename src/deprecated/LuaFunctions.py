def makeLuaSprite(name, path, x, y):
	return {
		"name": name,
		"path": path,
		"x": x,
		"y": y
	}

def makeAnimatedLuaSprite(name, path, x, y):
	return {
		"name": name,
		"path": path,
		"x": x,
		"y": y
	}

def addAnimationByPrefix(tag, name, prefix, fps, looped = True):
	return {
		{
			"tag": tag,
			"name": name,
			"prefix": prefix,
			"fps": fps,
			"looped": looped
		}
	}

def scaleObject(name, sx, sy, hitbox = False):
	return {
		"name": name,
		"sx": sx,
		"sy": sy,
		"hitbox": hitbox
	}

def FPORTER_missing(*args):
	print(f"boohoo missing callback {args}")

callbacks = {
	"makeLuaSprite": makeLuaSprite,
	"makeAnimatedLuaSprite": makeAnimatedLuaSprite,
	"addAnimationByPrefix": addAnimationByPrefix,
	"scaleObject": scaleObject,
	"FPORTER_missing": FPORTER_missing
}

def get():
	return callbacks