import flixel.tweens.FlxTweenManager;

var whiteBg:FlxSprite = new FlxSprite(-200, -100).makeGraphic(1920, 1080, FlxColor.WHITE); // PRECACHING;
whiteBg.scrollFactor.set(0, 0);

var colorTweenManager:FlxTweenManager = new FlxTweenManager();

var alphaTweenManager:FlxTweenManager = new FlxTweenManager();
var healthBarObjs:Array<FlxBasic> = [game.healthBar, game.iconP1, game.iconP2, game.scoreTxt];
var characters:Array<FlxBasic> = [game.boyfriendGroup, game.dadGroup, game.gfGroup];

function killBG(twn:FlxTween)
{
    remove(whiteBg);
}

function coolBgTween(alpha:Float)
{
    alphaTweenManager.clear();

    whiteBg.alpha = 1 - alpha;

    var tempTween:FlxTween = alphaTweenManager.tween(whiteBg, {alpha: alpha}, 0.37, {ease: FlxEase.circInOut});
    if (alpha == 0)
    {
        tempTween.onComplete = killBG;
    }

    for (obj in healthBarObjs)
        alphaTweenManager.tween(obj, {alpha: 1 - alpha}, 0.37, {ease: FlxEase.circInOut});
}

function colorTween(color:FlxColor)
{
    colorTweenManager.clear();
    for (char in characters)
    {
        colorTweenManager.color(char, 0.37, (color == FlxColor.BLACK) ? FlxColor.WHITE : FlxColor.BLACK, color, {ease: FlxEase.circInOut});
    }
}

function onEvent(name:String, value1:String)
{
    if (name == 'badapplelol')
    {
        if (value1 == "a")
        {
            addBehindGF(whiteBg);
            coolBgTween(1);
            colorTween(FlxColor.BLACK);
        }
        else
        {
            coolBgTween(0);
            colorTween(FlxColor.WHITE);
        }
    }
}

function onUpdate(elapsed:Float)
{
    colorTweenManager.update(elapsed);
    alphaTweenManager.update(elapsed);
}