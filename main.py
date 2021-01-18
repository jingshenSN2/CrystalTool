import sys
from crystalsearch.run import run_task_in_config


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_task_in_config('')
    elif sys.argv[1].startswith('-'):
        run_task_in_config(sys.argv[1:])
