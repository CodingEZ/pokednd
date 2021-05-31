import math
import random
from enum import Enum

from action_enum import ActionEnum, ACTIONS
from attack_enum import AttackEnum
from move_enum import MoveEnum, match_move_type
from status_enum import StatusEnum
from stat_enum import StatEnum
from data import POKEDATA
from character import Character


def roll_dice(num, sides):
    return [math.floor(random.random() * sides) + 1 for i in range(num)]


def roll_power():
    print("Rolling for power")
    results = roll_dice(5, 25)
    print(results)
    res = (sum(results) - min(results)) / 100
    print(f"Move power: {res}")
    print()
    return res


def turn_simulate(c1, c2):
    while True:
        decision = input("""Decision:
1: scout
2: heal hp
3: heal modifier
4: heal status
5: attack
What is your decision?: """)
        if decision == "1":
            c1.scout(c2)
            return
        elif decision == "2":
            roll_fraction = roll_power()
            c1.heal_hp(c2, roll_fraction)
            return
        elif decision == "3":
            c1.heal_modifier(c2)
            return
        elif decision == "4":
            c1.heal_status(c2)
            return
        elif decision == "5":
            print()
            break

    while True:
        attack_type = input("""Attack type:
1: physical
2: special
3: target_modification
4: target_hp
5: target_status
Choose an attack type: """)
        if attack_type == "1":
            attack_type = AttackEnum.PHYSICAL
            break
        elif attack_type == "2":
            attack_type = AttackEnum.SPECIAL
            break
        elif attack_type == "3":
            attack_type = AttackEnum.TARGET_MODIFICATION
            break
        elif attack_type == "4":
            attack_type = AttackEnum.TARGET_HP
            break
        elif attack_type == "5":
            attack_type = AttackEnum.TARGET_STATUS
            break
    print()

    if attack_type == AttackEnum.PHYSICAL or attack_type == AttackEnum.SPECIAL:
        while True:
            move_type = input("Move Type (fire/grass/water/etc): ")
            move_type = match_move_type(move_type)
            if move_type is not None:
                break
        print()
    else:
        move_type = MoveEnum.NORMAL

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
    print()

    if attack_type == AttackEnum.PHYSICAL or attack_type == AttackEnum.SPECIAL:
        roll_fraction = roll_power()
    else:
        roll_fraction = 0

    c1.attack(c2, attack_type, move_type, roll_fraction, status_type)


c1 = Character(
    "Techno", 10, [MoveEnum.FIRE],
    2, 1, 3, 1, 3,  # concrete
    1, 1, 2, 1, 2,  # mental
    -2, 0, 0, 0, 0,  # modifiers
    StatusEnum.NONE, 0)  # status
c2 = Character(
    "Squirrel", 8, [MoveEnum.NORMAL],
    2, 2, 2, 4, 2,  # concrete
    1, 1, 1, 1, 1,  # mental
    2, 0, 0, 2, 1,  # modifiers
    StatusEnum.NONE, 0)  # status
c3 = Character(
    "Octopus", 8, [MoveEnum.WATER],
    0, 0, 17, 0, 0,  # concrete
    0, 0, 0, 0, 0,  # mental
    0, 0, 0, 0, 0,  # modifiers
    StatusEnum.NONE, 0)  # status
c4 = Character(
    "Raccoon", 25, [MoveEnum.GRASS],
    0, 0, 0, 0, 0,  # concrete
    0, 0, 0, 0, 0,  # mental
    0, 0, 0, 0, 0,  # modifiers
    StatusEnum.NONE, 0)  # status

c5 = Character.create(POKEDATA["Charmander"], 1, 10)
# print(c5)
# print(Character.create(POKEDATA["Charizard"], 3, 70))

# c1.attack(c2, AttackEnum.SPECIAL, MoveEnum.FIRE, .5, StatusEnum.BURN)
# c2.attack(c1, AttackEnum.PHYSICAL, MoveEnum.NORMAL, .5, StatusEnum.NONE)

# c1.attack(c2, AttackEnum.SPECIAL, MoveEnum.FIGHTING, 0, StatusEnum.NONE);
# c3.attack(c1, AttackEnum.SPECIAL, MoveEnum.WATER, .80, StatusEnum.NONE);

turn_simulate(c1, c2)
