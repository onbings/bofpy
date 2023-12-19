import sys
import argparse
import os
from typing import Tuple

def Bof_Cli_Check(title:str, cli_parser:argparse.ArgumentParser):
    print(f"{title}")
    argc = len(sys.argv)
    print(f"{argc-1} command line arguments passed to '{sys.argv[0]}' (cwd '{os.getcwd()}')")

    for i in range(1, argc):
        print(sys.argv[i])
    if len(sys.argv) == 1:
        cli_parser.print_help(sys.stderr)
        #BofPy.exit_app("Incomplete argument", 3)
    try:
        args = cli_parser.parse_args()
    except SystemExit as e:
        if str(e) == '2':
            # Handle the exit due to a command-line parsing error
            print("There was an error in the command-line arguments.")
            cli_parser.print_help(sys.stderr)
            args = None
    return args

