import apiManager

#Make this smart in regards to symbol or name
class Coin:
    def __init__(self, name, sym, amt = 0):
        self.name = name
        self.amountHeld = float(amt) 
        self.currentPrice = 0
        self.totalValue = 0
        self.symbol = sym
        self.history = "addMe"


    def getName(self):
        return self.name

    def dictGen(self):
        pass

    def returnDict(self):
        return {'name': self.name,
                'symbol': self.symbol,
                'amountHeld': self.amountHeld,
                'currentPrice': self.currentPrice,
                'totalValue': self.totalValue
                }

    #Update values in coin
    def update(self):
        pass

    def initializeCoin(self, name):
        x = apiManager.ApiManager()
        price = x.requestPrice(name.lower())
        self.setCurrentPrice(price)

    def writeToLog(self, st):
        file_object = open('metatron.log', 'a')
        file_object.write(str(st) + "\n")
        file_object.close()

    def setCurrentPrice(self, num):
        self.currentPrice = num
        self.totalValue = self.amountHeld * self.currentPrice

    def setAmountHeld(self, amt):
        self.amountHeld = float(amt)
        self.totalValue = self.amountHeld * self.currentPrice

    def creationTest(self):
        self.writeToLog(self.returnDict())
     
    