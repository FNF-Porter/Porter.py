function onEvent(name:String, val1:String)
{
    if (name != "center cam") return;

    var midX:Float = (game.dad.getGraphicMidpoint().x + game.boyfriend.getGraphicMidpoint().x) / 2;
    if (val1 != "")
    {
        if (val1 == "boyfriend")
            midX += game.boyfriend.width / 8;
        else
            midX -= game.dad.width / 8;
    }

    game.triggerEvent("Camera Follow Pos", midX, game.camFollow.y);
}