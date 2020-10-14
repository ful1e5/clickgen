#!/usr/bin/env python
# -*- coding: utf-8 -*-


from clickgen.configs.core import Config


class WindowsBuilder:
    """ Generate `x11` cursors """

    def __init__(self, config: Config) -> None:
        self._config = config
