# wudoko 

_Simple word board solver_

[![Version](https://img.shields.io/docker/v/rudolphpienaar/wudoko?sort=semver)](https://hub.docker.com/r/rudolphpienaar/wudoko)
[![MIT License](https://img.shields.io/github/license/rudolphpienaar/wudoko)](https://github.com/FNNDSC/runj/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/runj/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/runj/actions/workflows/ci.yml)

```

██╗    ██╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗ ██████╗
██║    ██║██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██╔═══██╗
██║ █╗ ██║██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
██║███╗██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
╚███╔███╔╝╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝

                - - - - - - - - - - - - -
                - o - - - - o - - - - o -
                - - k - - - k - - - k - -
                - - - o - - o - - o - - -
                - - - - d - d - d - - - -
                - - - - - u u u - - - - -
                - o k o d u w u d o k o -
                - - - - - u u u - - - - -
                - - - - d - d - d - - - -
                - - - o - - o - - o - - -
                - - k - - - k - - - k - -
                - o - - - - o - - - - o -
                - - - - - - - - - - - - -

```

## Abstract

A recursive word board solver.

## Installation

### Using ``PyPI``

The best method of installing `wudoko` and all of its dependencies is by fetching it from PyPI

```bash
pip3 install wudoko 
```

### From source repo

Alternatively, you can just `pip3 install -U ./` from the root directory of the source repo.

## Usage

A good set of exemplars is provided in the [`test_core.py`](https://github.com/FNNDSC/wudoko/blob/master/tests/test_core.py) test code.

### script

For a given grid size, and a list of included/excluded words in separate files:

```bash
wudoko --gridSize 4x4 --wordInclude wordsInclude.txt --wordExclude wordsExclude.txt
```

## CLI Synopsis

```html

        --gridSize <Rows>x<Cols>
        The size of the board in rows, cols. This is a string and MUST have an 'x'
        separating the <rows> from <cols>, for example "10x7".

        --wordInclude <wordList>
        The file containing the list of words to include.

        [--wordExclude <wordList>]
        The file containing the list of words to exclude.

        [--version]
        If specified, print the version and exit.

        [--man]
        If specified, print a detail man page and exit.

        [--synopsis]
        If specified, print only an overview synposis and exit.

```

## Examples

_Watch this space!_

_-30-_
