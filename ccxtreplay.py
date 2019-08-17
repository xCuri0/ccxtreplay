import json

class Replay:
    def __init__(self, rpfile):
        self.__rplines = rpfile.splitlines()
        self.__orderbooks = {}
        self.__tickers = {}
        self.__current = 0

        self.markets = {}
        self.symbols = []
        self.currencies = []
        self.timestamp = 0

    def __iter__(self):
        return self

    def __setdata(self, data):
        if data[2] == 'OB':
            self.__orderbooks[data[1]] = json.loads(data[3])
        elif data[2] == 'TI':
            self.__tickers[data[1]] = json.loads(data[3])
        elif data[2] == 'MRKT':
            self.markets[data[1]] = json.loads(data[3])
            self.symbols.append(data[1])
        elif data[2] == 'COIN':
            self.currencies[data[1]] = json.loads(data[3])   
        elif data[2] == 'TR':
            print('HOW')

    def __next__(self):
        if self.__current > len(self.__rplines) - 2:
            raise StopIteration
        else:
            sp = self.__rplines[self.__current].split(" ", 3)
            if sp[0] == 'BASEDATA':
                for sp2 in self.__rplines[self.__current:]:
                    self.__current += 1
                    sp2s = sp2.split(" ", 3)
                    self.__setdata(sp2s)
                    if not sp2s[0] == 'BASEDATA':
                        self.timestamp = sp2s[0]
                        break
            else:
                self.__setdata(sp)
                self.timestamp = sp[0]

        self.__current += 1
        return self

    def load_markets(self):
        pass

    def fetch_markets(self):
        return self.markets

    def fetch_currencies(self):
        return self.currencies

    def fetch_ticker(self, symbol):
        if symbol in self.__tickers:
            return self.__tickers[symbol]
        return None

    def fetch_tickers(self):
        res = []
        for ticker in self.__tickers.items():
            res.append(ticker)
        return res

    def fetch_order_book(self, symbol):
        if symbol in self.__orderbooks:
            return self.__orderbooks[symbol]
        return None

    def fetch_ohlcv(self, symbol):
        raise NotImplementedError('y u need dis ?')

    def fetch_trades(self, symbol):
        raise NotImplementedError('Adding support for trades requires websocket support in CCXT')

    def fetch_status(self):
        raise NotImplementedError('uwu')
