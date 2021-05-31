import math
import random
from enum import Enum

from action_enum import ActionEnum, ACTIONS
from attack_enum import AttackEnum
from move_enum import MoveEnum, SUPER_EFFECTIVE, NOT_VERY_EFFECTIVE
from status_enum import StatusEnum
from stat_enum import StatEnum
from data import POKEDATA


def roll(rd, c1, c2):
    if rd.stat == StatEnum.LUCK:
        v1 = c1.luck
        v2 = c2.luck
    elif rd.stat == StatEnum.WILLPOWER:
        v1 = c1.willpower
        v2 = c2.willpower
    elif rd.stat == StatEnum.WISDOM:
        v1 = c1.wisdom
        v2 = c2.wisdom
    elif rd.stat == StatEnum.PERCEPTION:
        v1 = c1.perception
        v2 = c2.perception
    elif rd.stat == StatEnum.DEXTERITY:
        v1 = c1.dexterity
        v2 = c2.dexterity
    else:
        raise Exception()
    return random.random(), rd.base * (v1 / v2) ** 1.25

class Character:
    BASE_HP = 20
    BASE_OTHER = 5

    def __init__(self, name, level, type, constitution, strength,
        intelligence, defense, dexterity, charisma, wisdom,
        willpower, perception, luck, strength_modifier,
        intelligence_modifier, defense_modifier, dexterity_modifer,
        luck_modifier, status, damage_taken):
        self.name = name
        self.level = level
        self.type = type

        self.constitution = constitution * 10 + __class__.BASE_HP
        self.strength = strength + __class__.BASE_OTHER
        self.intelligence = intelligence + __class__.BASE_OTHER
        self.defense = defense + __class__.BASE_OTHER
        self.dexterity = dexterity + __class__.BASE_OTHER

        self.charisma = charisma + __class__.BASE_OTHER
        self.wisdom = wisdom + __class__.BASE_OTHER
        self.willpower = willpower + __class__.BASE_OTHER
        self.perception = perception + __class__.BASE_OTHER
        self.luck = luck + __class__.BASE_OTHER

        self.strength_modifier = strength_modifier
        self.intelligence_modifier = intelligence_modifier
        self.defense_modifier = defense_modifier
        self.dexterity_modifer = dexterity_modifer

        self.luck_modifier = luck_modifier

        self.status = status
        self.damage_taken = damage_taken

    def __str__(self):
        return f"""Constitution: {self.constitution}
Strength: {self.strength}
Intelligence: {self.intelligence}
Defense: {self.defense}
Dexterity: {self.dexterity}
Charisma: {self.charisma}
Wisdom: {self.wisdom}
Willpower: {self.willpower}
Perception: {self.perception}
Luck: {self.luck}"""

    @staticmethod
    def create(pokedata, stage, level):
        if MoveEnum.DRAGON in pokedata['types'] \
            or MoveEnum.ELECTRIC in pokedata['types'] \
            or MoveEnum.FIRE in pokedata['types']:
            wisdom = 100
        else:
            wisdom = 10

        if MoveEnum.GROUND in pokedata['types'] \
            or MoveEnum.STEEL in pokedata['types'] \
            or MoveEnum.GRASS in pokedata['types']:
            willpower = 100
        else:
            willpower = 10

        if MoveEnum.FLYING in pokedata['types'] \
            or MoveEnum.DARK in pokedata['types']:
            charisma = 100
        else:
            charisma = 10

        if MoveEnum.WATER in pokedata['types'] \
            or MoveEnum.PSYCHIC in  pokedata['types']:
            perception = 100
        else:
            perception = 10

        if MoveEnum.FIGHTING in pokedata['types'] \
            or MoveEnum.FAIRY in pokedata['types']:
            luck = 100
        else:
            luck = 10

        total = pokedata['hp'] + pokedata['attack'] + pokedata['defense'] + pokedata['sp_attack'] + pokedata['sp_defense'] + pokedata['speed'] \
            + charisma + wisdom + willpower + perception + luck
        stat_scale = 1000 * 0.8 / total

        level_scale = level / 100

        if stage == 1:
            stage_scale = 0.3
        elif stage == 2:
            stage_scale = 0.55
        elif stage == 3:
            stage_scale = 0.8
        elif stage == 4:
            stage_scale = 1.0
        else:
            raise Exception()

        constitution = math.floor(pokedata['hp'] * stat_scale * level_scale * stage_scale)
        strength = math.floor(pokedata['attack'] * stat_scale * level_scale * stage_scale)
        intelligence = math.floor(pokedata['sp_attack'] * stat_scale * level_scale * stage_scale)
        defense = math.floor((pokedata['defense'] + pokedata['sp_defense']) / 2 * stat_scale * level_scale * stage_scale)
        dexterity = math.floor(pokedata['speed'] * stat_scale * level_scale * stage_scale)

        # allocate some mental stats forom concrete and typing
        # charisma = math.floor(pokedata['friendship'] * stat_scale * level_scale * stage_scale)
        # wisdom = math.floor(pokedata['weight'] * stat_scale * level_scale * stage_scale)
        charisma = math.floor(charisma * stat_scale * level_scale * stage_scale)
        wisdom = math.floor(wisdom * stat_scale * level_scale * stage_scale)
        willpower = math.floor(willpower * stat_scale * level_scale * stage_scale)
        perception = math.floor(perception * stat_scale * level_scale * stage_scale)
        luck = math.floor(luck * stat_scale * level_scale * stage_scale)

        return Character(
            "random", level, pokedata['types'][0], 
            constitution, strength, intelligence, defense, dexterity, # concrete
            charisma, wisdom, willpower, perception, luck, # mental
            0, 0, 0, 0, 0, # modifiers
            StatusEnum.NONE, 0) # status

    def stab_modifier(self, attack_type):
        if self.type == attack_type:
            return 1.5
        return 1.0

    def effectiveness_modifier(self, move_type, opp_type):
        if opp_type in SUPER_EFFECTIVE[move_type]:
            print("Super effective!")
            return 1.25
        elif move_type in SUPER_EFFECTIVE[opp_type]:
            print("Not very effective")
            return 0.5
        return 1.0

    def critical_modifier(self, character):
        v1, v2 = roll(ACTIONS[ActionEnum.CRITICAL], self, character)
        if (v1 < v2):
            print("DAS A CRIT!!!")
            return 2.0
        return 1.0

    def stat_modifier(self, stat):
        if stat == StatEnum.CONSTITUTION:
            raise Exception()
        elif stat == StatEnum.STRENGTH:
            modifier = self.strength_modifier
        elif stat == StatEnum.INTELLIGENCE:
            modifier = self.intelligence_modifier
        elif stat == StatEnum.DEFENSE:
            modifier = self.defense_modifier
        elif stat == StatEnum.DEXTERITY:
            modifier = self.dexterity_modifier
        elif stat == StatEnum.LUCK:
            modifier = self.luck_modifier
        else:
            raise Exception()
        return (2 + max(0, modifier)) / (2 - min(0, modifier))

    def attack(self, character, attack_type, move_type, roll_fraction, status_type):
        # Accuracy check
        if attack_type == AttackEnum.SELF_HP \
            or attack_type == AttackEnum.SELF_MODIFICATION \
            or attack_type == AttackEnum.SELF_STATUS:
            pass
        elif attack_type == AttackEnum.PHYSICAL \
            or attack_type == AttackEnum.SPECIAL \
            or attack_type == AttackEnum.TARGET_HP \
            or attack_type == AttackEnum.TARGET_STATUS \
            or attack_type == AttackEnum.TARGET_MODIFICATION:
            v1, v2 = roll(ACTIONS[ActionEnum.ACCURACY], self, character)
            v2 = v2 * self.stat_modifier(StatEnum.LUCK)
            if (v1 > v2):
                print(self.name + "'s attack missed!")
                return
        else:
            raise Exception()

        # Damage calc
        damage = 0
        if attack_type == AttackEnum.PHYSICAL \
            or attack_type == AttackEnum.SPECIAL:
            if attack_type == AttackEnum.PHYSICAL:
                attack_stat = self.strength
                attack_modifier = StatEnum.STRENGTH
            else:
                attack_stat = self.intelligence
                attack_modifier = StatEnum.INTELLIGENCE

            damage = max(0, self.level / 2 + attack_stat - character.defense)
            damage = damage * self.stat_modifier(attack_modifier)
            damage = damage / character.stat_modifier(StatEnum.DEFENSE)
            
            damage = damage * self.effectiveness_modifier(move_type, character.type)
            damage = damage * roll_fraction
            damage = max(2, math.floor(damage))
            damage = damage * self.critical_modifier(character)
            damage = damage * self.stab_modifier(move_type)
            damage = math.floor(damage)

            print(f"{self.name}'s attack does {damage} damage to {character.name}")
        elif attack_type == AttackEnum.SELF_MODIFICATION \
            or attack_type == AttackEnum.TARGET_MODIFICATION \
            or attack_type == AttackEnum.SELF_HP \
            or attack_type == AttackEnum.SELF_STATUS \
            or attack_type == AttackEnum.TARGET_STATUS:
            damage = 0
        elif attack_type == AttackEnum.TARGET_HP:
            damage = 40
        else:
            raise Exception()

        if attack_type == AttackEnum.PHYSICAL \
            or attack_type == AttackEnum.SPECIAL:
                if status_type == StatusEnum.SLEEP:
                    roll(ACTIONS[ActionEnum.SLEEP_PROC], self, character)
                elif status_type == StatusEnum.PARALYZE:
                    roll(ACTIONS[ActionEnum.PARALYZE_PROC], self, character)
                elif status_type == StatusEnum.BURN:
                    roll(ACTIONS[ActionEnum.BURN_PROC], self, character)
                elif status_type == StatusEnum.CONFUSION:
                    roll(ACTIONS[ActionEnum.CONFUSION_PROC], self, character)
                elif status_type == StatusEnum.FLINCH \
                    or status_type == StatusEnum.NONE:
                    pass
                else:
                    raise Exception()
        elif attack_type == AttackEnum.SELF_MODIFICATION:
            pass
        elif attack_type == AttackEnum.TARGET_MODIFICATION:
            pass
        elif attack_type == AttackEnum.SELF_HP:
            v1, v2 = roll(Actions.HEAL_HP, self, character)
            if (v1 > v2):
                print(self.name + " failed to heal!")
                return
            else:
                print(self.name + " healed 50% of HP.")
        elif attack_type == AttackEnum.TARGET_HP:
            pass
        elif attack_type == AttackEnum.SELF_STATUS:
            pass
        elif attack_type == AttackEnum.TARGET_STATUS:
            v1, v2 = roll(Actions.ONLY_BURN_PROC, self, character)
            if (v1 > v2):
                print(f"{self.name} failed to burn the target!")
                return
            else:
                print(f"{self.name} burned the target!")
        else:
            raise Exception()

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
            attack_type = SELF_HP
            break
        elif attack_type == "6":
            attack_type = SELF_STATUS
            break
        elif attack_type == "7":
            attack_type = TARGET_HP
            break
        elif attack_type == "8":
            attack_type = TARGET_STATUS
            break

    print()

    while True:
        move_type = input("Move Type (fire/grass/water/etc): ")
        if move_type == "normal":
            move_type = MoveEnum.NORMAL
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
        elif move_type == "psychic":
            move_type = MoveEnum.PSYCHIC
            break
        elif move_type == "dark":
            move_type = MoveEnum.DARK
            break
        elif move_type == "fighting":
            move_type = MoveEnum.FIGHTING
            break
        elif move_type == "dragon":
            move_type = MoveEnum.DRAGON
            break
        elif move_type == "fairy":
            move_type = MoveEnum.FAIRY
            break
        elif move_type == "steel":
            move_type = MoveEnum.STEEL
            break
        elif move_type == "flying":
            move_type = MoveEnum.FLYING
            break
        elif move_type == "ground":
            move_type = MoveEnum.GROUND
            break
        elif move_type == "electric":
            move_type = MoveEnum.ELECTRIC
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
    "Techno", 10, MoveEnum.FIRE, 
    2, 1, 3, 1, 3, # concrete
    1, 1, 2, 1, 2, # mental
    -2, 0, 0, 0, 0, # modifiers
    StatusEnum.NONE, 0) # status
