GRAVITY = 0.005
MAXVELY = 20
MAXVELX = 0.7
DASHRATIO = 2
DASHDECREASE = 0.01
FRICTION = 1.05
AIRFRICTION = 1.01
PLAYERACCEL = 2
AIRACCEL = 0.05
JUMPVEL = -3
GROUNDHEIGHT = 550
CATSCALE = 0.66
CATHEIGHT = 500*CATSCALE
CATWIDTH = 500*CATSCALE
HURTWIDTH = 320*CATSCALE #cat hurtbox width
CHARGETIME = 100
HITCOOLDOWN = 100
COOLDOWNTIME = 500
PERFECTTHRESHOLD = 0.1
HITTHRESHOLD = 0.25
HITGLOWDURATION = 150
VIEWHITBOXES = True

attacks = {
    "light1": {
        "dimensions": (100, 200),
        "offset": (0, -200),
        "damage": 4,
        "knockback": (0, -1),
        "duration": 100,
        "stun": 200
    },
    "light2": {
        "dimensions": (100, 100),
        "offset": (0, -100),
        "damage": 4,
        "knockback": (-3, -1),
        "duration": 100,
        "stun": 200
    },
    "light3": {
        "dimensions": (100, 100),
        "offset": (0, -100),
        "damage": 4,
        "knockback": (2, -2),
        "duration": 100,
        "stun": 500
    },
    "heavy": {
        "dimensions": (150, 150),
        "offset": (50, 0),
        "damage": 10,
        "knockback": (20, 0),
        "duration": 200,
        "stun": 400
    }
}
