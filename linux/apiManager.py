import time
import coin
import math
import schedule
from decimal import Decimal, ROUND_CEILING
from pycoingecko import CoinGeckoAPI
import pandas as pd
import os.path
from os import path

class ApiManager:
    def __init__(self, coinList = [], freeCalls = 10, historyCalls  = 10, updateCalls = 80):
        self.coinList = coinList
        self.historyCalls = historyCalls
        self.historyCount = 0
        self.updateCalls = updateCalls
        self.updateCount = 0
        self.runManager = False
        self.cg = CoinGeckoAPI()

    def manager(self):
        schedule.every(self.round_decimals_up(float(self.getHistoryCalls()/60), 1)).seconds.do(self.historyCall)
        schedule.every(self.round_decimals_up(float(self.getUpdateCalls()/60),  1)).seconds.do(self.updateCall)
        while self.runManager:
           schedule.run_pending()
           time.sleep(1)

    def setCoinList(self, x):
        self.coinList = x

    def setFreeCalls(self, x):
        self.freeCalls = x
    
    def setHistoryCalls(self, x):
        self.historyCalls = x
    
    def setUpdateCalls(self, x):
        self.updateCalls = x

    def getHistoryCalls(self):
        return self.historyCall

    def getUpdateCalls(self):
        return self.updateCall

    def startManager(self):
        self.runManager = True

    def stopManager(self):
        self.runManager = False

    def round_decimals_up(self, number:float, decimals:int=2):
        """
        Returns a value rounded up to a specific number of decimal places.
        """
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.ceil(number)

        factor = 10 ** decimals
        return math.ceil(number * factor) / factor

    def updateCall(self):
        newPrice = self.cg.get_coin_by_id(self.coinList[self.updateCount].getName().lower())['market_data']['current_price'].get("usd")
        coin = self.coinList[self.updateCount]
        coin.setCurrentPrice(newPrice)
        self.updateCount = ((self.updateCount + 1) % (len(self.coinList)))

    def historyCall(self):
        #Do API call to self.coinList[self.updateCount]
        print("FUNC2", self.coinList[self.historyCount]) 
        self.historyCount = ((self.historyCount + 1) % (len(self.historyList)))


    def requestPrice(self, name):
        newPrice = self.cg.get_coin_by_id(name.lower())['market_data']['current_price'].get("usd")
        self.writeToLog(newPrice)
        return newPrice


    def requestHistory(self, name):
        pass

    def writeToLog(self, st):
        file_object = open('metatron.log', 'a')
        file_object.write(str(st) + "\n")
        file_object.close()


def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

def writeCSV():
        #print(os.getcwd())
        #linux/savedat/coinList.csv
        
        cg = CoinGeckoAPI()
        if(not path.exists( os.getcwd() + "/savedat/coinList.csv")):
            with open( os.getcwd() + "/savedat/coinList.csv", 'w+') as fp: 
                pass
        avail = cg.get_coins_list()
        i = []
        s = []
        n = []
        r = []

        for x in avail:
            i.append(x['id'])
            s.append(x['symbol'])
            n.append(x['name'].lower())
            r.append(x['name'])
        coins = pd.concat([pd.Series(n), pd.Series(s), pd.Series(i), pd.Series(r)], keys=["Name", "Symbol", "ID", "RealName"], axis=1)
        run = True
        coins.to_csv(os.getcwd() + "/savedat/coinList.csv", index=False)

def coinAdd():
    coins = getCoins()
    while(True):
        #print(wallet)
        try:
            i = input("Coin to Add: ")
        except:
            i = input("Coin to Add: ")
        try:
            if(i == "q"):
                run = False
            elif(i == 'c'):
                wallet = []
            elif(i.lower() in coins["Name"].values):
                dex = getIndexes(coins, i)
                dex = int(dex[0][0])
                print(dex)
                wallet.append(coins.iloc[dex]['Symbol'])
            elif(coins[coins['Symbol'].str.lower().contains(i)]):
                wallet.append(i)
                pass
            elif(coins[coins['ID'].str.contains(i)]):
                dex = getIndexes(coins, i)
                dex = int(dex[0][0])
                print(dex)
                wallet.append(coins.iloc[dex]['Symbol'])
            else:
                pass
        except:
            pass
        
def getCoins():
    try:
        writeCSV()
    except:
        writeCSV()
    coins = pd.read_csv( os.getcwd() + "/savedat/coinList.csv")
    return coins