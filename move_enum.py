from enum import Enum


class MoveEnum(Enum):
    NORMAL = 0
    FIGHTING = 1
    FLYING = 2
    POISON = 3
    GROUND = 4
    ROCK = 5
    BUG = 6
    GHOST = 7
    STEEL = 8
    FIRE = 9
    WATER = 10
    GRASS = 11
    ELECTRIC = 12
    PSYCHIC = 13
    ICE = 14
    DRAGON = 15
    DARK = 16
    FAIRY = 17


SUPER_EFFECTIVE = {
    MoveEnum.NORMAL: [],
    MoveEnum.FIGHTING: [MoveEnum.NORMAL, MoveEnum.ROCK, MoveEnum.STEEL, MoveEnum.ICE, MoveEnum.DARK],
    MoveEnum.FLYING: [MoveEnum.FIGHTING, MoveEnum.BUG, MoveEnum.GRASS],
    MoveEnum.POISON: [MoveEnum.GRASS, MoveEnum.FAIRY],
    MoveEnum.GROUND: [MoveEnum.POISON, MoveEnum.ROCK, MoveEnum.STEEL, MoveEnum.FIRE, MoveEnum.ELECTRIC],
    MoveEnum.ROCK: [MoveEnum.FLYING, MoveEnum.BUG, MoveEnum.FIRE, MoveEnum.ICE],
    MoveEnum.BUG: [MoveEnum.GRASS, MoveEnum.PSYCHIC, MoveEnum.DARK],
    MoveEnum.GHOST: [MoveEnum.GHOST, MoveEnum.PSYCHIC],
    MoveEnum.STEEL: [MoveEnum.ROCK, MoveEnum.ICE, MoveEnum.FAIRY],
    MoveEnum.FIRE: [MoveEnum.BUG, MoveEnum.STEEL, MoveEnum.GRASS, MoveEnum.ICE],
    MoveEnum.WATER: [MoveEnum.GROUND, MoveEnum.ROCK, MoveEnum.FIRE],
    MoveEnum.GRASS: [MoveEnum.GROUND, MoveEnum.ROCK, MoveEnum.WATER],
    MoveEnum.ELECTRIC: [MoveEnum.FLYING, MoveEnum.WATER],
    MoveEnum.PSYCHIC: [MoveEnum.FIGHTING, MoveEnum.POISON],
    MoveEnum.ICE: [MoveEnum.FLYING, MoveEnum.GROUND, MoveEnum.GRASS, MoveEnum.DRAGON],
    MoveEnum.DRAGON: [MoveEnum.DRAGON],
    MoveEnum.DARK: [MoveEnum.GHOST, MoveEnum.PSYCHIC],
    MoveEnum.FAIRY: [MoveEnum.FIGHTING, MoveEnum.DRAGON, MoveEnum.DARK],
}

NOT_VERY_EFFECTIVE = {
    MoveEnum.NORMAL: [MoveEnum.ROCK, MoveEnum.STEEL],
    MoveEnum.FIGHTING: [MoveEnum.FLYING, MoveEnum.POISON, MoveEnum.BUG, MoveEnum.PSYCHIC, MoveEnum.FAIRY],
    MoveEnum.FLYING: [MoveEnum.ROCK, MoveEnum.STEEL, MoveEnum.ELECTRIC],
    MoveEnum.POISON: [MoveEnum.POISON, MoveEnum.GROUND, MoveEnum.ROCK],
    MoveEnum.GROUND: [MoveEnum.BUG, MoveEnum.GRASS],
    MoveEnum.ROCK: [MoveEnum.FIGHTING, MoveEnum.STEEL],
    MoveEnum.BUG: [MoveEnum.FIGHTING, MoveEnum.FLYING, MoveEnum.POISON, MoveEnum.GHOST, MoveEnum.STEEL, MoveEnum.FIRE, MoveEnum.FAIRY],
    MoveEnum.GHOST: [MoveEnum.DARK],
    MoveEnum.STEEL: [MoveEnum.STEEL, MoveEnum.FIRE, MoveEnum.WATER, MoveEnum.ELECTRIC],
    MoveEnum.FIRE: [MoveEnum.ROCK, MoveEnum.FIRE, MoveEnum.WATER, MoveEnum.DRAGON],
    MoveEnum.WATER: [MoveEnum.WATER, MoveEnum.GRASS, MoveEnum.DRAGON],
    MoveEnum.GRASS: [MoveEnum.FLYING, MoveEnum.POISON, MoveEnum.BUG, MoveEnum.STEEL, MoveEnum.FIRE, MoveEnum.GRASS, MoveEnum.DRAGON],
    MoveEnum.ELECTRIC: [MoveEnum.GRASS, MoveEnum.ELECTRIC, MoveEnum.DRAGON],
    MoveEnum.PSYCHIC: [MoveEnum.STEEL, MoveEnum.PSYCHIC],
    MoveEnum.DRAGON: [MoveEnum.STEEL],
    MoveEnum.DARK: [MoveEnum.DARK, MoveEnum.FAIRY],
    MoveEnum.FAIRY: [MoveEnum.POISON, MoveEnum.STEEL, MoveEnum.FIRE],
}

IMMUNITY = {
    MoveEnum.NORMAL: [MoveEnum.GHOST],
    MoveEnum.FIGHTING: [MoveEnum.GHOST],
    MoveEnum.FLYING: [],
    MoveEnum.POISON: [MoveEnum.STEEL],
    MoveEnum.GROUND: [MoveEnum.FLYING],
    MoveEnum.ROCK: [],
    MoveEnum.BUG: [],
    MoveEnum.GHOST: [MoveEnum.NORMAL],
    MoveEnum.STEEL: [],
    MoveEnum.FIRE: [],
    MoveEnum.WATER: [],
    MoveEnum.GRASS: [],
    MoveEnum.ELECTRIC: [MoveEnum.GROUND],
    MoveEnum.PSYCHIC: [MoveEnum.DARK],
    MoveEnum.DRAGON: [MoveEnum.FAIRY],
    MoveEnum.DARK: [],
    MoveEnum.FAIRY: [],
}


def match_move_type(move_type):
    if move_type == "normal":
        return MoveEnum.NORMAL
    elif move_type == "fighting":
        return MoveEnum.FIGHTING
    elif move_type == "flying":
        return MoveEnum.FLYING
    elif move_type == "poison":
        return MoveEnum.POISON
    elif move_type == "ground":
        return MoveEnum.GROUND
    elif move_type == "rock":
        return MoveEnum.ROCK
    elif move_type == "bug":
        return MoveEnum.BUG
    elif move_type == "ghost":
        return MoveEnum.GHOST
    elif move_type == "steel":
        return MoveEnum.STEEL
    elif move_type == "fire":
        return MoveEnum.FIRE
    elif move_type == "water":
        return MoveEnum.WATER
    elif move_type == "grass":
        return MoveEnum.GRASS
    elif move_type == "electric":
        return MoveEnum.ELECTRIC
    elif move_type == "psychic":
        return MoveEnum.PSYCHIC
    elif move_type == "ice":
        return MoveEnum.ICE
    elif move_type == "dragon":
        return MoveEnum.DRAGON
    elif move_type == "dark":
        return MoveEnum.DARK
    elif move_type == "fairy":
        return MoveEnum.FAIRY
    return None
