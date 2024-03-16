""" A class to house boards, i.e. solution grids
"""

from    wudoko.lib.grid         import Grid
from    wudoko.lib.path         import Path
from    wudoko.lib.trajectory   import Trajectory
from    wudoko.models.data      import GridCoord
import  string
import  pudb


class WordIterate:
    """ A simple class/functor to iterate over a list
    """

    def __init__(self, words:list[str]):
        self.words:list[str]    = words
        self.index:int          = 0

    def __call__(self, offset:int = 0) -> str:
        if offset: self.index += offset
        if self.index <=0: self.index = 0
        if self.index >= len(self.words):
            return ''
        word:str    = self.words[self.index]
        self.index += 1
        return word

    def wordAfter(self, word:str) -> str:
        if not word:
            return self.words[0]
        next_words = [self.words[i+1] for i, w in enumerate(self.words) if w == word and i < len(self.words) - 1]
        return next_words[0] if next_words else ''

    def copy(self) -> 'WordIterate':
        iterateCopy:'WordIterate'   = WordIterate(self.words)
        iterateCopy.index           = self.index
        return iterateCopy

    def wordsRotate(self) -> None:
        self.words.append(self.words.pop(0))

    def __str__(self) -> str:
        return f"{self.index}:{self.words}"

class Solution:

    def __init__(self, legalWords:list[str], illegalWords:list[str] = []):
        self.boards:list[Grid]          = []
        self.illegalWords:list[str]     = illegalWords
        self.legalWords:list[str]       = legalWords
        self.pathMustHaveSpaces:bool    = False
        self.stateCount:int             = 0
        self.stateCountShow:bool        = True
        self.terminateInfo:str          = ""
        self.wordIterator:WordIterate   = WordIterate(legalWords)

    def addToSolution(self, grid:Grid) -> None:
        self.boards.append(grid)

    def fillAnyBlanks(self, templateGrid:Grid):
        for ch in list(string.ascii_lowercase):
            chGrid:Grid                 = templateGrid.copy()
            for cellCoord in chGrid.cellIterate():
                if chGrid.empty(cellCoord):
                    chGrid.set(cellCoord, ch)
            self.boards.append(chGrid)

    def terminate(self, grid:Grid):
        for word in self.illegalWords:
            if grid.contains_word(word):
                return
        found:bool = True
        # for word in self.legalWords:
        #     found = found and grid.contains_word(word)
        if found:
            self.addToSolution(grid)
            print(f"Board state: {self.stateCount:04} \t{self.terminateInfo} #{len(self.boards)}...")

    def state_incr(self):
        self.stateCount += 1
        if self.stateCountShow:
            print(f"Board state: {self.stateCount:04}      \r", end='')

    # def add_word(self, grid:Grid, nextWordIterator:WordIterate) -> Grid:
    #     self.state_incr()
    #
    #     word:str    = nextWordIterator()
    #     if not len(word) or grid.is_full():
    #         self.terminate(grid)
    #         return grid
    #     cell:GridCoord  = GridCoord(x=0, y=0)
    #     for cell in grid.cellIterate():
    #         if not grid.cell_canStart(cell, word):
    #             continue
#         trajectory:Trajectory   = Trajectory(grid.gridSize)
    #         trajectories:list[Path] = trajectory.paths_find(cell, len(word))
    #         for path in trajectories:
    #             if grid.word_canInsert(word, path):
    #                 newGrid:Grid        = grid.copy()
    #                 newGrid.word_insert(word, path)
    #                 newWordIterator:WordIterate = nextWordIterator.copy()
    #                 nextGrid:Grid               = self.add_word(newGrid, newWordIterator)
    #     return grid

    def add_word(self, grid:Grid, word:str) -> Grid:
        self.state_incr()

        if not len(word) or grid.is_full():
            self.terminate(grid)
            return grid
        cell:GridCoord  = GridCoord(x=0, y=0)
        for cell in grid.cellIterate():
            # if not grid.cell_canStart(cell, word):
            #     continue
            trajectory:Trajectory   = Trajectory(grid.gridSize)
            trajectories:list[Path] = trajectory.paths_find(cell, len(word))
            for path in trajectories:
                if grid.word_canInsert(word, path):
                    if self.pathMustHaveSpaces:
                        if not grid.word_alongPathHasSpaces(path):
                            continue
                    newGrid:Grid        = grid.copy()
                    newGrid.word_insert(word, path)
                    newWord:str         = self.wordIterator.wordAfter(word)
                    # nextGrid:Grid               = self.add_word(newGrid, newWordIterator)
                    nextGrid:Grid               = self.add_word(newGrid, newWord)
        return grid

    def hasGrid(self, grid:Grid) -> bool:
        for board in self.boards:
            if board.is_equal(grid):
                return True
        return False

    def duplicatesRemove(self) -> list[Grid]:
        seen_grids:set      = set()
        result:list[Grid]   = []
        for grid in self.boards:
            grid_tuple      = tuple(grid.grid.flatten())
            if grid_tuple not in seen_grids:
                seen_grids.add(grid_tuple)
                result.append(grid)
        return result

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

    def pruneMissingFromSolution(self, legalWords:list[str]) -> list[Grid]:
        # pudb.set_trace()
        illegalBoards:list[Grid]        = []
        illegalIndices:list[int]        = []
        for word in legalWords:
            boardIndex:int  = 0
            for grid in self.boards:
                if not grid.contains_word(word):
                    if boardIndex not in illegalIndices:
                        illegalIndices.append(boardIndex)
                        illegalBoards.append(grid)
                boardIndex  += 1
        if len(illegalIndices):
            self.boards = self.removeSolution(illegalIndices)
        return illegalBoards
