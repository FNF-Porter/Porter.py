local defaultY = 0

function onCreate()
	setPropertyFromClass('GameOverSubstate', 'deathSoundName', 'ourple_death')
end

function onCreatePost()
	defaultY = getProperty('boyfriend.y')
end

function onBeatHit() 
	setProperty('iconP1.flipX', curBeat % 2)
	
	if getProperty('boyfriend.animation.curAnim.name') == 'idle' then
		setProperty('boyfriend.flipX', curBeat % 2);
		setProperty('boyfriend.y', defaultY + 20);
		doTweenY('raise', 'boyfriend', defaultY, 0.15, 'cubeOut');
	end
end

function goodNoteHit(id, direction, noteType, isSustainNote)
	if not getPropertyFromGroup('notes', id, 'gfNote') then
		cancelTween('raise')
		setProperty('boyfriend.y', defaultY)
		setProperty('boyfriend.flipX', true)
	end
end

local angleOfs;
function onUpdate(e)
	angleOfs = math.random(-5, 5);
	setProperty('iconP1.angle', getProperty('healthBar.percent') < 20 and angleOfs or 0); -- Doesn't improve performance just looks cleaner
end