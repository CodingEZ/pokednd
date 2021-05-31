import math
import random
from action_enum import ActionEnum, ACTIONS
from attack_enum import AttackEnum
from move_enum import MoveEnum, SUPER_EFFECTIVE, NOT_VERY_EFFECTIVE
from status_enum import StatusEnum
from stat_enum import StatEnum


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

def stab_modifier(move_type, self_type):
    if self_type == move_type:
        return 1.5
    return 1.0

def effectiveness_modifier(move_type, opp_type):
    if opp_type in SUPER_EFFECTIVE[move_type]:
        print("Super effective!")
        return 1.25
    elif move_type in SUPER_EFFECTIVE[opp_type]:
        print("Not very effective")
        return 0.5
    return 1.0

def critical_modifier(attacker, defender):
    v1, v2 = roll(ACTIONS[ActionEnum.CRITICAL], attacker, defender)
    if (v1 < v2):
        print("DAS A CRIT!!!")
        return 2.0
    return 1.0


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

    def attack(self, opponent, attack_type, move_type, roll_fraction, status_type):
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
            v1, v2 = roll(ACTIONS[ActionEnum.ACCURACY], self, opponent)
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

            damage = max(0, self.level / 2 + attack_stat - opponent.defense)
            damage = damage * self.stat_modifier(attack_modifier)
            damage = damage / opponent.stat_modifier(StatEnum.DEFENSE)
            
            damage = damage * effectiveness_modifier(move_type, opponent.type)
            damage = damage * roll_fraction
            damage = max(2, math.floor(damage))
            damage = damage * critical_modifier(self, opponent)
            damage = damage * stab_modifier(move_type, self.type)
            damage = math.floor(damage)

            print(f"{self.name}'s attack does {damage} damage to {opponent.name}")
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