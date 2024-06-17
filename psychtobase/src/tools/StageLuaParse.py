import logging

from . import StageTool
from luaparser import ast
from luaparser.astnodes import *

def parseStage(lua_script_path):
    lua_script = open(lua_script_path, 'r').read()

    # Parse the Lua script into an AST
    tree = ast.parse(lua_script)

    calls = {}

    allowedMethods = ['makeLuaSprite', 'setScrollFactor', 'scaleObject', 'makeAnimatedLuaSprite', 'addAnimationByPrefix', 'addLuaSprite']
    allowedFuncs = ['onCreate', 'onCreatePost']

    # Note: addLuaSprite only checks for if a character is after the characters!

    for node in ast.walk(tree):
        if isinstance(node, ast.Function):
            curFunc = None

            if isinstance(node.name, ast.Name):
                try:
                    curFunc = node.name.id
                except Exception as e:
                    logging.error(f'Couldn\'t get the current Function name: {e}')
            else:
                curFunc = None

            if not curFunc in calls:
                calls[curFunc] = {}

        if isinstance(node, ast.Call):
            try:
                if isinstance(node.func, ast.Name) and node.func.id in allowedMethods and curFunc in allowedFuncs:
                    arguments = [node.func.id]

                    for arg in node.args:
                        #Me and the boys HATE Lua <3
                        # true.... better keep testing this!!!!! :imp:
                        try:
                            logging.info(f'Starting conversion of lua type: {type(arg)}')
                            match(type(arg)):
                                case ast.String:
                                    arguments.append(arg.s)
                                case ast.Number:
                                    arguments.append(arg.n)
                                case ast.Name:
                                    arguments.append(arg.id)
                                case ast.UMinusOp:
                                    arguments.append('-' + str(arg.operand.n))
                                case ast.FalseExpr:
                                    arguments.append(False)
                                case ast.TrueExpr:
                                    arguments.append(True)
                                case ast.Nil:
                                    arguments.append(None)
                                case ast.Field:
                                    key = arg.key.s if isinstance(arg.key, ast.String) else arg.key.id
                                    value = arg.value.s if isinstance(arg.value, ast.String) else arg.value.id
                                    arguments.append({key: value})
                                case ast.Table:
                                    fields = {}
                                    for field in arg.fields:
                                        key = field.key.s if isinstance(field.key, ast.String) else field.key.id
                                        value = field.value.s if isinstance(field.value, ast.String) else field.value.id
                                        fields[key] = value
                                    arguments.append(fields)
                                case ast.Concat:
                                    left = arg.left.s if isinstance(arg.left, ast.String) else arg.left.id
                                    right = arg.right.s if isinstance(arg.right, ast.String) else arg.right.id
                                    arguments.append(f'{left}..{right}')
                                case ast.Index:
                                    index = arg.idx.s if isinstance(arg.idx, ast.String) else arg.idx.id
                                    value = arg.value.s if isinstance(arg.value, ast.String) else arg.value.id
                                    arguments.append({index: value})
                                case ast.AddOp:
                                    left = arg.left.n if isinstance(arg.left, ast.Number) else (arg.left.id if isinstance(arg.left, ast.Name) else None)
                                    right = arg.right.n if isinstance(arg.right, ast.Number) else (arg.right.id if isinstance(arg.right, ast.Name) else None)
                                    arguments.append(f'{left} + {right}')
                                case ast.SubOp:
                                    left = arg.left.n if isinstance(arg.left, ast.Number) else (arg.left.id if isinstance(arg.left, ast.Name) else None)
                                    right = arg.right.n if isinstance(arg.right, ast.Number) else (arg.right.id if isinstance(arg.right, ast.Name) else None)
                                    arguments.append(f'{left} - {right}')
                                case _:
                                    logging.warn(f'Unsupported type of lua node: {type(arg)}')

                        except Exception as e:
                            logging.error(f'Could not append arguments of this call: {e}')

                    if not node.func.id in calls[curFunc]:
                        calls[curFunc][node.func.id] = []

                    calls[curFunc][node.func.id].append(arguments)

            except Exception as e:
                logging.error(f'Failed to assign arguments of this call: {e}')

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
