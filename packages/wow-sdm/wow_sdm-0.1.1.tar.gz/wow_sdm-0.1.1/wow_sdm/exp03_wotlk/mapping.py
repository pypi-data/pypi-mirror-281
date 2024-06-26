# -*- coding: utf-8 -*-

"""
这个模块的可以让你对 Account / Character 和宏命令 Yaml 文件进行排列组合, 然后一键将你的
配置文件应用到你的客户端中的 WTF 目录下.
"""

import typing as T
import dataclasses
from pathlib_mate import Path

from wow_acc.api import Account, Character

from ..logger import logger

from .model import SdmMacro, SdmLua


@dataclasses.dataclass
class Client:
    r"""
    代表着一个具体魔兽世界客户端. 你必须要指定这个客户端的目录. 然后就可以用各种 method 来
    获取对应的 SDM 插件 lua 文件的绝对路径了.

    :param dir: 客户端目录, 根据此目录可以定位其他的目录. 例如 "C:\Program Files\World of Warcraft"
    :param locale: 客户端语种, 例如 enUS, zhCN, zhTW 等.
    """

    dir: Path = dataclasses.field()
    locale: str = dataclasses.field()

    @property
    def dir_wtf(self) -> Path:
        return self.dir / "WTF"

    def get_account_sdm_lua(
        self,
        wtf_account_name: str,
    ) -> Path:
        r"""
        This file stores account level SDM AddOn configuration.

        Example: ``C:\...\WTF\Account\MYACCOUNT\SavedVariables\SuperDuperMacro.lua``
        """
        return self.dir_wtf.joinpath(
            "Account",
            wtf_account_name,
            "SavedVariables",
            "SuperDuperMacro.lua",
        )


@dataclasses.dataclass
class BaseMapping:
    """
    Mapping 是一个 Account / Character 和一个 Macro 文件的组合.
    """

    file: Path = dataclasses.field()


@dataclasses.dataclass
class AccLvlMapping(BaseMapping):
    """
    ``Account`` 和一个 Macro 文件的组合.

    :param acc: `wow_acc.api.Account <https://wow-acc.readthedocs.io/en/latest/wow_acc/model.html#wow_acc.model.Account>`_ 对象.
    :param file: Macro 文件的绝对路径.
    """

    acc: Account = dataclasses.field()
    file: Path = dataclasses.field()

    @classmethod
    def make_many(
        cls,
        account: T.Union[Account, T.Iterable[Account]],
        file: T.Union[Path, T.Iterable[Path]],
    ):
        """
        生成多个 ``Account`` 和 Macro 文件的组合. 让你写更少的代码.

        :param account: 单个 Account 或是多个 Account 的集合.
        :param file: 单个 Path 或是多个 Path 的集合.
        """
        if isinstance(account, Account):  # pragma: no cover
            accounts = [account]
        else:  # pragma: no cover
            accounts = account
        if isinstance(file, Path):  # pragma: no cover
            files = [file]
        else:
            files = file

        lst = list()
        for account in accounts:
            for file in files:
                lst.append(cls(acc=account, file=file))
        return lst


@dataclasses.dataclass
class CharLvlMapping(BaseMapping):
    """
    ``Character`` 和一个 Macro 文件的组合.

    :param char: `wow_acc.api.Character <https://wow-acc.readthedocs.io/en/latest/wow_acc/model.html#wow_acc.model.Character>`_ 对象.
    :param file: Macro 文件的绝对路径.
    """

    char: Character = dataclasses.field()
    file: Path = dataclasses.field()

    @classmethod
    def make_many(
        cls,
        character: T.Union[Character, T.Iterable[Character]],
        file: T.Union[Path, T.List[Path]],
    ):
        """
        生成多个 ``Character`` 和 Macro 文件的组合. 让你写更少的代码.

        :param character: 单个 Character 或是多个 Character 的集合.
        :param file: 单个 Path 或是多个 Path 的集合.
        """
        if isinstance(character, Character):  # pragma: no cover
            characters = [character]
        else:  # pragma: no cover
            characters = character
        if isinstance(file, Path):  # pragma: no cover
            files = [file]
        else:
            files = file

        lst = list()
        for character in characters:
            for file in files:
                lst.append(cls(char=character, file=file))
        return lst


@dataclasses.dataclass
class SdmMapping:
    """
    定义了一个魔兽世界客户端中被管理的所有 Sdm 宏命令的设定.

    :param client: :class:`Client` 对象. 有了这个才知道我们要将配置文件写到哪里去.
    :param all_accounts: 所有的 `wow_acc.api.Account <https://wow-acc.readthedocs.io/en/latest/wow_acc/model.html#wow_acc.model.Account>`_ 对象.
        在 render Jinja 模板时会用到.
    :param all_characters: 所有的 `wow_acc.api.Character <https://wow-acc.readthedocs.io/en/latest/wow_acc/model.html#wow_acc.model.Character>`_ 对象.
        在 render Jinja 模板时会用到.
    """

    # fmt: off
    client: Client
    all_accounts: T.Iterable[Account]
    all_characters: T.Iterable[Character]

    acc_macros: T.List[AccLvlMapping] = dataclasses.field(default_factory=list)
    char_macros: T.List[CharLvlMapping] = dataclasses.field(default_factory=list)
    # fmt: on

    @logger.emoji_block(msg="{func_name}", emoji="🎮")
    def apply(self, real_run: bool = False):
        """
        将 SDM 的 Lua 文件写入 ``SavedVariables`` 文件夹中.
        """
        # mapper 是一个以 account 为 key 的分组器
        mapper: T.Dict[str, T.List[SdmMacro]] = dict()

        for acc_map in self.acc_macros:
            macro = SdmMacro.from_yaml(acc_map.file)
            try:
                mapper[acc_map.acc.wtf_account_name].append(macro)
            except KeyError:
                mapper[acc_map.acc.wtf_account_name] = [macro]

        for char_map in self.char_macros:
            macro = SdmMacro.from_yaml(char_map.file)
            # 将其设定为 character macro
            macro.set_char(name=char_map.char.titled_character_name, realm=char_map.char.realm_name)
            try:
                mapper[char_map.char.account.wtf_account_name].append(macro)
            except KeyError:  # pragma: no cover
                mapper[char_map.char.account.wtf_account_name] = [macro]

        for wtf_account_name, macros in mapper.items():
            path_lua = self.client.get_account_sdm_lua(wtf_account_name)
            sdm_lua = SdmLua(
                path_lua=path_lua,
                macros=macros,
            )
            sdm_lua.write(real_run=real_run, verbose=True)
