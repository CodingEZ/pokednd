import math
import random
from action_enum import ActionEnum, ACTIONS
from attack_enum import AttackEnum
from move_enum import MoveEnum, SUPER_EFFECTIVE, NOT_VERY_EFFECTIVE, IMMUNITY
from status_enum import StatusEnum
from stat_enum import StatEnum


def roll(rd, c1, c2):
    if rd.stat == StatEnum.CHARISMA:
        v1 = c1.charisma
        v2 = c2.charisma
    elif rd.stat == StatEnum.LUCK:
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


def stab_modifier(move_type, self_types):
    if move_type in self_types:
        return 1.5
    return 1.0


def effectiveness_modifier(move_type, defender):
    m = 1.0
    for t in defender.types:
        if t in SUPER_EFFECTIVE[move_type]:
            print("Super effective!")
            m *= 1.25
        elif t in NOT_VERY_EFFECTIVE[move_type]:
            print("Not very effective")
            m *= 0.5
        elif t in IMMUNITY[move_type]:
            print("Immunity")
            m *= 0.25
    return m


def critical_modifier(attacker, defender):
    v1, v2 = roll(ACTIONS[ActionEnum.CRITICAL], attacker, defender)
    if (v1 < v2):
        print("DAS A CRIT!!!")
        return 2.0
    return 1.0


def stat_modifier(stat, character):
    if stat == StatEnum.CONSTITUTION:
        raise Exception()
    elif stat == StatEnum.STRENGTH:
        modifier = character.strength_modifier
    elif stat == StatEnum.INTELLIGENCE:
        modifier = character.intelligence_modifier
    elif stat == StatEnum.DEFENSE:
        modifier = character.defense_modifier
    elif stat == StatEnum.DEXTERITY:
        modifier = character.dexterity_modifier
    elif stat == StatEnum.LUCK:
        modifier = character.luck_modifier
    else:
        raise Exception()
    return (2 + max(0, modifier)) / (2 - min(0, modifier))


