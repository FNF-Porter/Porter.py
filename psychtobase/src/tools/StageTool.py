import copy
import logging
import src.Constants as Constants
import src.window as window

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
        pos = [0.0, 0.0]
        scale = [1.0, 1.0]
        scroll = [1.0, 1.0]

        try:
            pos = [float(pictureProp[3]), float(pictureProp[4])]
        except:
            logging.error(f'[{luaFilename}] Failed accessing x and y of prop! Did you check if it is defined?')

        for func in parentFunc.get('scaleObject', []):
            if func[1] == tag:
                scale = [float(func[2]), float(func[3])]
                break
        
        for func in parentFunc.get('setScrollFactor', []):
            if func[1] == tag:
                scroll = [float(func[2]), float(func[3])]
                break

        call = pictureProp[0]

        animated = False
        if call == 'makeAnimatedLuaSprite':
            animated = True

        _props.append({
            't': tag, # Tag
            's': sprite, # Sprite
            'x': pos[0], # X
            'y': pos[1], # Y
            'z': 0, # Z index
            'a': animated, # Animated
            'as': [], # Animations
            'scale': scale, # Scale
            'scroll': scroll # Scroll
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
                prop['as'].append({
                    'an': animName,
                    'p': prefix,
                    'f': fps,
                    'l': loop
                })
        
    addSpriteOrder = [addProp[1] for addProp in parentFunc.get('addLuaSprite', [])]

    for i, tag in enumerate(addSpriteOrder):
        for prop in _props:
            if prop['t'] == tag:
                if len(parentFunc.get('addLuaSprite', [])[i]) > 2 and parentFunc.get('addLuaSprite', [])[i][2]:
                    prop['z'] = 300 + i
                else:
                    prop['z'] = i - len(addSpriteOrder)

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
        scale = prop['scale']
        scroll = prop['scroll']

        _prop_template = None
        
        if not animated:
            _prop_template = copy.deepcopy(Constants.STAGE_PROP_IMAGE)
        else:
            _prop_template = copy.deepcopy(Constants.STAGE_PROP_ANIMATED)

        if _prop_template:
            #print(name, assetPath, posX, posY)

            _prop_template['name'] = name
            _prop_template['assetPath'] = assetPath
            _posY = 0

            try:
                #Should probably have this as a prompt in the future
                _posY = float(posY) - 720
            except Exception as e:
                logging.error(f'Error converting y value: {e}')

            _prop_template['position'][0] = posX
            _prop_template['position'][1] = _posY
            _prop_template['zIndex'] = posZ
            _prop_template['scale'] = scale
            _prop_template['scroll'] = scroll

            if animated:
                for animation in animations:
                    _animation_template = copy.deepcopy(Constants.STAGE_PROP_ANIMATION)

                    fps = animation['f']
                    loop = animation['l']
                    name = animation['an']
                    prefix = animation['p']

                    # Best ensure data type is correct or stage fails to load.
                    _animation_template['frameRate'] = int(fps)
                    _animation_template['looped'] = bool(loop)
                    _animation_template['name'] = str(name)
                    _animation_template['prefix'] = str(prefix)

                    _prop_template['animations'].append(_animation_template)

            _props_converted.append(_prop_template)

    return _props_converted