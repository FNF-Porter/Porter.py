-- Event notes hooks
function onEvent(name, value1, value2)
    if name == "MoveArrowsToMiddle" and (downscroll or upscroll) then
        local var value1 = tonumber(value1)
        local var value2 = tonumber(value2)
        if value1 == 0 then
            -- 1
            noteTweenX("backx5", 4, 740, 0.6, "quartInOut");
            noteTweenAngle("backr5", 4, -360, 0.6, "quartInOut");
            noteTweenAlpha("backo5", 4, 1, 0.6,"quartInOut");
            -- 2
            noteTweenX("backx6", 5, 852, 0.6, "quartInOut");
            noteTweenAngle("backr6", 5, -360, 0.6, "quartInOut");
            noteTweenAlpha("backo6", 5, 1, 0.6, "quartInOut");
            -- 3
            noteTweenX("backx7", 6, 963, 0.6, "quartInOut");
            noteTweenAngle("backr7", 6, -360, 0.6, "quartInOut");
            noteTweenAlpha("backo7", 6, 1, 0.6, "quartInOut");
            -- 4
            noteTweenX("backx8", 7, 1075, 0.6, "quartInOut");
            noteTweenAngle("backr8", 7, -360, 0.6, "quartInOut");
            noteTweenAlpha("backo8", 7, 1, 0.6, "quartInOut");
        end

        if value2 == 1 then
            noteTweenAlpha('outtaHere1Tween', 0, 0, 0.4, 'linear')
            noteTweenAlpha('outtaHere2Tween', 1, 0, 0.4, 'linear')
            noteTweenAlpha('outtaHere3Tween', 2, 0, 0.4, 'linear')
            noteTweenAlpha('outtaHere4Tween', 3, 0, 0.4, 'linear')
        elseif value2 == 0 then
            noteTweenAlpha('noWaitComeBack1Tween', 0, 1, 0.4, 'linear')
            noteTweenAlpha('noWaitComeBack2Tween', 1, 1, 0.4, 'linear')
            noteTweenAlpha('noWaitComeBack3Tween', 2, 1, 0.4, 'linear')
            noteTweenAlpha('noWaitComeBack4Tween', 3, 1, 0.4, 'linear')
        elseif value2 == 2 then
            noteTweenAlpha('outtaMyWay1Tween', 0, 0.4, 0.4, 'linear')
            noteTweenAlpha('outtaMyWay2Tween', 1, 0.4, 0.4, 'linear')
            noteTweenAlpha('outtaMyWay3Tween', 2, 0.4, 0.4, 'linear')
            noteTweenAlpha('outtaMyWay4Tween', 3, 0.4, 0.4, 'linear')
        end
        
        if value1 == 1 then
                -- !your note 1
            noteTweenX("x5", 4, 410, 0.6, "quartInOut");
            noteTweenAngle("r5", 4, 360, 0.6, "quartInOut");
            noteTweenAlpha("o5", 4, 1, 0.6,"quartInOut");
                -- !your note 2
            noteTweenX("x6", 5, 522, 0.6, "quartInOut");
            noteTweenAngle("r6", 5, 360, 0.6, "quartInOut");
            noteTweenAlpha("o6", 5, 1, 0.6, "quartInOut");
                -- !your note 3
            noteTweenX("x7", 6, 633, 0.6, "quartInOut");
            noteTweenAngle("r7", 6, 360, 0.6, "quartInOut");
            noteTweenAlpha("o7", 6, 1, 0.6, "quartInOut");
                -- !your note 4
            noteTweenX("x8", 7, 745, 0.6, "quartInOut");
            noteTweenAngle("r8", 7, 360, 0.6, "quartInOut");
            noteTweenAlpha("o8", 7, 1, 0.6, "quartInOut");
        end

            -- !ups n' downs
        --    noteTweenY("y5",4,bleh,grusd,"quartInOut");
        --    noteTweenY("y6",5,nah,noe,"quartInOut");
        --    noteTweenY("y7",6,but,hey,"quartInOut");
        --    noteTweenY("y8",7,no,need,"quartInOut");
    end
end
-- opp notes (uneeded)
 --if value1 == 0 then
        --    noteTweenX("x1",0,newnotePosX,duration,"quartInOut");
        --    noteTweenY("y1",0,newnotePosY,duration,"quartInOut");
        --    noteTweenAngle("r1",0,rotation,duration, "quartInOut");
        --    noteTweenAlpha("o1",0,opacity,duration,"quartInOut");
        --elseif value1 == 1 then
        --    noteTweenX("x2",1,newnotePosX,duration,"quartInOut");
        --    noteTweenY("y2",1,newnotePosY,duration,"quartInOut");
        --    noteTweenAngle("r2",1,rotation,duration, "quartInOut");
        --    noteTweenAlpha("o2",1,opacity,duration,"quartInOut");
        --elseif value1 == 2 then
        --    noteTweenX("x3",2,newnotePosX,duration,"quartInOut");
        --    noteTweenY("y3",2,newnotePosY,duration,"quartInOut");
        --    noteTweenAngle("r3",2,rotation,duration, "quartInOut");
        --    noteTweenAlpha("o3",2,opacity,duration,"quartInOut");
        --elseif value1 == 3 then
        --    noteTweenX("x4",3,newnotePosX,duration,"quartInOut");
        --    noteTweenY("y4",3,newnotePosY,duration,"quartInOut");
        --    noteTweenAngle("r4",3,rotation,duration, "quartInOut");
        --    noteTweenAlpha("o4",3,opacity,duration,"quartInOut");
        --else