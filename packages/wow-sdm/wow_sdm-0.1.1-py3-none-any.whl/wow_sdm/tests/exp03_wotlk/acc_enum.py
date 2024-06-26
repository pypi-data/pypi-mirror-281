# -*- coding: utf-8 -*-

from wow_sdm.tests.exp03_wotlk.acc_dataset import ds


# fmt: off
class AccountEnum:
    acc01 = ds.accounts["acc01"]
    acc02 = ds.accounts["acc02"]
    acc03 = ds.accounts["acc03"]
    acc04 = ds.accounts["acc04"]
    acc05 = ds.accounts["acc05"]


class RealmEnum:
    acc01_realm1 = ds.accounts["acc01"].realms_mapper["realm1"]
    acc02_realm1 = ds.accounts["acc02"].realms_mapper["realm1"]
    acc03_realm1 = ds.accounts["acc03"].realms_mapper["realm1"]
    acc04_realm1 = ds.accounts["acc04"].realms_mapper["realm1"]
    acc05_realm1 = ds.accounts["acc05"].realms_mapper["realm1"]


class CharacterEnum:
    acc01_realm1_mypaladin = ds.accounts["acc01"].realms_mapper["realm1"].characters_mapper["mypaladin"]
    acc02_realm1_myshaman1 = ds.accounts["acc02"].realms_mapper["realm1"].characters_mapper["myshaman1"]
    acc03_realm1_myshaman2 = ds.accounts["acc03"].realms_mapper["realm1"].characters_mapper["myshaman2"]
    acc04_realm1_myshaman3 = ds.accounts["acc04"].realms_mapper["realm1"].characters_mapper["myshaman3"]
    acc05_realm1_myshaman4 = ds.accounts["acc05"].realms_mapper["realm1"].characters_mapper["myshaman4"]
# fmt: on