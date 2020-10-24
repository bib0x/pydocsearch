import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def env_setup_and_teardown():
    testdata_root = os.path.dirname(os.path.realpath(__file__))
    docsearch_path = os.path.join(testdata_root, 'testdata')

    docsearch_env = {
        'DOCSEARCH_PATH': docsearch_path,
        'DOCSEARCH_COLORED': '0',
        'DOCSEARCH_MCOLORED': '0',
    }

    # Setup
    old_env = dict(os.environ)
    os.environ.update(docsearch_env)

    yield

    # Teardown
    os.environ.clear()
    os.environ.update(old_env)

@pytest.fixture(scope="session")
def envpaths():
    envpaths = os.getenv("DOCSEARCH_PATH")
    return envpaths.split(":") 

@pytest.fixture(scope="function")
def cmd_opts():
    return {
        'cheats': True,
        'colored': False,
        'env': False,
        'glossary': True,
        'inventory': False,
        'json': False,
        'links': True,
        'matched': False,
        'pwd': False,
        'search': "",
        'topic': ""
    }
