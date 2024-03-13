str_description = """
    This module provides some very simple shell-based job running
    methods.
"""


import  pudb
import  sys
from    pflog                       import pflog
from    pudb.remote                 import set_trace
from    pathlib                     import Path
from    datetime                    import datetime
from    argparse                    import Namespace, ArgumentParser, RawTextHelpFormatter
from    wudoko.models.data          import Dimensions, Space
from    multiprocessing             import Process, Manager
from    multiprocessing.managers    import DictProxy
from    typing                      import Any
from    wudoko.lib.board            import Solution, WordIterate
from    wudoko.lib.grid             import Grid

def parser_setup(desc:str, add_help:bool = True) -> ArgumentParser:
    parserSelf = ArgumentParser(
                description         = desc,
                formatter_class     = RawTextHelpFormatter,
                add_help            = add_help
            )

    parserSelf.add_argument("--gridSize",
                help    = "rows x col",
                dest    = 'gridSize',
                default = '')

    parserSelf.add_argument("--wordInclude",
                help    = "Words to fit into the board",
                dest    = 'wordInclude',
                default = '')

    parserSelf.add_argument("--wordExclude",
                help    = "words that must NOT appear in the board",
                dest    = 'wordExclude',
                default = '')

    parserSelf.add_argument("--version",
                help    = "if specified, print name and version",
                dest    = 'version',
                default = False,
                action  = 'store_true')

    parserSelf.add_argument("--man",
                help    = "if specified, print detailed man page",
                dest    = 'man',
                default = False,
                action  = 'store_true')

    parserSelf.add_argument("--synopsis",
                help    = "if specified, print help synopsis",
                dest    = 'synopsis',
                default = False,
                action  = 'store_true')

    return parserSelf

def parser_interpret(parser, args = None) -> tuple:
    """
    Interpret the list space of *args, or sys.argv[1:] if
    *args is empty
    """
    if args:
        args, unknown    = parser.parse_known_args(args)
    else:
        args, unknown    = parser.parse_known_args(sys.argv[1:])
    return args, unknown

def parser_JSONinterpret(parser, d_JSONargs) -> tuple:
    """
    Interpret a JSON dictionary in lieu of CLI.

    For each <key>:<value> in the d_JSONargs, append to
    list two strings ["--<key>", "<value>"] and then
    argparse.
    """
    l_args  = []
    for k, v in d_JSONargs.items():
        if type(v) == type(True):
            if v: l_args.append('--%s' % k)
            continue
        l_args.append('--%s' % k)
        l_args.append('%s' % v)
    return parser_interpret(parser, l_args)

def namespace_isempty(namespace: Namespace) -> bool:
    return all(value is None for value in vars(namespace).values())

def wordFile_read(filename:str) -> list[str]:
    try:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
        return lines
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except IOError:
        print(f"Error occurred while reading the file: {filename}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return []

def emptyStrings_remove(lst:list[str]) -> list[str]:
    return [s for s in lst if s]

class Wudoko:

    def __init__(self, options:Namespace = Namespace()):

        if namespace_isempty(options):
            options, extra          = parser_interpret(
                                        parser_setup(
                                            'A word grid board creator',
                                            True
                                        )
                                    )
        # pudb.set_trace()
        self.options:Space          = Space(**vars(options))
        self.desc                   = "" if not self.options.has('desc') else self.options.desc
        if self.options.has('desc'):
            self.options.rm('desc')
        if not self.options.has('verbosity'):
            self.options.verbosity  = 0
        self.gridSize               = self.gridDimensions_set()
        self.words:list[str]        = []
        self.wordsExclude:list[str] = []
        self.words_populate()
        self.solution               = Solution()
        self.solution.legalWords    = self.words
        if len(self.wordsExclude):
            self.solution.illegalWords  = self.wordsExclude

    def gridDimensions_set(self) -> Dimensions:
       rows, cols = self.options.gridSize.split('x')
       return Dimensions(x=cols, y=rows)

    def words_populate(self):
        self.words                  = emptyStrings_remove(
                                            wordFile_read(self.options.wordInclude)
                                        )
        # sort word list from longest to shortest
        self.words                  = sorted(self.words, key = len, reverse = True)
        self.wordsExclude:list[str] = []
        if len(self.options.wordExclude):
            self.wordsExclude       = emptyStrings_remove(
                                            wordFile_read(self.options.wordExclude)
                                        )


    def boards_headerPrint(self, numberOfBoards:int, qualifier:str = "solution"):
        print(f'{numberOfBoards} {qualifier}', end="")
        if numberOfBoards:
            if numberOfBoards > 1:
                print("s")
            else:
                print("")
        else:
            print("s")

    def boards_print(self, boards:list[Grid]):
        for board in boards:
            print("Board:")
            print(board)

    @pflog.tel_logTime(
            event   = 'Solve for all solutions'
    )
    def solve_allBoards(self):
        print("Solving wudoko!")
        print(f"Legal words:   {self.words}")
        print(f"Illegal words: {self.wordsExclude}")
        initialGrid:Grid            = Grid(self.gridSize, " ")
        wordIterator:WordIterate    = WordIterate(self.words)
        self.solution.add_word(initialGrid, wordIterator)
        print("\nAll boards:")
        self.boards_headerPrint(len(self.solution.boards))

    @pflog.tel_logTime(
            event   = 'Solve for illegal solutions'
    )
    def prune_illegalBoards(self):
        if len(self.wordsExclude):
            print(f"Removing all grids with illegal words: {self.wordsExclude}")
            illegalSolutions:list[Grid] = self.solution.pruneFromSolution(self.wordsExclude)
            if len(illegalSolutions):
                print("Disallowed Solutions:")
                self.boards_headerPrint(len(illegalSolutions), 'illegal')
                # self.boards_print(illegalSolutions)
                print("Legal Solutions:")

    def solve(self):
        self.solve_allBoards()
        # self.prune_illegalBoards()
        self.boards_print(self.solution.boards)
        print("done!")
