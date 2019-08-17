#!/usr/bin/python3
import ccxtreplay

dupe = []
for r in ccxtreplay.Replay(open('./COBINHOOD.replay').read()):
    ob = r.fetch_order_book('ETH/USDT')
    # dont print same duplicates
    if ob in dupe:
        continue
    else:
        dupe.append(ob)
        print(ob)