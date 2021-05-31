from enum import Enum

class MoveEnum(Enum):
    NORMAL = 0
    FIRE = 1
    WATER = 2
    GRASS = 3
    PSYCHIC = 4
    DARK = 5
    FIGHTING = 6
    DRAGON = 7
    FAIRY = 8
    STEEL = 9
    FLYING = 10
    GROUND = 11
    ELECTRIC = 12

SUPER_EFFECTIVE = {
    MoveEnum.NORMAL: [],
    MoveEnum.GRASS: [MoveEnum.WATER],
    MoveEnum.FIRE: [MoveEnum.GRASS],
    MoveEnum.WATER: [MoveEnum.FIRE],
    MoveEnum.FIGHTING: [MoveEnum.DARK],
    MoveEnum.PSYCHIC: [MoveEnum.FIGHTING],
    MoveEnum.DARK: [MoveEnum.PSYCHIC],
    MoveEnum.STEEL: [MoveEnum.FAIRY],
    MoveEnum.DRAGON: [MoveEnum.DRAGON, MoveEnum.STEEL],
    MoveEnum.FAIRY: [MoveEnum.DRAGON],
    MoveEnum.GROUND: [MoveEnum.ELECTRIC],
    MoveEnum.ELECTRIC: [MoveEnum.FLYING],
    MoveEnum.FLYING: [MoveEnum.GROUND],
}

NOT_VERY_EFFECTIVE = {
    MoveEnum.NORMAL: [],
    MoveEnum.GRASS: [MoveEnum.GRASS, MoveEnum.FIRE],
    MoveEnum.FIRE: [MoveEnum.FIRE, MoveEnum.WATER],
    MoveEnum.WATER: [MoveEnum.WATER, MoveEnum.GRASS],
    MoveEnum.FIGHTING: [MoveEnum.FIGHTING, MoveEnum.FIGHTING],
    MoveEnum.PSYCHIC: [MoveEnum.PSYCHIC, MoveEnum.PSYCHIC],
    MoveEnum.DARK: [MoveEnum.DARK, MoveEnum.DARK],
    MoveEnum.STEEL: [MoveEnum.DRAGON],
    MoveEnum.DRAGON: [MoveEnum.FAIRY],
    MoveEnum.FAIRY: [MoveEnum.STEEL],
    MoveEnum.GROUND: [MoveEnum.GROUND, MoveEnum.FLYING],
    MoveEnum.ELECTRIC: [MoveEnum.ELECTRIC, MoveEnum.GROUND],
    MoveEnum.FLYING: [MoveEnum.FLYING, MoveEnum.ELECTRIC],
}