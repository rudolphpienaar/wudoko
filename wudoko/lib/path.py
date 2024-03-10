"""
The path class is used to construct paths through a grid
"""

from __future__             import annotations

from    wudoko.models.data  import GridCoord, Dimensions, GridDir, Orient

def invalid_direction(direction:GridDir) -> str:
    return f"""
      Invalid direction {direction.name}
        Must be one of
            'N'
         'NW' 'NE'
       'W'       'E'
         'SW' 'SE'
            'S'
    """


class Path:
    def __init__(self, initialPosition:GridCoord, gridSize:Dimensions):
        self.gridSize   = gridSize
        self.path:list[GridCoord]   = [initialPosition]

    def __str__(self, orientation:Orient = Orient.row) -> str:
        """ A string representation that prints the path coordinates
            either in a single line row, or a multiline column
        """
        match(orientation):
            case Orient.row: ret = '[' + ' '.join(map(str, self.path)) + ']'
            case Orient.col: ret = '[' + '\n'.join(map(str, self.path)) + ']'
        return ret

    def dv_get(self, direction:GridDir) -> GridCoord:
        """
        Determine the "delta vector" for a given <direction>. This is simply
        the change in 'x' and 'y' grid directions.
        """
        dxy:GridCoord   = GridCoord(x=0, y=0)

        match(direction):
            case GridDir.N:   dxy = GridCoord(x =  0, y = -1)
            case GridDir.S:   dxy = GridCoord(x =  0, y =  1)
            case GridDir.E:   dxy = GridCoord(x =  1, y =  0)
            case GridDir.W:   dxy = GridCoord(x = -1, y =  0)
            case GridDir.NE:  dxy = GridCoord(x =  1, y = -1)
            case GridDir.NW:  dxy = GridCoord(x = -1, y = -1)
            case GridDir.SE:  dxy = GridCoord(x =  1, y =  1)
            case GridDir.SW:  dxy = GridCoord(x = -1, y =  1)
            case _:
                raise ValueError(invalid_direction(direction))
        return dxy

    def grow(self, direction:GridDir, distance:int) -> list[GridCoord]:
        """
        Grow the path in the specified direction by the given dstance.
        Returns the set of grid coordinates along the path.
        Raises an exception if the path extends outside the grid.
        """
        try:
            dxy:GridCoord  = self.dv_get(direction)
        except Exception as e:
            raise e
        new_positions:list[GridCoord]  = []

        # Get the position of the terminal coordinate in the existing path
        # This is the -1 index...
        if len(self.path):
            pathEndCoord        = self.path[-1]
        else:
            raise ValueError("Cannot grow from an empty path")

        for _ in range(distance):
            pathEndCoord = pathEndCoord + dxy

            if not (0 <= pathEndCoord.x < self.gridSize.x and
                    0 <= pathEndCoord.y < self.gridSize.y):
                raise ValueError(f"""
                Path extends outside the grid in {direction} direction
                Violation at grid space: {pathEndCoord.x}, {pathEndCoord.y}
                Current path: {self.__str__(Orient.row)}
                """)

            new_positions.append(pathEndCoord)

        self.path.extend(new_positions)
        return new_positions

