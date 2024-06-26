# -*- coding: utf-8 -*-

from pathlib_mate import Path
from wow_sdm.api import exp03_wotlk

dir_here = Path.dir_here(__file__)
dir_root = dir_here.joinpath("sdm_macros")

if __name__ == "__main__":
    content = exp03_wotlk.to_module(
        dir_root=dir_root,
        import_dir_root_line="from .sdm_dataset import dir_root",
    )
    dir_here.joinpath("sdm_enum.py").write_text(content, encoding="utf-8")
