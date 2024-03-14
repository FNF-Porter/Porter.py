# Test shenanigans for objects.py
from objects import CharacterXML

xml = CharacterXML().setup("mods/btoad-fnf/characters/btoad")
xml.save("output")