c2 = Character(
    "Squirrel", 8, MoveEnum.NORMAL, 
    2, 2, 2, 4, 2, # concrete
    1, 1, 1, 1, 1, # mental
    2, 0, 0, 2, 1, # modifiers
    StatusEnum.NONE, 0) # status
c3 = Character(
    "Octopus", 8, MoveEnum.WATER, 
    0, 0, 17, 0, 0, # concrete
    0, 0, 0, 0, 0, # mental
    0, 0, 0, 0, 0, # modifiers
    StatusEnum.NONE, 0) # status
c4 = Character(
    "Raccoon", 25, MoveEnum.GRASS, 
    0, 0, 0, 0, 0, # concrete
    0, 0, 0, 0, 0, # mental
    0, 0, 0, 0, 0, # modifiers
    StatusEnum.NONE, 0) # status

print(Character.create(POKEDATA["Bulbasaur"], 1, 10))
print(Character.create(POKEDATA["Charizard"], 3, 70))

# c1.attack(c2, AttackEnum.SPECIAL, MoveEnum.FIRE, .5, StatusEnum.BURN)
# c2.attack(c1, AttackEnum.PHYSICAL, MoveEnum.NORMAL, .5, StatusEnum.NONE)

# c1.attack(c2, AttackEnum.SPECIAL, MoveEnum.FIGHTING, 0, StatusEnum.NONE);
# c3.attack(c1, AttackEnum.SPECIAL, MoveEnum.WATER, .80, StatusEnum.NONE);

turn_simulate(c1, c2)
