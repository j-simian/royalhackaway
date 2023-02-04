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
CHARGETIME = 100
COOLDOWNTIME = 400
PERFECTTHRESHOLD = 0.2
HITTHRESHOLD = 0.4

attacks = {
    "light": {
        "dimensions": (200, 100),
        "offset": (0, -100),
        "damage": 4,
        "knockback": (2, -1),
        "duration": 100,
        "stun": 200
    },
    "heavy": {
        "dimensions": (250, 100),
        "offset": (0, 0),
        "damage": 10,
        "knockback": (5, -1),
        "duration": 500,
        "stun": 400
    }
}
