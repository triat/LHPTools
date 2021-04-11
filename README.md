# LHPTools

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md) 

LHPTools is a set of scripts used to help you manage the [LickHunter](http://www.lickhunter.com) bot. Every scripts contains an internal documentation that explain the main purpose of the script and how to use it.

## Requirements installation

### Python Requirements

LHPTools is implemented in Python 3. This requires a working Python installation to run. It officially supports Python 3.6+.

### Install Python

Install Python for your system:

On MacOS X:

```
$ brew install python3
```

On Debian/Ubuntu:

```
$ sudo apt-get install python3 python3-venv
```

On Windows:

[Download the latest binary installer](https://www.python.org/downloads/windows/) from the Python website.

### Create a virtual environment (optional)

Dependencies can be installed for your system via its package management but, more likely, you will want to install them yourself in a local virtual environment.

```bash
$ python3 -m venv ~/.venvs/lhptools
```

Make sure to always activate your virtual environment before using it:

```bash
$ source  ~/.venvs/lhptools/bin/activate
```

You may want to use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) to make this process much nicer.

## LHPTools installation and upgrade

Before you go any further, make sure you're installed all the requirements detailed in the (#requirements-installation).

### Clone the repo

The easiest way for now to get the LHPTools scripts and keep it up to date is to clone the repository on your system using [git](https://git-scm.com/)

```bash
$ git clone https://github.com/triat/LHPTools.git
```

From here, you can update the scripts using

```bash
$ git pull
```

### Download a copy

While cloning the repo helps you to keep everything up-to-date with a single command, you can also have more control on the version of the script you want to run by downloading the zip directly from the [releases](https://github.com/triat/LHPTools/releases)

## Usage

All the scripts you find in this repo contains a helper that you can display with `-h | --help` parameter. It describes what it does and how you can use it. 

```bash
$ python3 update_coins.py --help

usage: update_coins.py [-h] [--config-file CONFIG_FILE] [--debug]

Update liquidations values for the LHPControl GUI

optional arguments:
  -h, --help                    show this help message and exit
  --config-file CONFIG_FILE     Path to LHPC config file (usually called `varPairs.json`)
  --debug                       Give additional debug output
```

## Contributing

Contributors to this project are welcome as this is an open-source effort that seeks discussions and continuous improvement.

From a code perspective, if you wish to contribute, you will need to run a Python 3.6+ environment. Then, fork this repository and submit a PR. The project cares for code readability and checks the code style to match best practices defined in PEP8.

## Contact

Discord: Biwaa#7257
