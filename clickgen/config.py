#!/usr/bin/env python
# -*- coding: utf-8 -*-


from clickgen.typing import ThemeInfo, ThemeSettings


class Config:
    """ Configure `clickgen` modules. """

    def __init__(
        self,
        info: ThemeInfo,
        settings: ThemeSettings,
    ) -> None:
        # Default "comment" for cursor theme
        comment: str = f"{info.theme_name} By {info.author}"
        if info.comment:
            comment = info.comment

        self.info: ThemeInfo = ThemeInfo(
            theme_name=info.theme_name,
            author=info.author,
            comment=comment,
            url=info.url,
        )

        self.settings: ThemeSettings = settings
