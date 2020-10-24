import os
import pytest

from docsearch.docsearch import *

def test_docsearch_gather_inventory(cmd_opts, envpaths):
    d = Docsearch(cmd_opts, envpaths)
    gathered = d.gather_inventory()
    expected = []
    for p in d.paths:
        for f in os.listdir(p):
            expected.append(f)
    assert len(gathered) > 0
    assert len(expected) > 0
    assert sorted(expected) == gathered

def test_docsearch_show_inventory(cmd_opts, envpaths, capsys):
    cmd_opts['inventory'] = True
    d = Docsearch(cmd_opts, envpaths)
    d.execute()
    captured = capsys.readouterr()
    expected = []
    for p in d.paths:
        for f in os.listdir(p):
            expected.append(f[:-len(d.topic_ext)])
    expected = "\n".join(sorted(expected)) + "\n"
    assert len(expected) > 0
    assert captured.out == expected
