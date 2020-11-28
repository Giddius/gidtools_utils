# region [Imports]

# * Standard Library Imports -->
import re
import random
from enum import Enum

# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import readit, writeit
from gidtools.gidtriumvirate import give_std_repr

# endregion [Imports]

__updated__ = '2020-11-26 22:08:23'

# region [Logging]

log = glog.aux_logger(__name__)
log.debug(glog.imported(__name__))

# endregion [Logging]


# region [Random_Class_RGB]

class RandomRGB:
    def __init__(self, alpha=0.25):
        self.name = 'rgb'
        self.last = {'r': 0, 'g': 0, 'b': 0}
        self.alpha = alpha

    def __call__(self):
        _list = [1, 1, 1]
        _back_list = [256, 256, 256]
        random.shuffle(_list)
        random.shuffle(_back_list)
        r = random.randint(_list[0], _back_list[0])
        g = random.randint(_list[1], _back_list[1])
        b = random.randint(_list[2], _back_list[2])
        self.last = {'r': r, 'g': g, 'b': b}

        return (r, g, b, self.alpha)

    def make_settings_region(self, in_settings, in_name_list):
        self.color_list = []
        for item in in_name_list:
            self.color_list.append(f'    "{item}": "{str(self)}",')
        col_reg_set_rex = re.compile('(?<="coloredRegions.namedColors": {\n).*?(?=},)', re.DOTALL)
        _out_str = '\n'.join(self.color_list) + '\n'
        _out_str += '    '
        writeit(in_settings, re.sub(col_reg_set_rex, _out_str, readit(in_settings)))

    def __repr__(self):
        return give_std_repr(self)

    def __str__(self):
        r, g, b, a = self.__call__()
        return f'rgb({str(r)}, {str(g)}, {str(b)}, {str(a)})'


# endregion [Random_Class_RGB]


# region [Class_1]

class RandomHSV:
    def __init__(self, hue_range=None, saturation_range=None, value_range=None, alpha=200):
        self.name = 'hsv'
        self.last = {'hue': 0, 'saturation': 0, 'value': 0}
        self.hue_range = (0, 359) if hue_range is None else hue_range
        self.saturation_range = (0, 255) if saturation_range is None else saturation_range
        self.value_range = (0, 255) if value_range is None else value_range
        self.alpha = alpha

    def __call__(self):
        hue = random.randint(self.hue_range[0], self.hue_range[1])
        saturation = random.randint(self.saturation_range[0], self.saturation_range[1])
        value = random.randint(self.value_range[0], self.value_range[1])
        self.last = {'hue': hue, 'saturation': saturation, 'value': value}

        return (hue, saturation, value, self.alpha)

    def __repr__(self):
        return give_std_repr(self)

    def __str__(self):
        hue, saturation, value, alpha = self.__call__()
        return f'hsv({str(hue)}, {str(saturation)}, {str(value)}, {str(alpha)})'

# endregion [Class_1]


# region [Class_2]

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

# endregion [Class_2]


# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
