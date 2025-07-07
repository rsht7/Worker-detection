# utils/constants.py

from enum import IntEnum


class Rule(IntEnum):
    PERSON_IN_RESTRICTED_ZONE = 1
    # Add more as needed


# Reverse map for display/debug
RULE_NAMES = {v: k for k, v in Rule.__members__.items()}


class Alert(IntEnum):
    ANOMALY = 1
    NEAR_MISS = 2


# Reverse map for display/debug
RULE_NAMES = {v: k for k, v in Alert.__members__.items()}
