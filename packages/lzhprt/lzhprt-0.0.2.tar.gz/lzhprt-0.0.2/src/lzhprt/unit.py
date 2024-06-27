# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package
from .base import Str, Int, Float
from .filler import Filler
from .styler import Styler


class Unit:
    def __init__(self, value, **argv):
        '''
        value_length: 值长度
        value_inpercent: 值是否展示为百分比
        fill_block: 填充字符
        fill_loc: 填充位置 ['left', 'l', 'center', 'c', 'right', 'r']
        fill_length: 填充长度 [None:不填充, -1:动态填充, >=0:固定填充]
        style_effect: 样式效果 ['bold', 'b', 'underline', 'u', 'blink', 'l', 'reverse', 'r', 'invisible', 'i']
        style_front: 前景色 ['black', 'd', 'red', 'r', 'green', 'g', 'yellow', 'y', 'blue', 'b', 'purple', 'p', 'cyan', 'c', 'white', 'w']
        style_back: 背景色 ['black', 'd', 'red', 'r', 'green', 'g', 'yellow', 'y', 'blue', 'b', 'purple', 'p', 'cyan', 'c', 'white', 'w']
        '''
        for bclass in [Str, Int, Float]:
            if (type(value) in bclass.types()):
                self.base = bclass(value, **argv)
                break
        if (not hasattr(self, 'base')):
            self.base = Str(str(value), **argv)
        self.filler = Filler(**argv)
        self.styler = Styler(**argv)

    def _get_str(self):
        return self.base.__repr__()

    def _get_filled(self):
        return self.filler.fill(self._get_str())

    def _get_unit(self):
        return self.styler(self._get_filled())

    def __repr__(self):
        return self._get_unit()

    def is_dynamic(self):
        return self.filler.length == -1

    def get_length(self):
        return len(self._get_filled())
