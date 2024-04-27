from src.XMLTools import WeekXML
from src.Paths import Paths

Paths.assetsDir = "./mods/btoad-fnf"

# print(Paths.parseJson("weeks\story1Btoad"))
test = WeekXML().setup("weeks\story1Btoad")