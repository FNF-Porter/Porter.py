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

    for node in ast.walk(tree):
        if isinstance(node, Function):
            curFunc = node.name.id if isinstance(node.name, Name) else None
            if calls.get(curFunc, None) == None:
                calls[curFunc] = {}

        if isinstance(node, Call):
            if node.func.id in allowedMethods and curFunc in allowedFuncs:
                arguments = [node.func.id]
                for arg in node.args:
                    if isinstance(arg, String):
                        arguments.append(arg.s)
                    elif isinstance(arg, Number):
                        arguments.append(arg.n)
                    elif isinstance(arg, Name):
                        arguments.append(arg.id)
                    elif isinstance(arg, UMinusOp):
                        arguments.append('-' + str(arg.operand.n))

                if calls[curFunc].get(node.func.id, None) == None:
                    calls[curFunc][node.func.id] = []
                
                calls[curFunc][node.func.id].append(arguments)

    #print(f'{calls}')

    _props = []

    for key in calls.keys():
        logging.info(f'Getting props of {key}')
        _props.extend(StageTool.getProps(calls[key], key))

    return StageTool.toFNFProps(_props)