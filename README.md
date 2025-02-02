# Cron Expression Parser

A simple command-line tool to parse and expand cron expressions.

## Installation

Ensure Python 3.6+ and pip3 are installed.

## Usage

Run the parser with a cron string as the argument:

```bash
cd cron-parser
pip3 install -r requirements.txt

python3 parser/cron_parser.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```

## Test Cases
```bash
python3 -m pytest test_cron.py
```