# Family Tree Command Line Tool

Create and manipulate a family tree

# Setup

```console

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env$ git clone git@github.com:vinayteki95/family-tree-cli.git
.......

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env$ ls
family-tree-cli

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env$ cd family-tree-cli/

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ python3 -m venv venv

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ ls
commandline_test.sh  familytree  README.md  requirements.txt  src  tests  venv

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ source venv/bin/activate

fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ sudo apt install graphviz

(venv) fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ pip install -r requirements.txt 

(venv) fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ ./familytree 
Usage: familytree [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  add
  clear
  connect
  count

(venv) fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ python -m pytest -v
================================================================ test session starts =================================================================
platform linux -- Python 3.8.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- /home/fr33b1rd/Projects/marketpulse_tech/doc_env/family-tree-cli/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/fr33b1rd/Projects/marketpulse_tech/doc_env/family-tree-cli
collected 4 items                                                                                                                                    

tests/test_familytree.py::test_add_relationship PASSED                                                                                         [ 25%]
tests/test_familytree.py::test_add_person PASSED                                                                                               [ 50%]
tests/test_familytree.py::test_connect_people PASSED                                                                                           [ 75%]
tests/test_familytree.py::test_count_relation PASSED                                                                                           [100%]

================================================================= 4 passed in 0.56s ==================================================================

(venv) fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ ./commandline_test.sh 
/home/fr33b1rd/.familytree/cache.png
/home/fr33b1rd/.familytree/cache.json
/home/fr33b1rd/.familytree/cache.graphml

(venv) fr33b1rd@eye:~/Projects/marketpulse_tech/doc_env/family-tree-cli$ shotwell ~/.familytree/cache.png

```

# Tests

# Usage and Design Choices

# Limitations

# Scope
