from cyberutils.bash import execute_bash, get_json_from_bash_query


def test_execute_bash():
    _res, _err = execute_bash(bash_command="echo {'name': 'test'}")
    assert _res == b"{'name': 'test'}\n"
    assert _err is None


def test_get_json_from_bash_query():
    assert get_json_from_bash_query(bash_command="echo {'name': 'test'}") == {'name': 'test'}
