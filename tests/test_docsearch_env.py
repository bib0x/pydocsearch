import pytest

from docsearch.docsearch import *

def test_docsearch_env_enabled_mode(cmd_opts, envpaths):
    d = Docsearch(cmd_opts, envpaths)
    expected = 'disabled'
    assert d.colored_mode == expected
    assert d.mcolored_mode == expected

def test_docsearch_show_env(cmd_opts, envpaths, capsys):
    cmd_opts['env'] = True
    d = Docsearch(cmd_opts, envpaths)
    d.execute()

    captured = capsys.readouterr()
    assert len(captured.out) > 0

    expected = ['DOCSEARCH_MCOLORED', 'DOCSEARCH_COLORED', 'DOCSEARCH_PATH', 'color mode disabled']
    for exp in expected:
        assert exp in captured.out
