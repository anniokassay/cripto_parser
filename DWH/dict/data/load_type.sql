INSERT INTO dict.load_type
  (id, codename, url_adress,source_name)
VALUES
  (1, 'ByBit_p2p', 'https://api2.bybit.com/fiat/otc/item/online','ByBit'),
  (2, 'KuCoin_p2p', 'https://www.kucoin.com/_api/otc/ad/list','KuCoin'),
  (3, 'Binance_p2p', 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search','Binance'),
  (4, 'gate_2p2', 'https://www.gate.com/api/web/v1/c2c/advertisements?sub_website_id=0','gate.com');
  