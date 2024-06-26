.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2024-06-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release.
- Add the following public API:
    - :func:`get_values <wow_sdm.utils.get_values>`
    - :func:`group_by <wow_sdm.utils.group_by>`
    - :func:`concat_lists <wow_sdm.utils.concat_lists>`
    - :func:`apply <wow_sdm.utils.apply>`
    - :attr:`logger <wow_sdm.logger.logger>`
    - :mod:`exp03_wotlk <wow_sdm.exp03_wotlk.api>`
    - :class:`exp03_wotlk.model.SdmCharacter <wow_sdm.exp03_wotlk.model.SdmCharacter>`
    - :class:`exp03_wotlk.model.SdmMacroTypeEnum <wow_sdm.exp03_wotlk.model.SdmMacroTypeEnum>`
    - :class:`exp03_wotlk.model.SdmMacro <wow_sdm.exp03_wotlk.model.SdmMacro>`
    - :class:`exp03_wotlk.model.SdmLua <wow_sdm.exp03_wotlk.model.SdmLua>`
    - :class:`exp03_wotlk.Client <wow_sdm.exp03_wotlk.mapping.Client>`
    - :class:`exp03_wotlk.AccLvlMapping <wow_sdm.exp03_wotlk.mapping.AccLvlMapping>`
    - :class:`exp03_wotlk.CharLvlMapping <wow_sdm.exp03_wotlk.mapping.CharLvlMapping>`
    - :class:`exp03_wotlk.SdmMapping <wow_sdm.exp03_wotlk.mapping.SdmMapping>`
    - :class:`exp03_wotlk.to_module <wow_sdm.exp03_wotlk.dataset.to_module>`
    - :meth:`exp03_wotlk.Client.get_account_sdm_lua <wow_sdm.exp03_wotlk.mapping.Client.get_account_sdm_lua>`
    - :meth:`exp03_wotlk.AccLvlMapping.make_many <wow_sdm.exp03_wotlk.mapping.AccLvlMapping.make_many>`
    - :meth:`exp03_wotlk.CharLvlMapping.make_many <wow_sdm.exp03_wotlk.mapping.CharLvlMapping.make_many>`
    - :meth:`exp03_wotlk.SdmMapping.apply <wow_sdm.exp03_wotlk.mapping.SdmMapping.apply>`
