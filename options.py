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
PERFECTTHRESHOLD = 0.2
HITTHRESHOLD = 0.33
HITGLOWDURATION = 150
VIEWHITBOXES = False
STUNSPEED = 0.1
PERFECTMULT = 1
HITMULT = 0.6
MISSMULT = 0.3

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
        "knockback": (-6, -1),
        "duration": 100,
        "stun": 200
    },
    "light3": {
        "dimensions": (100, 100),
        "offset": (0, -100),
        "damage": 4,
        "knockback": (4, -2),
        "duration": 100,
        "stun": 500
    },
    "heavy": {
        "dimensions": (150, 100),
        "offset": (0, 0),
        "damage": 10,
        "knockback": (40, 0),
        "duration": 200,
        "stun": 400
    },
    "stunner": {
        "dimensions": (200, 200),
        "offset": (0, 0),
        "damage": 15,
        "knockback": (40, 0),
        "duration": 200,
        "stun": 2000
    },
    "ministunner": {
        "dimensions": (150, 150),
        "offset": (0, 0),
        "damage": 10,
        "knockback": (40, 0),
        "duration": 150,
        "stun": 1000
    },
    "badhit": {
        "dimensions": (50, 50),
        "offset": (-50, 0),
        "damage": 0,
        "knockback": (6, 0),
        "duration": 50,
        "stun": 0
    }
}
