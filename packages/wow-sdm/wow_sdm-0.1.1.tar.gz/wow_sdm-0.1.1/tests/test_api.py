# -*- coding: utf-8 -*-

from wow_sdm import api


def test():
    _ = api
    _ = api.get_values
    _ = api.group_by
    _ = api.concat_lists
    _ = api.logger
    _ = api.exp03_wotlk

    exp03_wotlk = api.exp03_wotlk
    _ = exp03_wotlk.SdmCharacter
    _ = exp03_wotlk.SdmMacroTypeEnum
    _ = exp03_wotlk.SdmMacro
    _ = exp03_wotlk.SdmLua
    _ = exp03_wotlk.Client
    _ = exp03_wotlk.AccLvlMapping
    _ = exp03_wotlk.CharLvlMapping
    _ = exp03_wotlk.SdmMapping
    _ = exp03_wotlk.to_module
    _ = exp03_wotlk.Client.get_account_sdm_lua
    _ = exp03_wotlk.AccLvlMapping.make_many
    _ = exp03_wotlk.CharLvlMapping.make_many
    _ = exp03_wotlk.SdmMapping.apply


if __name__ == "__main__":
    from wow_sdm.tests import run_cov_test

    run_cov_test(__file__, "wow_sdm.api", preview=False)
