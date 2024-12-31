from pre_commit_hooks.runner import run_sbt_command
from colorama import init as colorama_init, Fore
from typing import Optional

import sys

TASK_SCALAFMT = 'scalafmt'
TASK_SCALACHA = 'scalafmtCheck'
MISSING_PLUGIN_CHECK_STRING = 'Not a valid key: scalafmtCheck'
MISSING_PLUGIN_ERROR_MSG: str = f'{Fore.RED}ERROR: scalafmt SBT plugin not present! See {Fore.BLUE}https://scalameta.org/scalafmt/docs/installation.html#sbt{Fore.RED} for installation instructions.'


def main(argv: Optional[list[str]] = None) -> int:
    colorama_init()

    # Get file arguments passed from pre-commit
    files_arg: list[str] = argv or sys.argv[1:]

    # Only process files with .scala or .sbt extensions
    scala_files: list[str] = [file for file in files_arg if file.endswith(('.scala', '.sbt'))]

    if not scala_files:
        print(f"{Fore.YELLOW}No Scala or SBT files to format.")
        return 0
    
    files_cmd_input: str = " ".join(scala_files)

    check_exit_code: int = run_sbt_command(f'; {TASK_SCALACHA} --files {files_cmd_input}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    format_exit_code: int = run_sbt_command(f'; {TASK_SCALAFMT} --files {files_cmd_input}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    return check_exit_code + format_exit_code

if __name__ == '__main__':
    exit(main())
