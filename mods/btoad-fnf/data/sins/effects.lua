local function tohex(rgb)
    return string.format("%x", (rgb[1] * 0x10000) + (rgb[2] * 0x100) + rgb[3])
end
local RGB = function(hex)
    local mul = 0
    local a = 255
    if string.find(hex, "0x") then
        mul = 4
        a = tonumber("0x" .. hex:sub(3, 4))
    end
    local r = tonumber("0x" .. hex:sub(1 + mul, 2 + mul))
    local g = tonumber("0x" .. hex:sub(3 + mul, 4 + mul))
    local b = tonumber("0x" .. hex:sub(5 + mul, 6 + mul))
    return r, g, b, a
end

local function setColorTransform(object, redMult, greenMult, blueMult, alphaMult, redOff, greenOff, blueOff, alphaOff)
    local function set(k, v)
        setProperty(object .. "." .. k, v)
    end
    local function get(k)
        return getProperty(object .. "." .. k)
    end

    local hex =
        tohex(
        {
            math.max(math.floor(redMult * 255), 255),
            math.max(math.floor(greenMult * 255), 255),
            math.max(math.floor(blueMult * 255), 255)
        }
    )
    local color = bit.tobit(tonumber("0xff" .. hex))

    set("color", bit.band(color, 0xffffff))
    set("alpha", alphaMult)

    set("colorTransform.redMultiplier", redMult)
    set("colorTransform.greenMultiplier", greenMult)
    set("colorTransform.blueMultiplier", blueMult)
    set("colorTransform.alphaMultiplier", alphaMult)

    set("colorTransform.redOffset", redOff)
    set("colorTransform.greenOffset", greenOff)
    set("colorTransform.blueOffset", blueOff)
    set("colorTransform.alphaOffset", alphaOff)

    set("useColorTransform", get("alpha") ~= 1 or get(color) ~= 0xffffff)
    set("dirty", true)
end


local function dyeObject(object, hex)
    local r, g, b, a = RGB(hex)
    setColorTransform(object, 0, 0, 0, 1, r, g, b, a)
end
local fillObject = dyeObject

local effects = {
    coolBlueEffect = function(object) -- aka night time effect
        setColorTransform(object, 0.2, 0.6, 1, 1, 0, 0, 0, 0)
    end,
    cyberPunkEffect = function(object)
        setColorTransform(object, 1, 0, 0.8, 1, 0, 128, 0, 0)
    end,
    desaturateObject = function(object)
        setColorTransform(object, 0.3, 0.59, 0.11, 1, 0, 0, 0, 0)
    end,
    dustyRoseEffect = function(obj)
        setColorTransform(obj, 0.9, 0.3, 0.2, 1, 204, 119, 136, 255)
    end,
    heatmapEffect = function(object)
        setColorTransform(object, 1, 0, 0, 1, 0, 128, 255, 0)
    end,
    invertObject = function(object)
        local function get(k)
            return getProperty(object .. "." .. k)
        end
        setColorTransform(
            object,
            get("colorTransform.redMultiplier") * -1,
            get("colorTransform.greenMultiplier") * -1,
            get("colorTransform.blueMultiplier") * -1,
            1,
            255 - get("colorTransform.redOffset"),
            255 - get("colorTransform.greenOffset"),
            255 - get("colorTransform.blueOffset"),
            0
        )
    end,
    MinusinvertObject = function(object)
        setColorTransform(object, -1, -1, -1, 1, 255, 255, 255, 0)
    end,
    neonEffect = function(object)
        setColorTransform(object, 1, 1, 1, 1, 0, 255, 0, 0)
    end,
    nightVisionEffect = function(object)
        setColorTransform(object, 0.5, 0.5, 0.5, 1, 0, 255, 0, 0)
    end,
    sepiaEffect = function(object)
        setColorTransform(object, 0.393, 0.769, 0.189, 1, 66, 66, 0, 0)
    end,
    sinCityEffect = function(object)
        setColorTransform(object, 1, 0, 0, 1, 0, 0, 0, 0)
    end,
    streetLightEffect = function(object)
        setColorTransform(object, 0.9, 0.3, 0.2, 1, 0, 0, 55, 255)
    end,
    sunsetEffect = function(object, strength) -- strength is a value between 0 and 1
        strength = (strength == nil and 0.8 or 1 - strength)
        setColorTransform(object, 1, strength, 0.2, 1, 102, 0, 102, 0)
    end,
    vintageEffect = function(object)
        setColorTransform(object, 0.9, 0.5, 0.2, 1, 35, 35, 35, 0)
    end
}

function onCreatePost()
    effects.coolBlueEffect('boyfriend')
end