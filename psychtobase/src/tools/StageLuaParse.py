import json
from luaparser import ast
from luaparser.astnodes import Function, Call, String, Number, Name, UMinusOp
import logging
import psychtobase.src.tools.StageTool as StageTool

def parseStage(lua_script_path):
    lua_script = open(lua_script_path, 'r').read()

    # Parse the Lua script into an AST
    tree = ast.parse(lua_script)

    calls = {}

    allowedMethods = ['makeLuaSprite', 'makeAnimatedLuaSprite', 'addAnimationByPrefix', 'addLuaSprite']
    allowedFuncs = ['onCreate', 'onCreatePost']

    # Note: addLuaSprite only checks for if a character is after the characters!

    for node in ast.walk(tree):
        if isinstance(node, Function):
            curFunc = None

            if isinstance(node.name, Name):
                try:
                    curFunc = node.name.id
                except:
                    logging.error('Fail setting curFunc!')
            else:
                curFunc = None
            if calls.get(curFunc, None) == None:
                calls[curFunc] = {}

        if isinstance(node, Call):
            try:
                if node.func.id in allowedMethods and curFunc in allowedFuncs:
                    arguments = [node.func.id]
                for arg in node.args:
                    #idk what this used to do but i know how to make switch cases so
                    #hopefully it does the same thing
                    match isinstance:
                        case (arg, String):
                            arguments.append(arg.s)
                        case (arg, Number):
                            arguments.append(arg.n)
                        case (arg, Name):
                            arguments.append(arg.id)
                        case (arg, UMinusOp):
                            arguments.append('-' + str(arg.operand.n))
                if calls[curFunc].get(node.func.id, None) == None:
                    calls[curFunc][node.func.id] = []
                
                calls[curFunc][node.func.id].append(arguments)
            except:
                logging.error('Fail in isintance(node, Call)!')

    #print(f'{calls}')

    _props = []

    for key in calls.keys():
        logging.info(f'Getting props of {key}')
        _props.extend(StageTool.getProps(calls[key], key))

    return StageTool.toFNFProps(_props)