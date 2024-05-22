import copy
import logging
import psychtobase.src.Constants as Constants
import psychtobase.src.window as window

def convert(stageJSON, assetName, luaProps):
    stageTemplate = copy.deepcopy(Constants.STAGE)

    stageTemplate['cameraZoom'] = stageJSON['defaultZoom']
    stageTemplate['characters']['bf']['position'] = stageJSON['boyfriend']
    stageTemplate['characters']['gf']['position'] = stageJSON['girlfriend']
    stageTemplate['characters']['dad']['position'] = stageJSON['opponent']
    stageTemplate['props'] = luaProps

    stageTemplate['name'] = ' '.join([string.capitalize() for string in assetName.replace('.json', '').split('-')])

    return stageTemplate

def getProps(parentFunc, parentFuncName, luaFilename):
    # onCreate props have a negative z index
    # onCreatePost props have a positive z index
    # if ANY prop has addLuaSprite(tag, TRUE) then the z index increases until it is over 300

    _props = []

    propArr = parentFunc.get('makeLuaSprite', []) + parentFunc.get('makeAnimatedLuaSprite', [])

    for index, pictureProp in enumerate(propArr):
        tag = pictureProp[1]
        sprite = pictureProp[2]

        # Why do I have to add a try except for everything
        posx = 0
        posy = 0

        try:
            posx = pictureProp[3]
            posy = pictureProp[4]
        except:
            logging.error(f'[{luaFilename}] Failed accessing x and y of prop! Did you check if it is defined?')

        call = pictureProp[0]

        z_index = 0 
        if parentFuncName == 'onCreatePost':
            z_index = index
        else:
            z_index = -len(propArr) + index

        animated = False
        if call == 'makeAnimatedLuaSprite':
            animated = True

        _props.append({
            't': tag, # Tag
            's': sprite, # Sprite
            'x': posx, # X
            'y': posy, # Y
            'z': z_index, # Z index
            'a': animated, # Animated
            'as': [] # Animations
        })

    for animationAdd in parentFunc.get('addAnimationByPrefix', []):
        tag = animationAdd[1]
        animName = animationAdd[2]
        prefix = animationAdd[3]
        fps = 24
        loop = True

        if len(animationAdd) >= 5:
            fps = animationAdd[4]
        if len(animationAdd) >= 6:
            loop = animationAdd[5]

        for prop in _props:
            if prop['t'] == tag:
                thisProp = prop

                thisProp['as'].append({
                    'an': animName,
                    'p': prefix,
                    'f': fps,
                    'l': loop
                })
        
    for addProp in parentFunc.get('addLuaSprite', []):
        thisProp = None

        tag = addProp[1]
        afterChars = False
        if len(addProp) > 2:
            afterChars = addProp[2]

        for prop in _props:
            if prop['t'] == tag:
                thisProp = prop

        if thisProp:
            if afterChars:
                newZ = int(thisProp['z']) + 300
                thisProp['z'] = newZ

    return _props

def toFNFProps(props):
    _props_converted = []
    for prop in props:
        animated = prop['a']
        name = prop['t']
        assetPath = prop['s']
        posX = prop['x']
        posY = prop['y']
        posZ = prop['z']
        animations = prop['as']

        _prop_template = None
        
        if not animated:
            _prop_template = copy.deepcopy(Constants.STAGE_PROP_IMAGE)
        else:
            _prop_template = copy.deepcopy(Constants.STAGE_PROP_ANIMATED)

        if _prop_template:
            #print(name, assetPath, posX, posY)

            _prop_template['name'] = name
            _prop_template['assetPath'] = assetPath
            _posX = 0
            _posY = 0

            try:
                #Should probably have these as a prompt in the future
                _posX = float(posX) - 1000
                _posY = float(posY) - 720
            except Exception as e:
                logging.error(f'Error converting x and y values: {e}')

            _prop_template['position'][0] = _posX
            _prop_template['position'][1] = _posY
            _prop_template['zIndex'] = posZ

            if animated:
                for animation in animations:
                    _animation_template = copy.deepcopy(Constants.STAGE_PROP_ANIMATION)

                    fps = animation['f']
                    loop = animation['l']
                    name = animation['an']
                    prefix = animation['p']

                    _animation_template['frameRate'] = fps
                    _animation_template['looped'] = loop
                    _animation_template['name'] = name
                    _animation_template['prefix'] = prefix

                    _prop_template['animations'].append(_animation_template)

            _props_converted.append(_prop_template)

    return _props_converted