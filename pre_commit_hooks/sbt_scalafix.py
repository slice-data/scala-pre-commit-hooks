import sys
from pre_commit_hooks.runner import run_sbt_command
from colorama import init as colorama_init, Fore

TASK_SCALAFIX = 'scalafix --files' # this one changes the files
TASK_SCALAFIX_CHECK = 'scalafix --check --files'
MISSING_PLUGIN_CHECK_STRING = 'Not a valid key: scalafix'
MISSING_PLUGIN_ERROR_MSG = f'{Fore.RED}ERROR: Scalafix SBT plugin not present! See {Fore.BLUE}https://scalacenter.github.io/scalafix/docs/users/installation.html{Fore.RED} for installation instructions.'
SCALAC_OPTIONS = 'set scalacOptions ++= Seq("-Ywarn-unused-import")'
SCALAFIX_ENABLE = 'scalafixEnable'

def main(argv=None):

    argv = argv or sys.argv[1:]
    colorama_init()

    scala_files = [file for file in argv if file.endswith(".scala")]
    if not scala_files:
        print(f"{Fore.YELLOW}No Scala files to process.")
        return 0
    file_list = ' '.join(scala_files)
    check_exit_code = run_sbt_command(f'; clean ;  {SCALAC_OPTIONS} ; {SCALAFIX_ENABLE} ; {TASK_SCALAFIX_CHECK} {file_list}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    format_exit_code = run_sbt_command(f'; clean ;  {SCALAC_OPTIONS} ; {SCALAFIX_ENABLE} ; {TASK_SCALAFIX} {file_list}', MISSING_PLUGIN_CHECK_STRING, MISSING_PLUGIN_ERROR_MSG)
    return check_exit_code + format_exit_code

if __name__ == '__main__':
    exit(main())
