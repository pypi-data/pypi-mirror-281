# -*- coding: utf-8 -*-

"""
为了能实现用 Python 来操作 SDM 插件的 ``SavedVariables/SuperDuperMacro.lua`` 文件,
我们要对 .lua 文件中的代码块进行数据建模, 定义一些 Python 类来代表这些代码块, 然后实现将
Python 对象转化为 .lua 代码块的逻辑.
"""

import typing as T
import dataclasses

from jinja2 import Template
from pathlib_mate import Path
from yaml import load, SafeLoader

from ..utils import apply


_dir_here = Path.dir_here(__file__)
_path_sdm_template = _dir_here / "sdm.tpl"
_sdm_template = Template(_path_sdm_template.read_text(encoding="utf-8"))


@dataclasses.dataclass
class SdmCharacter:
    """
    代表 Character Macro 专有宏命令中关于角色信息的部分. 对应着如下代码块:

    .. code-block:: lua

        ["character"] = {
            ["name"] = "charname",
            ["realm"] = "realmname",
        },
    """

    name: str = dataclasses.field()
    realm: str = dataclasses.field()


class SdmMacroTypeEnum:
    """
    枚举 SDM 宏命令的三种类型.
    """

    button = "b"
    floating = "f"
    script = "s"


_DEFAULT_TYPE = SdmMacroTypeEnum.button  # 默认的宏命令类型
_DEFAULT_ID = 0  # 默认的起始 ID
_DEFAULT_ICON = 1  # 默认的宏命令图标


@dataclasses.dataclass
class SdmMacro:
    """
    定义了一个魔兽世界中的 SDM 宏命令的抽象, 目前只支持 Button + Global 这一种模式.

    代表着如下代码块:

    .. code-block:: lua

        {
            ["type"] = "f",
            ["name"] = "macroname",
            ["character"] = {
                ["name"] = "charname",
                ["realm"] = "realmname",
            },
            ["ID"] = 1,
            ["text"] = "/s hello",
            ["icon"] = 1,
        }, -- [1]
    """

    name: str = dataclasses.field()
    character: T.Optional[SdmCharacter] = dataclasses.field(default=None)
    type: str = dataclasses.field(default=_DEFAULT_TYPE)
    id: int = dataclasses.field(default=_DEFAULT_ID)  # SDM macro ID starts from 0
    icon: int = dataclasses.field(default=_DEFAULT_ICON)  # 1 is the Question Mark Icon
    text: str = dataclasses.field(default="")

    def set_id(self, id: int) -> "SdmMacro":  # pragma: no cover
        """
        Update it's attributes value.
        """
        self.id = id
        return self

    def set_char(self, name: str, realm: str) -> "SdmMacro":  # pragma: no cover
        """
        Update it's attributes value.
        """
        if self.character is None:
            self.character = SdmCharacter(
                name=name,
                realm=realm,
            )
        else:
            self.character.name = name
            self.character.realm = realm
        return self

    def is_global(self) -> bool:
        """
        Is this SDM macro a global macro or character macro
        """
        if self.character is None:  # pragma: no cover
            return True
        elif (self.character.name is None) or (self.character.realm is None):
            return True
        else:
            return False

    def encode_text(self) -> str:
        """
        Encode macro text to single-ling Lua string. The final string of the
        macro body in lua has to have only one line.
        """
        return self.text.replace("\n", "\\n")

    @classmethod
    def from_yaml(cls, stream) -> "SdmMacro":
        """
        从人类可读写的 yaml 文件中读取数据, 创建 :class:`SDMMacro` 对象. 这是我们
        这个模块的最核心的方法, 也是能让我们用 yaml 文件来维护宏命令的关键.

        下面是一个示例的 yaml 文件.

        .. code-block:: yaml

            name: interrupt
            character:
              name:
              realm:
            type: b
            id:
            # you can find icon id on https://wotlk.evowow.com/?icons
            icon:
            description: |
              cancel casting spell, interrupt enemy casting immediately!
            text: |
              #showtooltip
              /stopcasting
              /cast Counterspell

        :param stream: 可以是 yaml 文件的字符串内容, 也可是 yaml 的 Path 对象,
            也可以是 file object 对象.
        """
        if isinstance(stream, str):  # pragma: no cover
            data = load(stream, SafeLoader)
        elif isinstance(stream, Path):
            with stream.open("r", encoding="utf-8") as f:
                data = load(f, SafeLoader)
        else:  # pragma: no cover
            data = load(stream, SafeLoader)
        return cls(
            name=data["name"],
            character=SdmCharacter(**data["character"]),
            type=data["type"] if data["type"] else _DEFAULT_TYPE,
            id=data["id"] if data["id"] else _DEFAULT_ID,
            icon=data["icon"] if data["icon"] else _DEFAULT_ICON,
            text=data["text"].strip(),
        )

    def render(self) -> str:
        """
        Render the corresponding SuperDupeMacro.lua code. See example at
        :class:`SDMMacro`.
        """
        lines: T.List[str] = list()
        lines.append(f"[{self.id}] = {{")
        lines.append(f'    ["type"] = "{self.type}",')
        lines.append(f'    ["name"] = "{self.name}",')
        if self.is_global() is False:
            lines.append(f'    ["character"] = {{')
            lines.append(f'        ["name"] = "{self.character.name}",')
            lines.append(f'        ["realm"] = "{self.character.realm}",')
            lines.append(f"    }},")
        lines.append(f'    ["ID"] = {self.id},')
        lines.append(f'    ["icon"] = {self.icon},')
        lines.append(f'    ["text"] = "{self.encode_text()}",')
        lines.append(f"}},")
        return "\n".join(lines)


@dataclasses.dataclass
class SdmLua:
    """
    代表了 ``SuperDupeMacro.lua`` 文件的抽象. 该类只能用于将数据写入到 ``SuperDupeMacro.lua``,
    而不能从 ``SuperDupeMacro.lua`` 中读取数据.

    :param path_lua: ``SuperDupeMacro.lua`` 文件路径.
    :param macros: :class:`SDMMacro` 对象的列表.
    """

    path_lua: Path = dataclasses.field()
    macros: T.List[SdmMacro] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.check_path_lua()
        self.check_macros()

    def check_path_lua(self):
        """
        检查 :attr:`SdmLua.path_lua` 是否是 SuperDupeMacro.lua 文件.
        """
        if self.path_lua.basename != "SuperDuperMacro.lua":  # pragma: no cover
            raise ValueError(f"the SDMLua.path_lua has to end with SuperDupeMacro.lua!")

    def check_macros(self):
        """
        检查 :attr:`SdmLua.macros` 中是否有重复的 macro id.
        """
        id_set = {macro.id for macro in self.macros}
        if len(id_set) != len(self.macros):  # pragma: no cover
            macro_id_list = [macro.id for macro in self.macros]
            raise ValueError(
                f"Cannot render SDM lua! Found duplicate id in 'macro_list': {macro_id_list}"
            )

    def render(self) -> str:
        """
        将一堆 :class:`SDMMacro` 对象渲染成 SuperDupeMacro.lua 文件的内容 (只是生成内容
        而不将内容写入文件). 这里面会检查 macro_list 中的 macro id 是否有重复, 如果有重复,
        则会抛出异常.
        """
        return _sdm_template.render(macros=self.macros)

    def write(
        self,
        real_run: bool = True,
        verbose: bool = False,
    ) -> str:  # pragma: no cover
        content = self.render()
        apply(
            path=self.path_lua,
            content=content,
            real_run=real_run,
            verbose=verbose,
        )
        return content
