from pre_commit_hooks.runner import run_sbt_command
from colorama import init as colorama_init, Fore
from typing import Optional

import subprocess

TASK_SCALAFMT = 'scalafmt'
TASK_SCALACHA = 'scalafmt --check'
MISSING_PLUGIN_CHECK_STRING = 'Not a valid key: scalafmtCheck'
MISSING_PLUGIN_ERROR_MSG: str = f'{Fore.RED}ERROR: scalafmt SBT plugin not present! See {Fore.BLUE}https://scalameta.org/scalafmt/docs/installation.html#sbt{Fore.RED} for installation instructions.'


def main(argv: Optional[list[str]] = None) -> int:
    colorama_init()

    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Extract branch name from output: refs/remotes/origin/main -> main
        main_branch_name: str = result.stdout.strip().split("/")[-1]
    except subprocess.CalledProcessError as e:
        raise LookupError(f"Error determining main branch: {e}") # Default to 'main' if detection fails

    check_exit_code: int = run_sbt_command(f'; {TASK_SCALACHA} --diff-ref={main_branch_name}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    format_exit_code: int = run_sbt_command(f'; {TASK_SCALAFMT} --diff-ref={main_branch_name}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    return check_exit_code + format_exit_code

if __name__ == '__main__':
    exit(main())
