INSERT INTO dict.change_type
  (id, codename, currency_out, currency_gain)
VALUES
  (1, 'RUB/USDT_p2p', 'RUB', 'USDT'),
  (2, 'USDT_p2p/RUB', 'USDT', 'RUB'),
  (3, 'USDT_p2p/VND', 'USDT', 'VND'),
  (4, 'VND/USDT_p2p', 'VND', 'USDT'),
  (5, 'USDT_p2p/CNY', 'USDT', 'CNY');

  GRANT SELECT ON TABLE dict.change_type TO tgbot_analitic;