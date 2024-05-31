CHANGE_CHARACTER_EVENT_HXC_NAME = 'ChangeCharacterEvent.hxc'
CHANGE_CHARACTER_EVENT_HXC_CONTENTS = """import funkin.play.character.CharacterType;
import funkin.modding.module.ModuleHandler;
import funkin.modding.module.Module;
import funkin.play.character.BaseCharacter;
import funkin.play.character.CharacterDataParser;
import funkin.play.event.ScriptedSongEvent;
import funkin.play.PlayState;
//import Reflect;

/**
 * @author MayoOddToSee
 */
class ChangeCharacterEvent extends ScriptedSongEvent {
	static var BF = 'bf'; //does static even do or mean anything lol
	static var DAD = 'dad';
	static var GF = 'gf';
	
	var dataValue:Dynamic;

	public function new() {
		super('Change Character');
	}

	override function getEventSchema() {
		var map = ["Boyfriend" => BF, "Dad" => DAD, "Girlfriend" => GF,];

		var charMap = ["Boyfriend" => "bf"];
		for (char in CharacterDataParser.listCharacterIds()) {
			charMap.set(CharacterDataParser.fetchCharacterData(char).name, char);
		}

		return [
			{
				name: "target",
				title: "Target",
				type: "enum",
				defaultValue: BF,
				keys: map,
			},
			{
				name: "char",
				title: "Character",
				type: "enum",
				defaultValue: "bf",
				keys: charMap,
			}
		];
	}

	override function handleEvent(data) {
		if (data.value != null) {
			dataValue = data.value;
			var target = getValue('target', BF);
			ModuleHandler.getModule('change-character-handler').scriptCall('changeCharacter', [
				getValue('char', 'bf'),
				switch target {
					case BF:
						CharacterType.BF;
					case DAD:
						CharacterType.DAD;
					case GF:
						CharacterType.GF;
				},
				target
			]);
		}
	}

	//helper function
	function getValue(field:String, def:Dynamic) {
		var value = Type.resolveClass("Reflect").field(dataValue, field);
		if (value == null)
			return def;
		else
			return value;
	}
}

//this class actually changes the characters and stuff
class ChangeCharacterHandler extends Module {
	var debug = false;
	var switchedChars = false;
	var chars:Array<Map<String, BaseCharacter>> = [
		["" => null],
		["" => null],
		["" => null],
	];
	var latest:Array<BaseCharacter> = [];
	var charsFetched:Array<String> = [];
	var strid:Array<String> = ['bf', 'dad', 'gf'];
	var tid:Array<CharacterType> = [CharacterType.BF, CharacterType.DAD, CharacterType.GF];

	public function new() {
		super('change-character-handler');
	}

	override function onCreate(e) {
		trace('whaaat are you working now bitch');
	}

	override function onSongRetry() {
		super.onSongRetry();

		if(!PlayState.instance.isMinimalMode) {
			for(i in 0...3) {
				replaceChar(tid[i], strid[i], defaults[i]);
			}
		}
	}

	override function onStateChangeEnd(event){
        super.onStateChangeEnd(event);
        ok = false;
		for(map in chars) {
			for(char in map) {
				if(char != null) {
					if(debug) trace('IM KILLING YOU', char.characterName);
					char.destroy();
				}
			}
			map.clear();
		}
    }

	function changeCharacter(character:String, characterType:CharacterType, characterTypeString:String) {
		var id = tid.indexOf(characterType);
		var char = chars[id].get(character);
		if(char == null) {
			trace('couldnt find the preloaded :(', character, characterTypeString);
			char = CharacterDataParser.fetchCharacter(char);
			chars[id].set(character, char);
			if(char == null) {
				if(debug) trace('it was STILL null', character, characterTypeString);
				return;
			}
		}else{
			if(debug) trace('found preloaded char', character, characterTypeString);
		}
		replaceChar(characterType, characterTypeString, char);
	}

	function replaceChar(characterType:CharacterType, characterTypeString:String, char:BaseCharacter) {
		var old = PlayState.instance.currentStage.getCharacter(characterTypeString);
		if(old == char) return;
		var index = PlayState.instance.currentStage.members.indexOf(old);
		PlayState.instance.remove(char);
		PlayState.instance.currentStage.remove(old);
		hideChar(old);
		char.scrollFactor.set(1, 1);
		char.alpha = 1;
		PlayState.instance.currentStage.addCharacter(char, characterType);
		PlayState.instance.currentStage.remove(char);
		PlayState.instance.currentStage.insert(index, char);
	}

	function hideChar(char:BaseCharacter) {
		char.alpha = .00001;
		char.scrollFactor.set();
		char.screenCenter();
		PlayState.instance.add(char);
	}

	var ok = false;
	var defaults:Array<BaseCharacter> = [];
	override function onUpdate(e) {
		super.onUpdate(e);
		if(PlayState.instance != null && !PlayState.instance.isMinimalMode && PlayState.instance.currentStage != null && !ok) {
			ok = true;
			var i = 0;
			for(char in [PlayState.instance.currentStage.getBoyfriend(), PlayState.instance.currentStage.getDad(), PlayState.instance.currentStage.getGirlfriend()]) {
				chars[i].set(char.characterId, char);
				defaults[i] = char;
				i++;
			}
			for(event in PlayState.instance.songEvents) {
				if(event.value != null) {
					//??????????????????
					var char = Type.resolveClass("Reflect").field(event.value, 'char');
					var target = Type.resolveClass("Reflect").field(event.value, 'target');
					if(char != null && target != null && !chars[target].exists(char)) {
						var hi = CharacterDataParser.fetchCharacter(char);
						chars[strid.indexOf(target)].set(char, hi);
						hi.characterType = tid[strid.indexOf(target)];
						hideChar(hi);
					}
				}
			}
		}
	}
}"""
# https://youtu.be/eB6txyhHFG4