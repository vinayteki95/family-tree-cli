# Family Tree Command Line Tool

Create and manipulate a family tree

Typical usage patterns:

Check the file `commandline_test.sh`

```console

horus@eye:~/family-tree-cli$ ./familytree clear # removes pre-existing persistent files for current testing

horus@eye:~/family-tree-cli$ ./familytree add relationship son nextgen # add a relationship called son of type nextgen

horus@eye:~/family-tree-cli$ ./familytree add relationship wife partner # add a relationship called son of type partner

horus@eye:~/family-tree-cli$ ./familytree add person kid2 # add a person called kid2

horus@eye:~/family-tree-cli$ ./familytree connect kid2 --relation son --of rick # kid2 is son of rick

horus@eye:~/family-tree-cli$ ./familytree count rick --relation son # no of immediate sons of rick

horus@eye:~/family-tree-cli$ ./familytree count rick --relation son --all # no of sons (at all levels of heirarchy) of rick

```

## Setup

May be one can write an ansible playbook to take care of this setup but that would probably be an overkill

### Clone the repository

```console

horus@eye:~/family-tree-cli$ git clone git@github.com:vinayteki95/family-tree-cli.git
.......

```

### Create a virtual environment and verify that venv folder is created

```console

horus@eye:~/family-tree-cli$ ls
family-tree-cli

horus@eye:~/family-tree-cli$ cd family-tree-cli/

horus@eye:~/family-tree-cli/family-tree-cli$ python3 -m venv venv

horus@eye:~/family-tree-cli/family-tree-cli$ ls
commandline_test.sh  familytree  README.md  requirements.txt  src  tests  venv
```

### It is recommended to install "graphviz" dependency which is required to generate graphs (family tree)

Also activate the virtual enviroment before installing python dependencies

```console
horus@eye:~/family-tree-cli/family-tree-cli$ sudo apt install graphviz

horus@eye:~/family-tree-cli/family-tree-cli$ source venv/bin/activate

(venv) horus@eye:~/family-tree-cli/family-tree-cli$ pip install -r requirements.txt
```

### Verify that the command works - It should provide with a basic help

```console

(venv) horus@eye:~/family-tree-cli/family-tree-cli$ ./familytree
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

```

## Tests

I included the example provided in the assessment as a test so essentially the provided example is verified
Tests are included in the folder tests: `tests/test_familytree.py`

### Run unit tests

```console

(venv) horus@eye:~/family-tree-cli/family-tree-cli$ python -m pytest -v
================================================================ test session starts =================================================================
platform linux -- Python 3.8.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1 -- /home/horus/family-tree-cli/family-tree-cli/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/horus/family-tree-cli/family-tree-cli
collected 4 items

tests/test_familytree.py::test_add_relationship PASSED                                                                                         [ 25%]
tests/test_familytree.py::test_add_person PASSED                                                                                               [ 50%]
tests/test_familytree.py::test_connect_people PASSED                                                                                           [ 75%]
tests/test_familytree.py::test_count_relation PASSED                                                                                           [100%]

================================================================= 4 passed in 0.56s ==================================================================
```

### There is a command line test script as well. You can verify a sample image generated in your default home directory

`~/.familytree/` -> we'll be maintaining a few files here for persistence. I wanted to see if this application can be built on the most basic principles (**files**) without the necessity of a **daemon api** or a **database** for persistence.

```console

(venv) horus@eye:~/family-tree-cli/family-tree-cli$ ./commandline_test.sh
/home/horus/.familytree/cache.png
/home/horus/.familytree/cache.json
/home/horus/.familytree/cache.graphml

(venv) horus@eye:~/family-tree-cli/family-tree-cli$ shotwell ~/.familytree/cache.png

```

## Usage and Design Choices

The command line interface provides with the list of options necessary to run a command (use the `--help` option)

```console
(venv) horus@eye:~/Projects/marketpulse_tech/family-tree-cli$ ./familytree add relationship --help
Usage: familytree add relationship [OPTIONS] RELATION RELATION_TYPE:[prevgen|nextgen|samegen|partner]

Arguments:
  RELATION                        [required]
  RELATION_TYPE:[prevgen|nextgen|samegen|partner]
                                  [required]

Options:
  --help  Show this message and exit.

```

### Design choice for "relationship" entity.

If you look at the above help, it requires two arguments

1. RELATION -> a simple string ("mother", "father", etc)
2. RELATION_TYPE -> an enum from the choices (prevgen|nextgen|samegen|partner)
   prevgen -> one step above in family tree hierarchy (mother, father)
   nextgen -> one step below in family tree hierarchy (son, daughter)
   samegen -> same level in family tree hierarchy (brother, sister)
   partner -> same level in family tree but common children (wife / step wife / husband / step husband)

### Interesting features which emerge out of this property

#### Currently implemented

```python
    ft.connect_people("john shakespeare", "mary arden", "wife")
    ft.connect_people("john shakespeare", "joan", "daughter")
    ft.connect_people("john shakespeare", "margaret", "daughter")
    ft.connect_people("john shakespeare", "joan2", "daughter")
    ft.connect_people("mary arden", "anne", "daughter")
    ft.connect_people("mary arden", "gilbert", "son")
    ft.connect_people("mary arden", "richard", "son")
    ft.connect_people("mary arden", "edmund", "son")
    ft.connect_people("mary arden", "william", "son")
    ft.connect_people("william", "anne hathaway", "wife")
    ft.connect_people("william", "hamnet", "son")
    ft.connect_people("william", "susanna", "daughter")
    ft.connect_people("william", "judith", "daughter")
    ft.connect_people("john hall", "susanna", "wife")
    ft.connect_people("thomas quiney", "judith", "wife")
    ft.connect_people("susanna", "elizabeth", "daughter")
    ft.connect_people("judith", "shakespeare", "son")
    ft.connect_people("judith", "richard2", "son")
    ft.connect_people("judith", "thomas", "son")
```

If you look at the connections, we did not have to provide multiple connections between (mother, father, daughter, son) to properly infer the count of all sons and grandsons.

This can be expanded by explicitly writing familytree functions to traverse based on the type of relation. Currently it is implemented to handle cases for the assessment but there is enough functional scalability.

#### Scope

One feature I was hoping to include was to manage mulitple graphs / familytrees. This will also improve the code structure and graph,config file management through the application

## Limitations

- The main limitation of this application is to stay in the enum range for relation_type. I can easily provide an option to add arbitary relation but without a concrete **type** of a relation which is essentially used to traverse / navigate through relations internally in a graph it'll be impossible to derive any useful outcome.
