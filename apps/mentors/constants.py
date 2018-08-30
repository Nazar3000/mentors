from enum import Enum


class Regions(Enum):
    # TODO: complete the list of regions
    KYIV = 'Kyiv'
    ZHYTOMYR = 'Zhytomyr'

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)
