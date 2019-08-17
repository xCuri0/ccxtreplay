# ccxtreplay
save data like orderbooks of CCXT supported exchanges to be later used for backtesting, etc.

## usage
```
./save-rp [ccxt supported exchange name]
```
this will create a .replay file which will log all changes to orderbooks and tickers (trades will be added soon) until you stop it

you can replay it using the ccxtreplay library which uses the same method names as ccxt. ```example.py``` contains an example on how to use it.

this library should be considered alpha since ccxt doesn't support websockets at the current moment so it just polls the exchange until you stop it. which can trigger ddos protection on some exchanges. i will add support for websockets to this library as soon as ccxt starts officially supporting them since lfern's fork is inconsistent between exchanges