# cripto_parser
Demonstration project of DWH architecture

## Secure database config

Parsers read database settings from environment variables:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

For systemd deployment, store secrets in `/etc/py_bots/parser.env` and restrict permissions: