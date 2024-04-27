function onCreatePost()
    if not getPropertyFromClass("backend.ClientPrefs", "data.shaders") then
      return close();
    end

    makeLuaSprite("die2");
    makeGraphic("die2", screenWidth, screenHeight, "000000");

    initLuaShader("HeatwaveShader", 140);
    setSpriteShader("die2", "HeatwaveShader");

    addHaxeLibrary("ShaderFilter", "openfl.filters");
    runHaxeCode([[
      game.camHUD.setFilters([new ShaderFilter(game.getLuaObject("die2").shader)]);
      game.camGame.setFilters([new ShaderFilter(game.getLuaObject("die2").shader)]);
    ]]);
end

function onUpdatePost()
  setShaderFloat("die2", "iTime", os.clock());
end