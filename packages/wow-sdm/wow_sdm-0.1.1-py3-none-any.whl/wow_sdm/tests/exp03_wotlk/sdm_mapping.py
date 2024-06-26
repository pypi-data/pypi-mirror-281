# -*- coding: utf-8 -*-

from pathlib_mate import Path
from wow_sdm.api import get_values, concat_lists, exp03_wotlk
from wow_sdm.tests.exp03_wotlk.acc_enum import (
    AccountEnum as AccEnum,
    CharacterEnum as CharEnum,
)
from wow_sdm.tests.exp03_wotlk.acc_group import (
    AccountGroupEnum as AccGrpEnum,
    CharacterGroupEnum as CharGrpEnum,
)
from wow_sdm.tests.exp03_wotlk.sdm_enum import MacroEnum
from wow_sdm.tests.exp03_wotlk.sdm_group import MacroGroupEnum

Client = exp03_wotlk.Client
AccMap = exp03_wotlk.AccLvlMapping
CharMap = exp03_wotlk.CharLvlMapping
SdmMapping = exp03_wotlk.SdmMapping

dir_here = Path.dir_here(__file__)
dir_game_client = dir_here.joinpath("world_of_warcraft_zhCN")

client = exp03_wotlk.Client(
    locale="zhCN",
    dir=dir_game_client,
)
all_accounts = AccGrpEnum.all_accounts
all_characters = CharGrpEnum.all_characters

# ==============================================================================
# START of manual editing
# ==============================================================================
# ------------------------------------------------------------------------------
# acc_macros
# ------------------------------------------------------------------------------
acc_macros = AccMap.make_many(AccGrpEnum.all_accounts, MacroGroupEnum.acc_common)

# ------------------------------------------------------------------------------
# char_macros
# ------------------------------------------------------------------------------
char_macros = concat_lists(
    CharMap.make_many(
        CharGrpEnum.paladin_protect_retri, MacroGroupEnum.paladin_protect_retri
    ),
    CharMap.make_many(
        CharGrpEnum.shaman_elemental_resto, MacroGroupEnum.shaman_elemental_resto
    ),
)

# ==============================================================================
# END of manual editing
# ==============================================================================
# ------------------------------------------------------------------------------
# wtf_mapping
# ------------------------------------------------------------------------------
sdm_mapping = exp03_wotlk.SdmMapping(
    client=client,
    all_accounts=all_accounts,
    all_characters=all_characters,
    acc_macros=acc_macros,
    char_macros=char_macros,
)
