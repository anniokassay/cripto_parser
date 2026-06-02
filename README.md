# cripto_parser
Demonstration project of DWH architecture
# Bybi_parser отключен из-за прогрем с интеграцией API
## Secure database config

Parsers read database settings from environment variables:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

For systemd deployment, store secrets in `/etc/py_bots/parser.env` and restrict permissions.

## Диаграма потока данных:
flowchart LR
  subgraph ingest
    B[Binance API]
    Y[Bybit API]
    K[KuCoin API]
    G[Gate + Playwright]
  end
  subgraph dwh
    R[raw_data.*]
    L[load_info / errors]
    S[staged_data MV]
    REP[report.v_tg_data]
  end
  TG[Telegram bot]
  B & Y & K & G --> R
  R --> L
  R --> S
  S --> REP --> TG
