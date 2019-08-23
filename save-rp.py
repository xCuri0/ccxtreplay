#!/usr/bin/python3
import sys
import asyncio
import time
import json
import ccxt.async_support as ccxt

exchange = getattr(ccxt, sys.argv[1])({})
out = open(f'{exchange.name}.replay', 'a')

prevob = {}
prevti = {}

async def main():
    await exchange.load_markets()

    for s in exchange.symbols:
        out.write(f"BASEDATA {s} MRKT {json.dumps(exchange.markets[s])}\n")
        try:
            book = await exchange.fetch_order_book(s)
            for k in list(book.keys()):
                if not k == 'asks' and not k == 'bids':
                    del book[k]
            prevob[s] = book
            out.write(f"BASEDATA {s} OB {json.dumps(book)}\n")
        except ccxt.ExchangeError:
            print('failed to fetch ob for ' + s)
        ticker = await exchange.fetch_ticker(s)
        prevti[s] = book
        out.write(f"BASEDATA {s} TI {json.dumps(ticker)}\n")

    for c in exchange.currencies:
        out.write(f"BASEDATA {s} COIN {json.dumps(exchange.currencies[c])}\n")

    while (True):
        for m in exchange.markets:
            try:
                book = await exchange.fetch_order_book(m)
                timestamp = 0
                datetime = book['datetime']
                nonce = book['nonce']

                if book['timestamp']:
                    timestamp = book['timestamp']
                else:
                    timestamp = int(time.time()) * 1000

                del book['timestamp']
                del book['datetime']
                del book['nonce']
                if not book == prevob[m]:
                    prevob[m] = book
                    book['timestamp'] = timestamp
                    book['datetime'] = datetime
                    book['nonce'] = nonce
                    out.write(f"{timestamp} {m} OB {json.dumps(book)}\n")

                ticker = await exchange.fetch_ticker(m)
                datetime = ticker['datetime']
                if ticker['timestamp']:
                    timestamp = ticker['timestamp']
                else:
                    timestamp = int(time.time()) * 1000

                del ticker['timestamp']
                del ticker['datetime']

                if not ticker == prevti[m]:
                    prevti[m] = ticker
                    ticker['timestamp'] = timestamp
                    ticker['datetime'] = datetime
                    out.write(f"{timestamp} {m} TI {json.dumps(ticker)}\n")
            except Exception:
                pass
    await exchange.close()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        out.close()
