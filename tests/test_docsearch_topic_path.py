import os
import pytest

from docsearch.docsearch import *

def test_docsearch_show_empty_topic(cmd_opts, envpaths, capsys):
    cmd_opts['pwd'] = True

    d = Docsearch(cmd_opts, envpaths)
    d.execute()
    captured = capsys.readouterr()

    assert not captured.out

def test_docsearch_show_topic_path(cmd_opts, envpaths, capsys):
    topic_chosen = 'mixed_topic'

    cmd_opts['pwd'] = True
    cmd_opts['topic'] = topic_chosen

    d = Docsearch(cmd_opts, envpaths)
    d.execute()
    captured = capsys.readouterr()

    expected = []
    topic_name = f"{topic_chosen}.yaml"
    for p in d.paths:
        for f in os.listdir(p):
            if topic_name == f:
                expected.append(os.path.join(p, f))
    expected = "\n".join(expected) + "\n"

    assert len(expected) > 0
    assert len(captured.out) > 0
    assert captured.out == expected
