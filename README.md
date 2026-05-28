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

```bash
sudo mkdir -p /etc/py_bots
sudo cp .env.example /etc/py_bots/parser.env
sudo chown root:root /etc/py_bots/parser.env
sudo chmod 600 /etc/py_bots/parser.env
```

After service updates:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ByBit_parser.service KuCoin_parser.service
sudo systemctl status ByBit_parser.service KuCoin_parser.service
```
