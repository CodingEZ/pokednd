import math
import random
from enum import Enum

from action_enum import ActionEnum, ACTIONS
from attack_enum import AttackEnum
from move_enum import MoveEnum, SUPER_EFFECTIVE, NOT_VERY_EFFECTIVE
from status_enum import StatusEnum
from stat_enum import StatEnum
from data import POKEDATA
from character import Character


def roll_dice(num, sides):
    return [math.floor(random.random() * sides) + 1 for i in range(num)]

def roll_power():
    results = roll_dice(5, 25)
    print(results)
    res = (sum(results) - min(results)) / 100
    print(f"Move power: {res}")
    return res

def turn_simulate(c1, c2):
    while True:
        attack_type = input("""Attack type:
1: physical
2: special
3: self_modification
4: target_modification
5: self_hp
6: self_status
7: target_hp
8: target_status
Choose an attack type: """)
        if attack_type == "1":
            attack_type = AttackEnum.PHYSICAL
            break
        elif attack_type == "2":
            attack_type = AttackEnum.SPECIAL
            break
        elif attack_type == "3":
            attack_type = AttackEnum.SELF_MODIFICATION
            break
        elif attack_type == "4":
            attack_type = AttackEnum.TARGET_MODIFICATION
            break
        elif attack_type == "5":
            attack_type = AttackEnum.SELF_HP
            break
        elif attack_type == "6":
            attack_type = AttackEnum.SELF_STATUS
            break
        elif attack_type == "7":
            attack_type = AttackEnum.TARGET_HP
            break
        elif attack_type == "8":
            attack_type = AttackEnum.TARGET_STATUS
            break

    print()

    while True:
        move_type = input("Move Type (fire/grass/water/etc): ")
        if move_type == "normal":
            move_type = MoveEnum.NORMAL
            break
        elif move_type == "fighting":
            move_type = MoveEnum.FIGHTING
            break
        elif move_type == "flying":
            move_type = MoveEnum.FLYING
            break
        elif move_type == "ground":
            move_type = MoveEnum.GROUND
            break
        elif move_type == "rock":
            move_type = MoveEnum.ROCK
            break
        elif move_type == "bug":
            move_type = MoveEnum.BUG
            break
        elif move_type == "ghost":
            move_type = MoveEnum.GHOST
            break
        elif move_type == "steel":
            move_type = MoveEnum.STEEL
            break
        elif move_type == "fire":
            move_type = MoveEnum.FIRE
            break
        elif move_type == "water":
            move_type = MoveEnum.WATER
            break
        elif move_type == "grass":
            move_type = MoveEnum.GRASS
            break
        elif move_type == "electric":
            move_type = MoveEnum.ELECTRIC
            break
        elif move_type == "psychic":
            move_type = MoveEnum.PSYCHIC
            break
        elif move_type == "ice":
            move_type = MoveEnum.ICE
            break
        elif move_type == "dragon":
            move_type = MoveEnum.DRAGON
            break
        elif move_type == "dark":
            move_type = MoveEnum.DARK
            break
        elif move_type == "fairy":
            move_type = MoveEnum.FAIRY
            break

    print("Rolling for power")
    roll_fraction = roll_power()
    print()

    while True:
        status_type = input("""Status type:
1: sleep
2: paralyze
3: burn
4: confusion
5: flinch
6: none
Choose an status type: """)
        if status_type == "1":
            status_type = StatusEnum.SLEEP
            break
        elif status_type == "2":
            status_type = StatusEnum.PARALYZE
            break
        elif status_type == "3":
            status_type = StatusEnum.BURN
            break
        elif status_type == "4":
            status_type = StatusEnum.CONFUSION
            break
        elif status_type == "5":
            status_type = StatusEnum.FLINCH
            break
        elif status_type == "6":
            status_type = StatusEnum.NONE
            break

    c1.attack(c2, attack_type, move_type, .5, status_type)

c1 = Character(
    "Techno", 10, [MoveEnum.FIRE], 
    2, 1, 3, 1, 3, # concrete
    1, 1, 2, 1, 2, # mental
    -2, 0, 0, 0, 0, # modifiers
    StatusEnum.NONE, 0) # status
c2 = Character(
    "Squirrel", 8, [MoveEnum.NORMAL], 
    2, 2, 2, 4, 2, # concrete
    1, 1, 1, 1, 1, # mental
    2, 0, 0, 2, 1, # modifiers
    StatusEnum.NONE, 0) # status
c3 = Character(
    "Octopus", 8, [MoveEnum.WATER], 
    0, 0, 17, 0, 0, # concrete
    0, 0, 0, 0, 0, # mental
    0, 0, 0, 0, 0, # modifiers
    StatusEnum.NONE, 0) # status
c4 = Character(
    "Raccoon", 25, [MoveEnum.GRASS], 
    0, 0, 0, 0, 0, # concrete
    0, 0, 0, 0, 0, # mental
    0, 0, 0, 0, 0, # modifiers
    StatusEnum.NONE, 0) # status

# c5 = Character.create(POKEDATA["Charmander"], 1, 10)
# print(c5)
# print(Character.create(POKEDATA["Charizard"], 3, 70))

# c1.attack(c2, AttackEnum.SPECIAL, MoveEnum.FIRE, .5, StatusEnum.BURN)
# c2.attack(c1, AttackEnum.PHYSICAL, MoveEnum.NORMAL, .5, StatusEnum.NONE)

# c1.attack(c2, AttackEnum.SPECIAL, MoveEnum.FIGHTING, 0, StatusEnum.NONE);
# c3.attack(c1, AttackEnum.SPECIAL, MoveEnum.WATER, .80, StatusEnum.NONE);

# turn_simulate(c1, c2)
