from enum import Enum
from stat_enum import StatEnum


class RollData:
    def __init__(self, base, stat):
        self.base = base
        self.stat = stat


class ActionEnum(Enum):
    CRITICAL = 0
    HEAL_STATUS = 1
    HEAL_HP = 2
    MODIFIER = 3
    SCOUT = 4
    ESCAPE = 5

    ONLY_SLEEP_PROC = 6
    ONLY_BURN_PROC = 7
    ONLY_PARALYZE_PROC = 8
    ONLY_CONFUSION_PROC = 9

    SLEEP_PROC = 10
    SLEEP = 11
    BURN_PROC = 12
    PARALYZE_PROC = 13
    PARALYZE = 14
    FLINCH = 15
    CONFUSION_PROC = 16
    CONFUSION_SNAP = 17
    CONFUSION = 18
    ACCURACY = 19


ACTIONS = {
    ActionEnum.CRITICAL: RollData(0.05, StatEnum.LUCK),
    ActionEnum.HEAL_STATUS: RollData(0.3, StatEnum.WILLPOWER),
    ActionEnum.HEAL_HP: RollData(0.3, StatEnum.WISDOM),
    ActionEnum.MODIFIER: RollData(0.15, StatEnum.PERCEPTION),
    ActionEnum.SCOUT: RollData(0.8, StatEnum.CHARISMA),
    ActionEnum.ESCAPE: RollData(0.15, StatEnum.DEXTERITY),

    ActionEnum.ONLY_SLEEP_PROC: RollData(0.5, StatEnum.WILLPOWER),
    ActionEnum.ONLY_BURN_PROC: RollData(0.5, StatEnum.WISDOM),
    ActionEnum.ONLY_PARALYZE_PROC: RollData(0.5, StatEnum.WISDOM),
    ActionEnum.ONLY_CONFUSION_PROC: RollData(0.5, StatEnum.PERCEPTION),

    ActionEnum.SLEEP_PROC: RollData(0.1, StatEnum.WILLPOWER),
    ActionEnum.SLEEP: RollData(0.3, StatEnum.WILLPOWER),
    ActionEnum.BURN_PROC: RollData(0.1, StatEnum.WISDOM),
    ActionEnum.PARALYZE_PROC: RollData(0.1, StatEnum.WISDOM),
    ActionEnum.PARALYZE: RollData(0.25, StatEnum.WISDOM),
    ActionEnum.FLINCH: RollData(0.3, StatEnum.CHARISMA),
    ActionEnum.CONFUSION_PROC: RollData(0.3, StatEnum.PERCEPTION),
    ActionEnum.CONFUSION_SNAP: RollData(0.3, StatEnum.PERCEPTION),
    ActionEnum.CONFUSION: RollData(0.2, StatEnum.PERCEPTION),
    ActionEnum.ACCURACY: RollData(0.9, StatEnum.LUCK),
}
