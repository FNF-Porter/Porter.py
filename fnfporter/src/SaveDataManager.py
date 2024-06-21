import json

defaultSaveData = {
    'paths': {
        'psychToBase': {
            'psychMod': '',
            'baseGame': ''
        },
        'baseToPsych': {
            'baseMod': '',
            'psych': ''
        }
    },
    "lastLogFile": "",
    "conversionOptions": {
        "psychToBase": None,
        "baseToPsych": None
    }
}

class SaveData():
    def __init__(self, path:str = '.SAVE_DATA'):
        self.saveData = None
        self.savePath = path
    
    def initSave(self):
        try:
            self.saveData = json.load(open(self.savePath, 'r'))
        except FileNotFoundError as e:
            print(f'Save Data does not exist! {e}\n Creating one...')
            open(self.savePath, 'w').write(json.dumps(defaultSaveData, indent=4))
            self.saveData = json.load(open(self.savePath, 'r'))
        except Exception:
            print('Could not load save file: ', exc_info=Exception)

    def save(self, path:str = '.SAVE_DATA'):
        open(path, 'w').write(json.dumps(self.saveData, indent=4))

save = SaveData()

def initSaveData():
    save.initSave()
    print('Initiated save data!')

def getField(field:str):
    if field != None:
        return save.saveData.get(field, None)
    
def setField(field:str, value):
    if field != None:
        save.saveData[field] = value
    
def writeSave():
    save.save()