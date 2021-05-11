import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import os.path
from os import path
import coin

#https://www.coingecko.com/en/api
cg = CoinGeckoAPI()


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

#This does all available updates
def updateCoin(coin):
    pass

def updatePrice(coin):
    return cg.get_coin_by_id(coin.name)

def updateHistory(coin):
    pass

def pingServer():
    pass

def getTickers():
    pass

def writeCSV():
        if(not path.exists( os.getcwd() + "/savedat/coinList.csv")):
            with open( os.getcwd() + "/savedat/coinList.csv", 'w') as fp: 
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
