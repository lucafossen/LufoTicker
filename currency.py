import cryptocompare
import datetime

class Pair:
    def __init__(self, base, quote):
        self.base = base
        self.quote = quote
    
    def get_price(self):
        return str(cryptocompare.get_price(self.base,currency=self.quote)[self.base][self.quote])
    
    def get_quote(self):
        return self.base
    
    #For getting the price of the base with the quote name following it
    def get_qprice(self):
        return str(cryptocompare.get_price(self.base,currency=self.quote)[self.base][self.quote]) + " " + self.quote
    
    def get_historical_price(self, timeframe):
        
        
        if timeframe == "1hr":
            ls = cryptocompare.get_historical_price_minute(self.base, self.quote, 60, exchange='Kraken', toTs=datetime.datetime.now())
        elif timeframe == "1d":
            ls = cryptocompare.get_historical_price_minute(self.base, self.quote, 1440, exchange='Kraken', toTs=datetime.datetime.now())
        elif timeframe == "1w":
            ls = cryptocompare.get_historical_price_hour(self.base, self.quote, 168, exchange='Kraken', toTs=datetime.datetime.now())
        elif timeframe == "1mo":
            ls = cryptocompare.get_historical_price_day(self.base, self.quote, 30, exchange='Kraken', toTs=datetime.datetime.now())
        elif timeframe == "3mo":
            ls = cryptocompare.get_historical_price_day(self.base, self.quote, 90, exchange='Kraken', toTs=datetime.datetime.now())
        elif timeframe == "1y":
            ls = cryptocompare.get_historical_price_day(self.base, self.quote, 365, exchange='Kraken', toTs=datetime.datetime.now())
        elif timeframe == "3y":
            ls = cryptocompare.get_historical_price_day(self.base, self.quote, 1095, exchange='Kraken', toTs=datetime.datetime.now())
        
        returnlist = []
        
        counter = 0
        
        for i in ls:
            returnlist.append((ls[counter]["time"], ls[counter]["close"]))
            counter += 1
        return(returnlist)
