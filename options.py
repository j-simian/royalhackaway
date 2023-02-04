GRAVITY = 0.005
MAXVELY = 20
MAXVELX = 0.7
DASHRATIO = 2
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

attacks = {
    "light": {
        "dimensions": (200, 50),
        "offset": (0, 0),
        "damage": 10,
        "knockback": (2, 2),
        "duration": 100,
        "stun": 200
    },
    "heavy": {
        "dimensions": (250, 100),
        "offset": (0, 0),
        "damage": 20,
        "knockback": (5, 5),
        "duration": 500,
        "stun": 400
    }
}
