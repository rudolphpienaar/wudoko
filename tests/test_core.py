import  os
import  shlex
import  shutil
from    _pytest.capture         import capsys
from    runj.__main__           import main
from    runj.runj               import RunJ, json_respresentation, dir_create
os.environ['XDG_CONFIG_HOME'] = '/tmp'
from    argparse                import Namespace
from    runj.models.data        import ShellRet, ScriptRet
from    pathlib                 import Path

def CLIcall_parseForStringAndRet(capsys, cli:str, contains:str, exitCode:int) -> None:
    """ helper for running main module simulating CLI call
    """
    ret:int     = main(shlex.split(cli))
    captured    = capsys.readouterr()
    assert contains in captured.out
    assert ret  == exitCode

def test_main_manCore(capsys) -> None:
    """ core man page
    """
    CLIcall_parseForStringAndRet(capsys, "--man", "--exec", 1)

def test_main_version(capsys) -> None:
    """ version CLI reporting
    """
    CLIcall_parseForStringAndRet(capsys, "--version", "Name", 2)

