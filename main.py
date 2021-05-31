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


choice_decision = [
    ('Decision', '', None),
    ('1', 'scout', None),
    ('2', 'heal hp', None),
    ('3', 'heal modifier', None),
    ('4', 'heal status', None),
    ('5', 'attack', None),
    ('What is your decision?', '', None),
]

choice_attack_type = [
    ('Attack type', '', None),
    ('1', 'physical', AttackEnum.PHYSICAL),
    ('2', 'special', AttackEnum.SPECIAL),
    ('3', 'target_hp', AttackEnum.TARGET_HP),
    ('4', 'target_modification', AttackEnum.TARGET_MODIFICATION),
    ('5', 'target_status', AttackEnum.TARGET_STATUS),
    ('Choose an attack type', '', None),
]

choice_status_type = [
    ('Status type', '', None),
    ('1', 'sleep', StatusEnum.SLEEP),
    ('2', 'paralyze', StatusEnum.PARALYZE),
    ('3', 'burn', StatusEnum.BURN),
    ('4', 'confusion', StatusEnum.CONFUSION),
    ('5', 'flinch', StatusEnum.FLINCH),
    ('6', 'none', StatusEnum.NONE),
    ('Choose an status type', '', None),
]


def input_text(lst):
    s = []
    for e in lst:
        s.append(f"{e[0]}: {e[1]}")
    return '\n'.join(s)


def make_choice(lst, choice):
    for e in lst:
        if e[2] is None:
            continue
        if e[0] == choice:
            return e[2]
    return None


def turn_simulate(c1, c2):
    while True:
        decision = input(input_text(choice_decision))
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
        attack_type = input(input_text(choice_attack_type))
        attack_type = make_choice(choice_attack_type, attack_type)
        if attack_type is not None:
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
        status_type = input(input_text(choice_status_type))
        status_type = make_choice(choice_status_type, status_type)
        if status_type is not None:
            break
    print()

    if attack_type == AttackEnum.PHYSICAL or attack_type == AttackEnum.SPECIAL:
        roll_fraction = roll_power()
    else:
        roll_fraction = 0

    c1.attack(c2, attack_type, move_type, roll_fraction, status_type)


# c2 = Character.create("EZ", POKEDATA["Treecko"], 1, 10)
c3 = Character.create("???", POKEDATA["Metapod"], 1, 10,
    0, 0, 1, 0, 0,  # modifiers
    False, False, False, True)  # status
# c3 = Character.create("Octillery", POKEDATA["Octillery"], 2, 20)

c1 = Character(
    "Techno", 10, [MoveEnum.FIRE],
    2, 1, 3, 1, 3,  # concrete
    1, 1, 2, 1, 2,  # mental
    0, 0, 0, 0, 0,  # modifiers
    True, False, False, False)  # status
c2 = Character(
    "EZ", 10, [MoveEnum.GRASS],
    2, 2, 3, 2, 3,  # concrete
    0, 0, 5, 0, 0,  # mental
    0, 0, 0, 0, 0,  # modifiers
    False, True, False, False)  # status

# c5 = Character.create(POKEDATA["Treecko"], 1, 10)
# print(c5)

turn_simulate(c1, c3)
