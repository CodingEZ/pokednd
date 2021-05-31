from enum import Enum


class AttackEnum(Enum):
    PHYSICAL = 0
    SPECIAL = 1
    SELF_MODIFICATION = 2
    TARGET_MODIFICATION = 3
    SELF_HP = 4
    SELF_STATUS = 5
    TARGET_HP = 6
    TARGET_STATUS = 7
