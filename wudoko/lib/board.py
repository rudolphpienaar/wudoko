""" A class to house boards, i.e. solution grids
"""

from    wudoko.lib.grid         import Grid
from    wudoko.lib.path         import Path
from    wudoko.lib.trajectory   import Trajectory
from    wudoko.models.data      import GridCoord
import  pudb


class WordIterate:
    """ A simple class/functor to iterate over a list
    """

    def __init__(self, words:list[str]):
        self.words:list[str]    = words
        self.index:int          = 0

    def __call__(self) -> str:
        if self.index >= len(self.words):
            return ''
        word:str    = self.words[self.index]
        self.index += 1
        return word

    def copy(self) -> 'WordIterate':
        iterateCopy:'WordIterate'   = WordIterate(self.words)
        iterateCopy.index           = self.index
        return iterateCopy

    def __str__(self) -> str:
        return f"{self.index}:{self.words}"

class Solution:

    def __init__(self):
        self.boards:list[Grid]          = []
        self.illegalWords:list[str]     = []
        self.legalWords:list[str]       = []
        self.memo:dict                  = {}
        self.usememoization:bool        = False
        self.stateCount:int             = 0
        self.stateCountShow:bool        = True

    def addToSolution(self, grid:Grid) -> None:
        self.boards.append(grid)

    def terminate(self, grid:Grid):
        if grid.is_full():
            for word in self.illegalWords:
                if grid.contains_word(word):
                    return
            self.addToSolution(grid)
            print(f"Valid solution found! Adding solution #{len(self.boards)}...")

    def state_incr(self):
        self.stateCount += 1
        if self.stateCountShow:
            print(f"Board state: {self.stateCount}      \r", end='')

    def add_word(self, grid:Grid, nextWordIterator:WordIterate) -> Grid:
        self.state_incr()
        if self.usememoization:
            state = (grid.strRep(), str(nextWordIterator))
            if state in self.memo:
                print("found state!")
                return self.memo[state]

        word:str    = nextWordIterator()
        if not len(word):
            self.terminate(grid)
            return grid
        cell:GridCoord  = GridCoord(x=0, y=0)
        for cell in grid.cellIterate():
            trajectory:Trajectory   = Trajectory(grid.gridSize)
            trajectories:list[Path] = trajectory.paths_find(cell, len(word))
            for path in trajectories:
                newGrid:Grid        = grid.copy()
                if newGrid.word_canInsert(word, path):
                    newGrid.word_insert(word, path)
                    newWordIterator:WordIterate = nextWordIterator.copy()
                    nextGrid:Grid               = self.add_word(newGrid, newWordIterator)
                    if self.usememoization:
                        nextState               = (nextGrid.strRep(), str(newWordIterator))
                        self.memo[nextState]    =  nextState
        self.terminate(grid)
        return grid

    def removeSolution(self, indices:list) -> list[Grid]:
        return [grid for idx, grid in enumerate(self.boards) if idx not in indices]

    def pruneFromSolution(self, illegalWords:list[str]) -> list[Grid]:
        # pudb.set_trace()
        illegalBoards:list[Grid]        = []
        illegalIndices:list[int]        = []
        for word in illegalWords:
            boardIndex:int  = 0
            for grid in self.boards:
                if grid.contains_word(word):
                    if boardIndex not in illegalIndices:
                        illegalIndices.append(boardIndex)
                        illegalBoards.append(grid)
                boardIndex  += 1
        if len(illegalIndices):
            self.boards = self.removeSolution(illegalIndices)
        return illegalBoards
