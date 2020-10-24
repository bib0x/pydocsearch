import pytest

from docsearch.docsearch import *

def test_docsearch_show_topic_without_search(cmd_opts, envpaths, capsys):
    tests = { 
        'one_cheat': "\n".join([
            "[one_cheat] description for the first cheat",
            "- first cheat",
            "- second cheat",
            "\n"
        ]),
        'one_link': "\n".join([
            "[one_link] description of the first link",
            "- https://linkone/",
            "- https://linktwo/",
            "\n"
        ]),
    }
    for topic, expected in tests.items():
        cmd_opts['topic'] = topic
        d = Docsearch(cmd_opts, envpaths)
        d.execute()
        captured = capsys.readouterr()
        assert captured.out == expected

def test_docsearch_empty_topic(cmd_opts, envpaths, capsys):
    cmd_opts['topic'] = 'empty_topic'
    d = Docsearch(cmd_opts, envpaths)
    d.execute()
    captured = capsys.readouterr()
    expected = 'No data received from YAML file.\n'
    assert captured.out == expected
