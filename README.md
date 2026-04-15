# osint-entity-mapper

Simple OSINT entity mapper that collects domain intelligence from WHOIS, DNS, crt.sh, Shodan, GitHub, and writes relationships to Neo4j.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure credentials in `config.py`.

## Usage

```bash
python main.py <domain>
```

Example:

```bash
python main.py example.com
```

## Notes

- `config.py` currently stores API credentials and Neo4j connection details.
- Keep this file private and do not commit secrets to git.
- Generated reports are saved as `report_<domain>_<timestamp>.md`.
