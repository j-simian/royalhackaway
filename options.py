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
CATHEIGHT = 385*CATSCALE
CATWIDTH = 248*CATSCALE
CHARGETIME = 100
COOLDOWNTIME = 400

attacks = {
    "light": {
        "dimensions": (200, 50),
        "offset": (-100, -150),
        "damage": 10,
        "knockback": (2, 2),
        "duration": 100
    },
    "heavy": {
        "dimensions": (250, 100),
        "offset": (-100, -150),
        "damage": 20,
        "knockback": (5, 5),
        "duration": 500
    }
}
