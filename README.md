# PYDOCSEARCH

## Goal

Same project as https://github.com/bib0x/docsearch but in Python.
It has been useful for experimenting with:
- Poetry
- Pyenv
- Pytest (output capture)

## Setup

### From git

```
$ cd HOME/perso/git/
$ git clone <repository>
$ cd pydocsearch
$ poetry install
```

### Configuration

```
$ cat ~/.bash_aliases
# ---------------------------
# DOCSEARCH
# ---------------------------
export DOCSEARCH_PATH="$HOME/perso/git/resources:$HOME/work/git/resources"
export DOCSEARCH_ROOT="$HOME/perso/git/pydocsearch"
export DOCSEARCH_COLORED=1

if [ -d "$DOCSEARCH_ROOT" ]; then
    alias docsearch="$DOCSEARCH_ROOT/docsearch/docsearch.py"

    # autocompletion
    if [ -f "$DOCSEARCH_ROOT/docsearch-completion.bash" ]; then
        . "$DOCSEARCH_ROOT/docsearch-completion.bash"
    fi
fi
```

## Usage

### Command line help

```
docsearch --help
usage: docsearch [-h] [-C] [-G] [-L] [-c] [-e] [-i] [-j] [-m] [-p] [-s SEARCH]
                 [-t TOPIC]

optional arguments:
  -h, --help            show this help message and exit
  -C, --cheats          Restrict search on cheats matches
  -G, --glossary        Restrict search on glossary matches
  -L, --links           Restrict search on glossary matches
  -c, --colored         Enable colored output
  -e, --env             Show used DOCSEARCH_* environment variables
  -i, --inventory       List all topics
  -j, --json            JSON output
  -m, --matched         Colorize matched terms
  -p, --pwd             Show topics fullpath on matched terms
  -s SEARCH, --search SEARCH
                        Keyword or term to search
  -t TOPIC, --topic TOPIC
                        Search on a specific topic
```

### Examples

Same as https://github.com/bib0x/docsearch#examples

## Development

### Tests

```
$ poetry run pytest
===================================== test session starts =====================================
platform linux -- Python 3.7.3, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/user/perso/git
collected 8 items                                                                             

tests/test_docsearch_env.py ..                                                          [ 25%]
tests/test_docsearch_inventory.py ..                                                    [ 50%]
tests/test_docsearch_topic.py ..                                                        [ 75%]
tests/test_docsearch_topic_path.py ..                                                   [100%]

====================================== 8 passed in 0.05s ======================================
```

## License

`pydocsearch` is available under the [Beerware](http://en.wikipedia.org/wiki/Beerware) license.
If we meet some day, and you think this stuff is worth it, you can buy me a beer in return.
