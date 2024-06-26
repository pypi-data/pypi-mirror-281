# -*- coding: utf-8 -*-

"""
This module can help you organize your enum into group, made it easier to
construct mappings later.
"""

from wow_sdm.api import get_values
from wow_sdm.tests.exp03_wotlk.acc_enum import AccountEnum, CharacterEnum


# ==============================================================================
# START of manual editing
# ==============================================================================
class AccountGroupEnum:
    all_accounts = get_values(AccountEnum)


class CharacterGroupEnum:
    all_characters = get_values(CharacterEnum)

    paladin_protect_retri = [
        CharacterEnum.acc01_realm1_mypaladin,
    ]

    shaman_elemental_resto = [
        CharacterEnum.acc02_realm1_myshaman1,
        CharacterEnum.acc03_realm1_myshaman2,
        CharacterEnum.acc04_realm1_myshaman3,
        CharacterEnum.acc05_realm1_myshaman4,
    ]


# ==============================================================================
# END of manual editing
# ==============================================================================
