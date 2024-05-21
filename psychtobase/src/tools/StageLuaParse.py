import json
from luaparser import ast
from luaparser.astnodes import Function, Call, String, Number, Name, UMinusOp, FalseExpr, TrueExpr
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
                except Exception as e:
                    logging.error(f'Couldn\'t get the current Function name: {e}')
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
                    try:
                        if isinstance(arg, String):
                            arguments.append(arg.s)
                        elif isinstance(arg, Number):
                            arguments.append(arg.n)
                        elif isinstance(arg, Name):
                            arguments.append(arg.id)
                        elif isinstance(arg, UMinusOp):
                            arguments.append('-' + str(arg.operand.n))
                        elif isinstance(arg, FalseExpr):
                            arguments.append(False)
                        elif isinstance(arg, TrueExpr):
                            arguments.append(True)
                        else:
                            logging.warn(f'Unsupported type of lua node: {type(arg)}')
                    except Exception as e:
                        logging.error(f'Could not append arguments of this call: {e}')
                if calls[curFunc].get(node.func.id, None) == None:
                    calls[curFunc][node.func.id] = []
                
                calls[curFunc][node.func.id].append(arguments)
            except Exception as e:
                logging.error(f'Failed to asign arguments of this call: {e}')

    #print(f'{calls}')

    _props = []
    _newProps = []

    for key in calls.keys():
        logging.info(f'Getting props of {key}')
        _props.extend(StageTool.getProps(calls[key], key, lua_script_path))

    try:
        _newProps = StageTool.toFNFProps(_props)
    except Exception as e:
        logging.error(f'Could not convert objects to FNF props: {e}')

    return _newProps