#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""regmapGen это Генератор Регистровой Карты.
Он позволяет автоматически создавать пригодный для синтеза SystemVerilog код и документацию.
"""

__title__ = "regmapGen"
__description__ = "Генератор Регистровой Карты."
__version__ = '1.1.0'

from . import config                        # noqa: F401
from . import generators                    # noqa: F401
from .enum import EnumValue                 # noqa: F401
from .bitfield import BitField              # noqa: F401
from .reg import Register                   # noqa: F401
from .regmap import RegisterMap             # noqa: F401
from .register_node import RegisterNode     # noqa: F401
