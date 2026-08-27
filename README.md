# csvwash

Small pandas pipeline that cleans messy CSV exports

## Features

- Drops duplicates, trims strings, normalizes dates
- Writes a cleaning report next to the output
- Config-driven column renames and type casts
- Chunked reading for files that do not fit in memory

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pipeline.py raw.csv --config config.yaml --out clean.csv
```

## Project structure

```text
├── docs/
│   ├── configuration.md
│   ├── development.md
│   └── usage.md
├── examples/
│   └── quickstart.md
├── tests/
│   └── test_smoke.py
├── .editorconfig
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── SECURITY.md
├── config.yaml
├── pipeline.py
└── requirements.txt
```

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

## Notes

- mostly stable, edge cases remain

## License

MIT. Do whatever you want.
