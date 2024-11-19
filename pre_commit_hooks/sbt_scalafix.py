from pre_commit_hooks.runner import run_sbt_command
from colorama import init as colorama_init, Fore

TASK_SCALAFIX = 'scalafixAll' # this one changes the files
TASK_SCALAFIX_CHECK = 'scalafixAll --check'
MISSING_PLUGIN_CHECK_STRING = 'Not a valid key: scalafix'
MISSING_PLUGIN_ERROR_MSG = f'{Fore.RED}ERROR: Scalafix SBT plugin not present! See {Fore.BLUE}https://scalacenter.github.io/scalafix/docs/users/installation.html{Fore.RED} for installation instructions.'
SCALAC_OPTIONS = 'set scalacOptions ++= Seq("-Ywarn-unused-import")'
SCALAFIX_ENABLE = 'scalafixEnable'

def main(argv=None):
    colorama_init()
    enable_exit_code = run_sbt_command(f'; clean ; {SCALAC_OPTIONS} ; {SCALAFIX_ENABLE}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    check_exit_code = run_sbt_command(f'; {TASK_SCALAFIX_CHECK}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    format_exit_code = run_sbt_command(f'; {TASK_SCALAFIX}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    return enable_exit_code + check_exit_code + format_exit_code

if __name__ == '__main__':
    exit(main())
