from subprocess import Popen, PIPE
import json
from typing import Optional
from sys import stdout
from time import sleep


def display_sleep(delay_time: int) -> None:
    """
    Sleep delay time and display time left in console
    :param delay_time: delay time in seconds
    :return: None
    """
    for _remaining in range(delay_time, -1, -1):
        stdout.write("\r")
        stdout.write("{:2d} from {:2d} seconds remaining.".format(_remaining, delay_time))
        stdout.flush()
        sleep(1)
    stdout.write("\n")


def execute_bash(bash_command: str, shell: bool = False,
                 timeout: Optional[int] = 20) -> tuple[Optional[str], Optional[str]]:
    """
    Execute a bash command
    :param bash_command: a bash command for execution
    :param shell: shell or regular execution approach
    :param timeout: execution timeout
    :return: execution result and error
    """
    if len(bash_command.split('"')) == 1:
        _bash_command_list = bash_command.split()
    elif len(bash_command.split('"')) == 2:
        _bash_command_list = \
            bash_command.split('"')[0].split() + \
            [bash_command.split('"')[1]]
    elif len(bash_command.split('"')) > 2:
        _bash_command_list = \
            bash_command.split('"')[0].split() + \
            [bash_command.split('"')[1]] + \
            [item for items in bash_command.split('"')[2:] for item in items.split()]
    else:
        return None, f'Cannot split bash command {bash_command}'
    _popen_process = Popen([bash_command], stdout=PIPE, shell=shell, text=True) \
        if shell else Popen(_bash_command_list, stdout=PIPE)
    return _popen_process.communicate(timeout=timeout)


def get_json_from_bash_query(bash_command: str, shell: bool = False,
                             timeout: Optional[int] = 20) -> Optional[dict]:
    """
    Execute a bash command and convert a result to json format
    :param bash_command: bash command for execution
    :param shell: shell or regular execution approach
    :param timeout: execution timeout
    :return: execution result in json format
    """
    _res, _ = execute_bash(bash_command, shell=shell, timeout=timeout)
    if _res:
        return json.loads(_res.decode('utf8').replace("'", '"'))
    return
