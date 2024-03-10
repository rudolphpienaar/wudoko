"""
Some models used by Jobber
"""

from pydantic_settings          import BaseSettings
from pathlib                    import Path
from enum                       import Enum
from argparse                   import Namespace
from multiprocessing.managers   import BaseManager

class Space(Namespace):
    """ A namespace that can check if it has an attribute """
    def has(self, attrib:str) -> bool:
        return hasattr(self, attrib)

    def rm(self, attrib:str) -> bool:
        if not self.has(attrib):
            return False
        delattr(self, attrib)
        return True

class BreakOut(Exception):
    """ This is just dummy "custom" exception class. We use this
        to raise a BreakOut exception if we want to break out of
        a code block (for instance a group of nested for loops
    """
    pass

class GridDir(Enum):
    """ Directions in grid """
    N   = 1
    S   = 2
    E   = 3
    W   = 4
    NE  = 5
    NW  = 6
    SE  = 7
    SW  = 8

class Orient(Enum):
    row = 1
    col = 2

class GridCoord(BaseSettings):
    """ A row,col (y, x) coordinate in a grid """
    x:int                   = 0
    y:int                   = 0

    def __add__(self, coord):
        if isinstance(coord, GridCoord):
            return GridCoord(x = self.x + coord.x, y = self.y + coord.y)
        else:
            raise TypeError(
                "Unsupported operand type for +: 'GridCoord' and '{}'".
                format(type(coord).__name__))

    def __str__(self):
        return f'({self.x}, {self.y})'

    def tuple(self) -> tuple[int, int]:
        return self.x, self.y

class Dimensions(GridCoord):
    """ Just another name for a GridCoord """
    pass
