# -*- coding: utf-8 -*-

"""
This module can help you organize your enum into group, made it easier to
construct mappings later.
"""

from ordered_set import OrderedSet
from wow_sdm.api import get_values
from wow_sdm.tests.exp03_wotlk.sdm_enum import MacroEnum


# ==============================================================================
# START of manual editing
# ==============================================================================
class MacroGroupEnum:
    all_macros = get_values(MacroEnum)

    acc_common = [
        # GM command
        MacroEnum.f_00_common__1001_respawn,
        MacroEnum.f_00_common__1002_feigh_death,
        MacroEnum.f_00_common__1003_reset_cooldown,
        MacroEnum.f_00_common__1004_ice_block,
        MacroEnum.f_00_common__1005_resurrection,
        MacroEnum.f_00_common__1006_invisibility,
        MacroEnum.f_00_common__1007_unbind_instance,
        MacroEnum.f_00_common__1008_fly_up,
        MacroEnum.f_00_common__1009_fly_down,
        MacroEnum.f_00_common__1010_x32_speed,
        # Mount
        MacroEnum.f_00_common__1011_MountUp_zhTW,
        MacroEnum.f_00_common__1012_MountDown_zhTW,
        # Multi-box
        MacroEnum.f_00_common__1101_target_party,
        MacroEnum.f_00_common__1102_target_raid,
        MacroEnum.f_00_common__1103_target_focus_target,
        MacroEnum.f_00_common__1104_target_focus_target_target,
        MacroEnum.f_00_common__1105_confirm,
        MacroEnum.f_00_common__1106_set_focus,
        MacroEnum.f_00_common__1107_clear_focus,
        MacroEnum.f_00_common__1108_set_high_fps,
        MacroEnum.f_00_common__1109_set_low_fps,
        MacroEnum.f_00_common__1110_follow_focus,
        # Target specific character
        MacroEnum.f_00_common__1131_target_window_01,
        MacroEnum.f_00_common__1132_target_window_10,
        # Party and Raid
        MacroEnum.f_00_common__1151_invite_raid,
        MacroEnum.f_00_common__1152_leave_raid,
        MacroEnum.f_00_common__1153_summon,
        # Teleport
        MacroEnum.f_00_common__1173_tele_orgrimmar,
        MacroEnum.f_00_common__1174_tele_undercity,
        MacroEnum.f_00_common__1175_tele_shattrath,
        MacroEnum.f_00_common__1176_tele_dalaran,
    ]
    acc_common = OrderedSet(acc_common)

    paladin_protect_retri = [
        # Buff
        MacroEnum.f_02_paladin__1_protect_retri__11311_buff_self_alliance_zhCN,
        # Act
        MacroEnum.f_02_paladin__1_protect_retri__11301_act1_zhCN,
        MacroEnum.f_02_paladin__1_protect_retri__11302_act2_zhCN,
        MacroEnum.f_02_paladin__1_protect_retri__11303_act3_zhCN,
        MacroEnum.f_02_paladin__1_protect_retri__11304_act4_zhCN,
        MacroEnum.f_02_paladin__0_common__11131_protect_rotation_zhCN,
        MacroEnum.f_02_paladin__0_common__11132_retribution_rotation_zhCN,
    ]
    paladin_protect_retri = OrderedSet(paladin_protect_retri)

    shaman_elemental_resto = [
        # Command
        MacroEnum.f_05_shaman__0_common__14102_interrupt_zhCN,
        # Buff
        MacroEnum.f_05_shaman__1_elemental_resto__14311_buff_self_zhCN,
        # Act
        MacroEnum.f_05_shaman__0_common__14111_elemental_rotation_lv60_zhCN,
        MacroEnum.f_05_shaman__0_common__14112_resto_rotation_zhCN,
        MacroEnum.f_05_shaman__0_common__14114_mb_resto_earth_shield_zhCN,
        MacroEnum.f_05_shaman__1_elemental_resto__14312_burst_zhCN,
    ]
    shaman_elemental_resto = OrderedSet(shaman_elemental_resto)


# ==============================================================================
# END of manual editing
# ==============================================================================