class Character:
    BASE_HP = 20
    BASE_OTHER = 5

    def __init__(self, name, level, types, constitution, strength,
                 intelligence, defense, dexterity, charisma, wisdom,
                 willpower, perception, luck, strength_modifier,
                 intelligence_modifier, defense_modifier, dexterity_modifer,
                 luck_modifier, status, damage_taken):
        self.name = name
        self.level = level
        self.types = types

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

        self.is_burned = False

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
                or MoveEnum.GRASS in pokedata['types'] \
                or MoveEnum.POISON in pokedata['types']:
            willpower = 100
        else:
            willpower = 10

        if MoveEnum.FIGHTING in pokedata['types'] \
                or MoveEnum.ROCK in pokedata['types'] \
                or MoveEnum.FAIRY in pokedata['types']:
            charisma = 100
        else:
            charisma = 10

        if MoveEnum.ICE in pokedata['types'] \
                or MoveEnum.FLYING in pokedata['types'] \
                or MoveEnum.PSYCHIC in pokedata['types'] \
                or MoveEnum.BUG in pokedata['types']:
            perception = 100
        else:
            perception = 10

        if MoveEnum.FIGHTING in pokedata['types'] \
                or MoveEnum.DARK in pokedata['types'] \
                or MoveEnum.GHOST in pokedata['types']:
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

        constitution = math.floor(
            pokedata['hp'] * stat_scale * level_scale * stage_scale)
        strength = math.floor(
            pokedata['attack'] * stat_scale * level_scale * stage_scale)
        intelligence = math.floor(
            pokedata['sp_attack'] * stat_scale * level_scale * stage_scale)
        defense = math.floor(
            (pokedata['defense'] + pokedata['sp_defense']) / 2 * stat_scale * level_scale * stage_scale)
        dexterity = math.floor(
            pokedata['speed'] * stat_scale * level_scale * stage_scale)

        # allocate some mental stats forom concrete and typing
        # charisma = math.floor(pokedata['friendship'] * stat_scale * level_scale * stage_scale)
        # wisdom = math.floor(pokedata['weight'] * stat_scale * level_scale * stage_scale)
        charisma = math.floor(charisma * stat_scale *
                              level_scale * stage_scale)
        wisdom = math.floor(wisdom * stat_scale * level_scale * stage_scale)
        willpower = math.floor(willpower * stat_scale *
                               level_scale * stage_scale)
        perception = math.floor(
            perception * stat_scale * level_scale * stage_scale)
        luck = math.floor(luck * stat_scale * level_scale * stage_scale)

        return Character(
            "random", level, pokedata['types'],
            constitution, strength, intelligence, defense, dexterity,  # concrete
            charisma, wisdom, willpower, perception, luck,  # mental
            0, 0, 0, 0, 0,  # modifiers
            StatusEnum.NONE, 0)  # status

    def attack(self, opponent, attack_type, move_type, roll_fraction, status_type):
        # Accuracy check
        if attack_type == AttackEnum.PHYSICAL \
                or attack_type == AttackEnum.SPECIAL \
                or attack_type == AttackEnum.TARGET_HP \
                or attack_type == AttackEnum.TARGET_STATUS \
                or attack_type == AttackEnum.TARGET_MODIFICATION:
            v1, v2 = roll(ACTIONS[ActionEnum.ACCURACY], self, opponent)
            v2 = v2 * stat_modifier(StatEnum.LUCK, self)
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
            damage = damage * stat_modifier(attack_modifier, self)
            damage = damage / stat_modifier(StatEnum.DEFENSE, opponent)

            damage = damage * effectiveness_modifier(move_type, opponent)
            damage = damage * roll_fraction
            damage = max(2, math.floor(damage))
            damage = damage * critical_modifier(self, opponent)
            damage = damage * stab_modifier(move_type, self.types)
            damage = math.floor(damage)

            if self.is_burned:
                damage = max(2, damage//2)

            print(f"{self.name}'s attack does {damage} damage to {opponent.name}")
        elif attack_type == AttackEnum.TARGET_MODIFICATION \
                or attack_type == AttackEnum.TARGET_STATUS:
            damage = 0
        elif attack_type == AttackEnum.TARGET_HP:
            damage = 40
            print(f"{self.name}'s attack does {damage} damage to {opponent.name}")
        else:
            raise Exception()

        if attack_type == AttackEnum.PHYSICAL \
                or attack_type == AttackEnum.SPECIAL:
            if status_type == StatusEnum.SLEEP:
                v1, v2 = roll(ACTIONS[ActionEnum.SLEEP_PROC], self, opponent)
                if (v1 < v2):
                    print("Target is now asleep!")
            elif status_type == StatusEnum.PARALYZE:
                v1, v2 = roll(
                    ACTIONS[ActionEnum.PARALYZE_PROC], self, opponent)
                if (v1 < v2):
                    print("Target is now paralyzed!")
            elif status_type == StatusEnum.BURN:
                v1, v2 = roll(ACTIONS[ActionEnum.BURN_PROC], self, opponent)
                if (v1 < v2):
                    print("Target is now burned!")
            elif status_type == StatusEnum.CONFUSION:
                v1, v2 = roll(
                    ACTIONS[ActionEnum.CONFUSION_PROC], self, opponent)
                if (v1 < v2):
                    print("Target is now confused!")
            elif status_type == StatusEnum.FLINCH \
                    or status_type == StatusEnum.NONE:
                pass
            else:
                raise Exception()
        elif attack_type == AttackEnum.TARGET_MODIFICATION:
            pass
        elif attack_type == AttackEnum.TARGET_HP:
            pass
        elif attack_type == AttackEnum.TARGET_STATUS:
            v1, v2 = roll(ACTIONS[ActionEnum.ONLY_BURN_PROC], self, opponent)
            if (v1 > v2):
                print(f"{self.name} failed to burn the target!")
                return
            else:
                print(f"{self.name} burned the target!")
        else:
            raise Exception()

    def heal_hp(self, opponent, roll_fraction):
        v1, v2 = roll(ACTIONS[ActionEnum.HEAL_HP], self, opponent)
        if (v1 > v2):
            print(f"{self.name} fails to heal!")
            return
        else:
            print(f"{self.name} heals {roll_fraction * 100} percent of HP.")

    def heal_modifier(self, opponent):
        v1, v2 = roll(ACTIONS[ActionEnum.HEAL_MODIFIER], self, opponent)
        if (v1 > v2):
            print(f"{self.name} fails to heal!")
            return
        else:
            print(f"{self.name} heals a modifier.")

    def heal_status(self, opponent):
        v1, v2 = roll(ACTIONS[ActionEnum.HEAL_STATUS], self, opponent)
        if (v1 > v2):
            print(f"{self.name} fails to heal!")
            return
        else:
            print(f"{self.name} heals a status condition.")

    def scout(self, opponent):
        v1, v2 = roll(ACTIONS[ActionEnum.SCOUT], self, opponent)
        if (v1 > v2):
            print(f"{self.name} fails to scout!")
            return
        else:
            print(f"{self.name} scouts successfully.")

    def escape(self, opponent):
        v1, v2 = roll(ACTIONS[ActionEnum.ESCAPE], self, opponent)
        if (v1 > v2):
            print(f"{self.name} fails to escape.")
            return
        else:
            print(f"{self.name} escapes successfully.")
