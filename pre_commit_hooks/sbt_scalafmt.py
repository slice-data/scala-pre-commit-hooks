from pre_commit_hooks.runner import run_sbt_command
from colorama import init as colorama_init, Fore

TASK_SCALAFMT = 'scalafmtAll'
TASK_SCALACHA = 'scalafmtCheckAll'
MISSING_PLUGIN_CHECK_STRING = 'Not a valid key: scalafmtCheck'
MISSING_PLUGIN_ERROR_MSG = f'{Fore.RED}ERROR: scalafmt SBT plugin not present! See {Fore.BLUE}https://scalameta.org/scalafmt/docs/installation.html#sbt{Fore.RED} for installation instructions.'


def main(argv=None):
    colorama_init()

    check_cmd = run_sbt_command(f'; {TASK_SCALACHA}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    format_cmd = run_sbt_command(f'; {TASK_SCALAFMT}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    return format_cmd + check_cmd

if __name__ == '__main__':
    exit(main())
