"""
The trajectory module determines trajectories in a grid space
"""

from    argparse            import Namespace
from    wudoko.lib.path     import Path
from    wudoko.models       import data
from    wudoko.models.data  import GridDir

class Trajectory:

    def __init__(self, gridSize:data.Dimensions = data.Dimensions(x = 0, y = 0)):
        """ This class is initialized with the size of the grid and will compute
            the space of valid paths (indexed to grid coordinates) starting
            at some origin.
        """
        self.gridSize           = gridSize
        self.paths:list[Path]   = []

    def paths_find(self, origin:data.GridCoord, length:int) -> list[Path]:
        canAddPath:bool         = True
        path:Path               = Path(data.GridCoord(), data.Dimensions())
        for direction in GridDir:
            canAddPath          = True
            try:
                path            = Path(origin, self.gridSize)
                path.grow(direction, length-1) # length-1 since distances count from zero!
            except:
                canAddPath      = False
            if canAddPath:
                self.paths.append(path)
        return self.paths

