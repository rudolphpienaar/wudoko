#!/usr/bin/env python3
#
# (c) 2024 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  sys, os, re


from    wudoko.__init__         import __version__

from    argparse                import RawTextHelpFormatter
from    argparse                import ArgumentParser
import  pudb

from    pfmisc._colors          import Colors
from    pfmisc                  import other

from    wudoko.wudoko           import Wudoko, parser_setup, parser_interpret
from    wudoko.lib.path         import Path
from    wudoko.lib.grid         import Grid
from    wudoko.lib.trajectory   import Trajectory
from    wudoko.models.data      import GridDir, GridCoord, Dimensions

CY      = Colors.CYAN
YL      = Colors.YELLOW
NC      = Colors.NO_COLOUR
GR      = Colors.GREEN
PL      = Colors.PURPLE
RD      = Colors.RED

str_desc = Colors.CYAN + f"""{CY}

██╗    ██╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗ ██████╗
██║    ██║██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██╔═══██╗
██║ █╗ ██║██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
██║███╗██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
╚███╔███╔╝╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝

{NC}
                                make word grids

                             -- version {YL}{__version__}{NC} --

    {GR}wudoko{NC} makes word grids guaranteed to contain a set of seed words
    and optionally discard illegal words.
""" + Colors.NO_COLOUR

package_CLIself = f'''
         {CY}--gridSize {PL}<Rows>x<Cols>{NC}           \\
         {CY}--wordInclude {PL}<wordList>{NC}           \\
        [{CY}--wordExclude {PL}<wordList>{NC}]          \\
        [{CY}--version{NC}]                         \\
        [{CY}--man{NC}]                             \\
        [{CY}--synopsis{NC}]                        \\
'''

package_argSynopsisSelf = f'''
        {CY} --gridSize {PL}<Rows>x<Cols>{NC}
        The size of the board in rows, cols. This is a string and MUST have an 'x'
        separating the <rows> from <cols>, for example "10x7".

        {CY}--wordInclude {PL}<wordList>{NC}
        The file containing the list of words to include.

        [{CY}--wordExclude {PL}<wordList>{NC}]
        The file containing the list of words to exclude.


        [{CY}--logPrefix {PL}<prefix>{NC}]
        If specified, prepend log snapshots with <prefix>.

        [{CY}--version{NC}]
        If specified, print the version and exit.

        [{CY}--man{NC}]
        If specified, print a detail man page and exit.

        [{CY}--synopsis{NC}]
        If specified, print only an overview synposis and exit.

'''

package_CLItagHelp          = """
"""

package_CLIfull             = package_CLIself
package_CLIDS               = package_CLIself
package_argsSynopsisFull    = package_argSynopsisSelf
package_argsSynopsisDS      = package_argSynopsisSelf

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis = f"""
    {YL}NAME{NC}

        {GR}wudoko{NC}

    {YL}SYNOPSIS

        {GR}wudoko{NC} """ + package_CLIfull + f"""

    {YL}BRIEF EXAMPLE

        {GR}wudoko      {CY}--gridSize {YL}10x7{NC}             \\
                    {CY}--wordInclude {YL}include.txt{NC}   \\
                    {CY}--wordExclude {YL}exclude.txt{NC}

    """

    description =  f'''
    {YL}DESCRIPTION

        {GR}wudoko{NC} will solve for all word grids that include all words
        in {CY}--wordInclude{NC} and optionally not contain any words from
        {CY}--wordExclude{NC}.


    {YL}ARGS{NC}
    ''' +  package_argsSynopsisFull     +\
                package_CLItagHelp + f'''
    {YL}EXAMPLES{NC}

    {GR}wudoko {CY}--gridSize {YL}10x5 {CY}--wordInclude {YL}mustHave.txt {CY}--wordExclude {YL}notHave.txt{NC}


    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description


def earlyExit_check(args) -> int:
    """Perform some preliminary checks
    """
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        return 1
    if args.version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        return 2
    return 0

def path_test() -> None:
    gridSize:Dimensions                 = Dimensions(x = 10, y = 10)
    initialPosition:GridCoord           = GridCoord(x = 5, y = 5)

    path:Path   = Path(initialPosition, gridSize)
    try:
        path.grow(GridDir.E, 4)
        path.grow(GridDir.N, 3)
        path.grow(GridDir.SE, 4)
    except Exception as e:
        print(str(e))

def trajectory_test() -> None:
    trajectory:Trajectory   = Trajectory(Dimensions(x=10, y=10))
    trajectory.paths_find(GridCoord(x = 1, y = 1), 3)


def format_alphanum(input:str) -> str:
    return re.sub(r'(\w)', rf'{YL}\1{NC}', input)

def gridWord_banner() -> None:
    word:str                = "wudoko"
    grid:Grid               = Grid(Dimensions(x = 13, y = 13), "-")
    trajectory:Trajectory   = Trajectory(grid.gridSize)
    origin:GridCoord        = GridCoord(x=6, y=6)

    for path in trajectory.paths_find(origin, len(word)):
        if grid.word_canInsert(word, path):
            grid.word_insert(word, path)
    sgrid:str   = format_alphanum('%s' % grid)
    print(f'{sgrid}')

def main(argv:list[str]=[]) -> int:
    add_help:bool           = False
    parserSA:ArgumentParser = parser_setup(
                                    'A command line python helper',
                                    add_help
                                )
    args, extra              = parser_interpret(parserSA, argv)

    if (exit:=earlyExit_check(args)): return exit

    # pudb.set_trace()
    # path_test()
    # trajectory_test()
    gridWord_banner()

    args.version            = __version__
    args.desc               = synopsis(True)

    wudoko                  = Wudoko(args)
    wudoko.solve()

    return 0

if __name__ == "__main__":
    sys.exit(main())
