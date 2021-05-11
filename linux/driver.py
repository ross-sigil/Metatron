import urwid
import urwid.raw_display
import urwid.web_display
import time
import csv
import pandas as pd
import json
import os.path
import coin
import math
import apiManager
from scrollable import ScrollBar, Scrollable
from os import path
import smtplib 
import emoji
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




'''
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ███╗   ███╗███████╗████████╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║    ██╔████╔██║█████╗     ██║   ███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
 “Someone had awoken METATRON: the Voice of God." ― Ian Tregillis
'''



'''
 ██████╗ ██╗      ██████╗ ██████╗  █████╗ ██╗     ███████╗
██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔══██╗██║     ██╔════╝
██║  ███╗██║     ██║   ██║██████╔╝███████║██║     ███████╗
██║   ██║██║     ██║   ██║██╔══██╗██╔══██║██║     ╚════██║
╚██████╔╝███████╗╚██████╔╝██████╔╝██║  ██║███████╗███████║
 ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
'''
#CLEAN THIS SHIT UP
df = apiManager.getCoins()
df['Symbol'] = df["Symbol"].astype(str)
coins = df['RealName'].tolist()

coins.sort()
choices = ["Input Coins", "List Coins", "Portfolio", "Import Holdings", "Debug", "Run Test", "Settings", "Exit"]
saved = True
inputStatus = ""
portfolio = []

#Settings stuff
email = "Metatron@waifu.club"
pas = "AH7qUNS5"
gateway = '6189324037@mms.cricketwireless.net'
gateway2 = "2702825160@txt.att.net"
smtp = "mail.cock.li" 
port = 587

#This is for API Call Timer
#Need to validate that this adds up to 100

#JK Free calls are free. JUst dont be a dummy about how you use them



freeCalls = 10          # Calls not implemented, these will be taken up by user actions like adding a coin
                        # Free Calls do not need a timer

historyCalls = 10       # Calls to update the respective histories of a coin 
updateCalls = 80        # Calls to update Selected Coins.



'''
██████╗ ███████╗██████╗ ██╗   ██╗ ██████╗ 
██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝ 
██║  ██║█████╗  ██████╔╝██║   ██║██║  ███╗
██║  ██║██╔══╝  ██╔══██╗██║   ██║██║   ██║
██████╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝
╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝

writeToLog is cool and can help you debug stuff because there is no real "console output" here and VSCODE debug stuff for python sucks.
            This just writes to metatron.log and can be cleared at any time. metatron.log to be deleted at "release" or used for error catching!
'''
def writeToLog(st):
    file_object = open('metatron.log', 'a')
    file_object.write(str(st) + "\n")
    file_object.close()

def getUSDT():
    pass


#DEBUG MODE STUFF
coins = coins[0:100]
coins1 = coins[10:20]
coins2 = coins[20:30]

#This should be used to catch exceptions and can even be used in settings to notify about great trades or losses maybe!
#https://dev.to/mraza007/sending-sms-using-python-jkd
def alertToPhone(email, pas, gateway, smtp, port, message):
    server = smtplib.SMTP(smtp,port)
    server.starttls()
    server.login(email,pas)

    # Now we use the MIME module to structure our message.
    msg = MIMEMultipart()
    msg['From'] = "Metatron"
    msg['To'] = gateway
    msg['Test'] = "You can insert anything\n"

    msg.attach(MIMEText(message, 'plain'))

    sms = msg.as_string()

    server.sendmail(email,gateway,sms)
    server.quit()


'''
 █████╗ ██████╗ ██╗     ██████╗ █████╗ ██╗     ██╗     ███████╗    
██╔══██╗██╔══██╗██║    ██╔════╝██╔══██╗██║     ██║     ██╔════╝    
███████║██████╔╝██║    ██║     ███████║██║     ██║     ███████╗    
██╔══██║██╔═══╝ ██║    ██║     ██╔══██║██║     ██║     ╚════██║    
██║  ██║██║     ██║    ╚██████╗██║  ██║███████╗███████╗███████║    
╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   
'''

#try:
    #apiMan = apiManager(portfolio, freeCalls, historyCalls, updateCalls)
    #apiMan = 
#except:
#    pass


'''
 ██████╗██╗      █████╗ ███████╗███████╗███████╗███████╗
██╔════╝██║     ██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝
██║     ██║     ███████║███████╗███████╗█████╗  ███████╗
██║     ██║     ██╔══██║╚════██║╚════██║██╔══╝  ╚════██║
╚██████╗███████╗██║  ██║███████║███████║███████╗███████║
 ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝                       
'''
class InputCoinBox(urwid.ListBox):
    def keypress(self, size, key):
        if key == 'enter':
            self.getData()
            return
        elif key == 'tab':
            self.moveDown(1)
            return
        elif key == 'shift tab':
            self.moveUp(1)
            return
        elif key == 'f8':
            main.original_widget = menu()
            return
        urwid.ListBox.keypress(self, size, key)

    def clearText(self):
        for x in self.body:
            try:
                x.original_widget.set_edit_text("")
            except:
                pass

    def moveUp(self, n):
        self.set_focus((self.focus_position + n) % len(self.body))

    def moveDown(self, n):
        self.set_focus((self.focus_position - n) % len(self.body))


    def getData(self):
        uglything = []
        for x in self.body:
            try:
                uglything.append(x.original_widget.get_edit_text())
            except:
                pass
        try:
            if(validateToName(uglything[0]).lower() not in portfolioNameGenerator()):
                if uglything[1] == '':
                    uglything[1] = 0
                mintCoin(validateToName(uglything[0]), uglything[1])
        except:
            pass
        self.clearText()
        self.set_focus(1)
    
class InputSettingBox(urwid.ListBox):
    def keypress(self, size, key):
        if key == 'enter':
            self.getData()
            return
        elif key == 'tab':
            self.moveDown(1)
            return
        elif key == 'shift tab':
            self.moveUp(1)
            return
        elif key == 'f8':
            main.original_widget = menu()
            return
        urwid.ListBox.keypress(self, size, key)

    def moveUp(self, n):
        self.set_focus((self.focus_position + n) % len(self.body))

    def moveDown(self, n):
        self.set_focus((self.focus_position - n) % len(self.body))

    def getData(self):
        uglything = []
        for x in self.body:
            try:
                uglything.append(x.original_widget.get_edit_text())
            except:
                pass    
        dc = {
            'freeCalls': int(uglything[0]),
            'historyCalls': int(uglything[1]),
            'updateCalls': int(uglything[2])
            }
        saveSettingsJSON(dc)
        settingsSavedMenu()


class SavedSettingBox(urwid.ListBox):
    def keypress(self, size, key):
        if key == 'enter':
            main.original_widget = menu()
        elif key == 'f8':
            main.original_widget = menu()
            return
        urwid.ListBox.keypress(self, size, key)


class InputDebugBox(urwid.ListBox):
    def keypress(self, size, key):
        if key == 'enter':
            self.getData()
            return
        elif key == 'tab':
            self.moveDown(1)
            return
        elif key == 'shift tab':
            self.moveUp(1)
            return
        elif key == 'f8':
            main.original_widget = menu()
            return
        urwid.ListBox.keypress(self, size, key)

    def clearText(self):
        for x in self.body:
            try:
                x.original_widget.set_edit_text("")
            except:
                pass

    def moveUp(self, n):
        self.set_focus((self.focus_position + n) % len(self.body))

    def moveDown(self, n):
        self.set_focus((self.focus_position - n) % len(self.body))


    def getData(self):
        uglything = []
        for x in self.body:
            try:
                uglything.append(x.original_widget.get_edit_text())
            except:
                pass
        try:
            if(validateToName(uglything[0]).lower() not in portfolioNameGenerator()):
                if uglything[1] == '':
                    uglything[1] = 0
                mintCoin(validateToName(uglything[0]), uglything[1])
        except:
            pass
        self.clearText()
        self.set_focus(1)

class MenuListBox(urwid.ListBox):
    signals = ["click"]
    def keypress(self, size, key):
        #if key == 'enter':
        #    return
        if key == 'tab' or key == 'down':
            self.move(1)
        elif key == 'shift tab' or key == 'up':
            self.move(-1)
        elif key == 'f8':
            main.original_widget = menu()
            return
        urwid.ListBox.keypress(self, size, key)

    def validateMove(self):
        pass

    def move(self, n):
        self.set_focus((self.focus_position + n) % (len(self.body)))

    def zero(self):
        self.set_focus(0)

class CmdWidget(urwid.WidgetWrap):
    def __init__(self, name, command):
        self.name = name
        self.command = command
        urwid.WidgetWrap.__init__(self, urwid.AttrMap(urwid.Text(name), 'headerMagenta', 'reversed'))

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


#Cool hack, basically moves cursor out of view. We will have to define custom events for these buttons though possibly though it might work because it wraps the widget
class ButtonLabel(urwid.SelectableIcon):
    def __init__(self, text):
        """
        Here's the trick: 
        we move the cursor out to the right of the label/text, so it doesn't show
        """
        curs_pos = len(text) + 1 
        urwid.SelectableIcon.__init__(self, text, cursor_position=curs_pos)

class FixedButton(urwid.WidgetWrap):
    _selectable = True
    signals = ["click"]
    def __init__(self, label):
        self.label = ButtonLabel(label)
        # you could combine the ButtonLabel object with other widgets here
        display_widget = self.label 
        urwid.WidgetWrap.__init__(self, urwid.AttrMap(display_widget, None, 'lightBlueText'))

    def keypress(self, size, key):
        if key == "enter":
            urwid.emit_signal(self, 'click', self.label)

    def mouse_event(self, size, event, button, col, row, focus):
        #urwid.emit_signal(self, 'click', self.label)
        pass

    def set_label(self, new_label):
        # we can set the label at run time, if necessary
        self.label.set_text(str(new_label))


'''
███╗   ███╗███████╗███╗   ██╗██╗   ██╗███████╗
████╗ ████║██╔════╝████╗  ██║██║   ██║██╔════╝
██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║███████╗
██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║╚════██║
██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝███████║
╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
'''                                          

def inputCoinMenu():
    #Maybe wrap a padding around it
    head = generateStatusHeader("Input Coin Details")
    name = urwid.AttrMap(urwid.Edit(('redText', u"Coin Name: "), ""), "headerMagenta", "blackTextRedBox")
    held = urwid.AttrMap(urwid.Edit(('redText', u"Amount Held: "), ""), "headerMagenta", "blackTextRedBox")

    
    #EVERY ITEM HERE NEEDS A DIVIDER FOR THE TAB SETTINGS TO WORK, sorry its not generic
    #body = InputCoinBox(urwid.SimpleFocusListWalker([name, urwid.Divider(),held, urwid.Divider()]))
    
    body = InputCoinBox(urwid.SimpleFocusListWalker([name, held]))
    
    response = urwid.Frame(
        urwid.Padding(urwid.AttrMap(body, "headerMagenta"), left = 20, right = 20),
        header = head
        #footer = foot
    )

    out = generateSmallOverlay(response)
    main.original_widget = out
    

def listCoinMenu():
    items = []
    for i in coins:
        items.append(CmdWidget(i, 0))
    maxw = 40
    cols = urwid.Frame(Scrollable(urwid.GridFlow(items, maxw, 1, 0, 'center')))
    box = urwid.Frame(urwid.Filler(cols, 'top'))
    main.original_widget = cols

#This get additional details for Coin object creation
def listFormMenu():
    pass

#Portfolio should track amounts. Should store to a file too and be read at start.
#Catch empty portfolios
def portfolioMenu():
    footer_text = [
        ('title', 'DeleteMe')
    ]
    header = generateHeader("Coins In Portfolio")
    foot = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    body = [header, urwid.Divider()]
    for c in selectedCoins:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', menu)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    response = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    out = generateSmallOverlay(response)
    main.original_widget = out

def savePrompt():
    #Add Input Handling for this
    yn = ["Yes", "No"]
    
    body = [
        urwid.AttrMap(urwid.Text("SEE YOU SPACE COWBOY"), "headerMagenta"),
        urwid.Divider(),
        urwid.AttrMap(urwid.Text("Would you like to Save Changes before exiting?"), "headerMagenta"),
        urwid.Divider()
        ]

    for c in yn:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    response = urwid.ListBox(urwid.SimpleFocusListWalker(body))

    out = generateSmallOverlay(response)
    main.original_widget = out

def debugMenu():
    head = generateStatusHeader("Debug")
    debugOptions = ["Test Phone"]
    body = []

    for x in debugOptions:
        button = FixedButton(x)
        urwid.connect_signal(button, 'click', testAlert)
        #urwid.Padding(button, left=0, )
        body.append(urwid.AttrMap(button, None, 'reversed'))
        
    bodyList = urwid.Padding(MenuListBox(urwid.SimpleFocusListWalker(body)), left=2, right=70)
 
    #urwid.ListBox(urwid.SimpleFocusListWalker(body))
    #foot = urwid.AttrMap(urwid.Text(inputStatus), 'top')
    response = urwid.Frame(
        bodyList,
        header = head
        #footer = foot
    )

    out = generateSmallOverlay(response)
    main.original_widget = out

#https://www.webfx.com/tools/emoji-cheat-sheet/
#message_head = ":fire::fire::fire: FAT FUCKING SALE ALERT :fire::fire::fire:\n" 
#message_body = "Just made your ass $2050.00 by flipping 0.251 BTC from a buy in at $200\n"

def testAlert(x, message_body= "", message_head=""):
    message_head = ":fire::fire::fire: FAT FUCKING SALE ALERT :fire::fire::fire:\n" 
    message_body = "Just made your ass $2050.00 by flipping 0.251 BTC from a buy in at $200\n"
    message = message_head + message_body
    message = emoji.emojize(message)
    alertToPhone(email,pas,gateway,smtp,port,message)
    #alertToPhone(email,pas,gateway2,smtp,port,message)

def settingMenu():
    head = generateStatusHeader("Settings")
    fC = urwid.AttrMap(urwid.Edit(('redText', u"Free API Calls:    "), str(freeCalls)), "headerMagenta", "blackTextRedBox")
    hC = urwid.AttrMap(urwid.Edit(('redText', u"History API Calls: "), str(historyCalls)), "headerMagenta", "blackTextRedBox")
    uC = urwid.AttrMap(urwid.Edit(('redText', u"Update API Calls:  "), str(updateCalls)), "headerMagenta", "blackTextRedBox")

    #EVERY ITEM HERE NEEDS A DIVIDER FOR THE TAB SETTINGS TO WORK, sorry its not generic
    body = InputSettingBox(urwid.SimpleFocusListWalker([fC,hC,uC]))

    response = urwid.Frame(
        urwid.Padding(urwid.AttrMap(body, "headerMagenta"), left = 20, right = 50),
        header = head
        #footer = foot
    )

    out = generateSmallOverlay(response)
    main.original_widget = out

def settingsSavedMenu():
    ok = ["Ok"]
    head = generateSettingsMenu("Saved")

    body =[]

    for i in ok:
        button = FixedButton(i)
        body.append(urwid.AttrMap(button, None, 'reversed'))

    body = urwid.Padding(SavedSettingBox(urwid.SimpleFocusListWalker(body)), left = 20, right = 50)

    response = urwid.Frame(
        urwid.AttrMap(body, "headerMagenta"),
        header=head
        )
    out = generateSmallOverlay(response)
    main.original_widget = out

#rename to mainmenu
def menu(): 
    body =[]
    for c in choices:
        button = FixedButton(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        #urwid.Padding(button, left=0, )
        body.append(urwid.AttrMap(button, None, 'reversed'))
        
    bodyList = urwid.Padding(MenuListBox(urwid.SimpleFocusListWalker(body)), left=2, right=70)
 
    #urwid.ListBox(urwid.SimpleFocusListWalker(body))
    #foot = urwid.AttrMap(urwid.Text(inputStatus), 'top')
    response = urwid.Frame(
        bodyList,
        header = generateStatusHeader("Welcome To Metatron")
        #footer = foot
    )

    out = generateSmallOverlay(response)
    return out


#Might be able to get fancy formatting in the numbers where the dollar signs percentages and negatives or + is a static color and only the number changes  with a Column of text boxes

#These values should eventually get to be used on whatever exchange we choose
def statsPile():
    accountValue = 1240.125
    totalUSDT = 300.2362346
    dailyChange = 25.13672347
    weeklyChange = -14.347437

    topName = "ChainLink"
    topChange = 460.00
    topValue = 1000.00
    
    botName = "Ripple"
    botChange = -62.40
    botValue = 2.30

    coinsHeld = []
    prospectCoins = []

    col1 = urwid.Columns([
        urwid.Pile([
        urwid.AttrMap(urwid.Text("Top Coin:"), 'greenText'),
        urwid.AttrMap(urwid.Text("24HR Change:"), 'greenText'),
        urwid.AttrMap(urwid.Text("Value:"), 'greenText'),
        ])
    ])

    col2 = urwid.Columns([
        urwid.Pile([
        urwid.AttrMap(urwid.Text(topName), 'greenText'),
        urwid.AttrMap(urwid.Text(profitLossText(topChange) + "%"), profitLossColor(topChange)),
        urwid.AttrMap(urwid.Text(profitLossText(topValue)), 'greenText')
        ])
    ])

    col3 = urwid.Columns([
        urwid.Pile([
        urwid.AttrMap(urwid.Text("Account Value:"), 'headerMagenta'),
        urwid.AttrMap(urwid.Text("USDT Held:"), 'headerMagenta'),
        urwid.AttrMap(urwid.Text("24 HR Change:"), 'greenText'),
        urwid.AttrMap(urwid.Text("7 Day Change:"), 'greenText'),
        ])
    ])
    
    col4 = urwid.Columns([
        urwid.Pile([
        urwid.AttrMap(urwid.Text(profitLossText(accountValue)), profitLossColor(accountValue)),
        urwid.AttrMap(urwid.Text(str(roundDecimalsDown(totalUSDT))), 'headerMagenta'),
        urwid.AttrMap(urwid.Text(profitLossText(dailyChange) + "%"), profitLossColor(dailyChange)),
        urwid.AttrMap(urwid.Text(profitLossText(weeklyChange) + "%"), profitLossColor(weeklyChange))
        ])
    ])

    col5 = urwid.Columns([
        urwid.Pile([
        urwid.AttrMap(urwid.Text("Bottom Coin:"), 'greenText'),
        urwid.AttrMap(urwid.Text("24HR Change:"), 'greenText'),
        urwid.AttrMap(urwid.Text("Value:"), 'greenText'),
        ])
    ])

    col6 = urwid.Columns([urwid.Pile([
        urwid.AttrMap(urwid.Text(botName), 'greenText'),
        urwid.AttrMap(urwid.Text(profitLossText(botChange) + "%"), profitLossColor(botChange)),
        urwid.AttrMap(urwid.Text(profitLossText(botValue)), 'greenText')
      ])
    ])


    colFin = urwid.Columns([col1,col2,col3,col4,col5,col6], 1)
    colFin = urwid.Pile([urwid.Divider(), colFin, urwid.Divider()])


    lineBox = urwid.Padding(colFin, left=1, right=1)
    out = urwid.LineBox(lineBox, tlcorner='░', tline='░', lline='░', trcorner='░', blcorner='░', rline='░', bline='░', brcorner='░')

    return urwid.Pile(widget_list=[out])


'''
███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗
██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝
█████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  
██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  
██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗
╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝

These are all controls only to do with money calculations
'''






'''
███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗
████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝
██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
'''

def profitLossColor(num):

    if num > 0 :
        return 'greenText'
    elif num < 0:
        return 'redText'
    else:
        return 'yellowText'
    pass

def profitLossText(num):
    if num > 0 :
        return ("+" + str(roundDecimalsDown(num)))
    else:
        return(str(roundDecimalsDown(num)))

def menuRestore(button, item):
    main.original_widget = menu()

def mintCoin(name, amt = 0):
    sym = validateToSymbol(name)
    x = coin.Coin(name, sym, amt)
    x.initializeCoin(name)
    x.creationTest()
    portfolio.append(x)
    global saved
    saved = False

def roundDecimalsDown(number:float, decimals:int=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)
    factor = 10 ** decimals
    return math.floor(number * factor) / factor


#This is what will be called by outputter
def addTestCoin():
    pass

#This needs to handle adding coins without tripping the saved flag
def loadAddCoin(c):
    if validatePortfolioAdd(c):
        portfolio.append(coin.Coin(c['name'], c['amountHeld']))

def portfolioNameGenerator():
    new = []
    global portfolio
    for x in portfolio:
        new.append(x.name)
    return new

#Needs to update the values of the coin that can be changed and flag saved = False
def updateCoin():
    pass

def generateHeader(title, div1 = " ", div2 = " "):
    return urwid.Pile([
        urwid.Divider(),
        urwid.AttrMap(urwid.Text(title), "headerMagenta"),
        urwid.Divider(div1),
        urwid.Divider(div2)
    ])

def generateStatusHeader(title, div1 = " ", div2 = " "):
    colBox = urwid.Pile([
        urwid.Divider(),
        urwid.AttrMap(urwid.Text(title),
        "headerMagenta"),
        urwid.Divider(div1),
        statsPile(),
        urwid.Divider(div2),
        urwid.Divider()])
    return colBox

def generateSettingsMenu(title, div1 = " ", div2 = " "):
    colBox = urwid.Pile([
        urwid.Divider(),
        urwid.AttrMap(urwid.Text(title), "headerMagenta"),
        urwid.Divider(div1), statsPile(),urwid.Divider(div2),
        urwid.Divider(),
        urwid.AttrMap(urwid.Text("Settings Have Been Saved"), "headerMagenta"), 
        urwid.Divider()
        ])
    return colBox


def generateSmallOverlay(widget):
    return urwid.Overlay(urwid.Padding(widget, left = 5, right = 5), urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 87),
        valign='middle', height=('relative', 72),
        min_width=20, min_height=9)

def generateLargeOverlay(widget):
    return urwid.Overlay(urwid.Padding(widget, left = 5, right = 5), urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 87),
        valign='middle', height=('relative', 80),
        min_width=20, min_height=9)

def adder(c):
    global saved
    saved = False
    selectedCoins.append(c)

def addCoinFromListWidget(button, choice):
    if choice not in selectedCoins and choice in coins:
        adder(choice) 

#Refactor me can take out validateCoinInputAdd and start with false to short circuit and cut out an if probably
def addCoin(choice):
    if validateCoinInputAdd(choice):
        if choice in selectedCoins:
            st = ("Duplicate Coin:", choice)
            return st
        else:
            #Symbol to Name
            #
            #REWRITE
            #
            if choice.lower() in list(map(str.lower, df["Symbol"].tolist())):
                st = "Successfully Added:", df['RealName'].tolist()[list(map(str.lower, df["Symbol"].tolist())).index(choice.lower())]
                adder(df['RealName'].tolist()[list(map(str.lower, df["Symbol"].tolist())).index(choice.lower())])
                saved = False
                return st
            else:
                st = "Successfully Added:", choice
                adder(choice)

                return st
    else:
        st = "Not In CoinList:", choice
        return st

def exit_program(button):
    raise urwid.ExitMainLoop()

def unhandled(key):
    if key == 'f8':
        main.original_widget = menu()

def validateCoinInputAdd(coin):
    if coin.lower() in list(map(str.lower, df['RealName'].tolist())) or coin.lower() in list(map(str.lower, df["Symbol"].tolist())):
        return True
    else:
        return False

def validatePortfolioAdd(coin):
    if coin['name'] in portfolioNameGenerator():
        return False
    else:
        return True

#This can validate and return a name
#It will raise an error to signal if it failed so it must always be wrapped in try catch when looped
def validateToName(st):
    if st.lower() in list(map(str.lower, df['RealName'].tolist())):
        return df['RealName'].tolist()[list(map(str.lower, df['RealName'].tolist())).index(st.lower())]
    elif st.lower() in list(map(str.lower, df["Symbol"].tolist())):
        return df['RealName'].tolist()[list(map(str.lower, df['Symbol'].tolist())).index(st.lower())]
    else:
        raise ValueError

def validateToSymbol(st):
        return df['Symbol'].tolist()[list(map(str.lower, df['RealName'].tolist())).index(st.lower())]



'''
██████╗  █████╗ ████████╗ █████╗ 
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
██║  ██║███████║   ██║   ███████║
██║  ██║██╔══██║   ██║   ██╔══██║
██████╔╝██║  ██║   ██║   ██║  ██║
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
'''

def savePortfolio():
    data = {}
    data['portfolio'] = []
    for x in portfolio:
        data['portfolio'].append(x.returnDict())

    savePortfolioCSV(data)
    savePortfolioJSON(data)

def savePortfolioCSV(data):
    prt = data["portfolio"]
    file = open(os.getcwd() + "/savedat/portfolio.csv", 'w')
    csv_writer = csv.writer(file)
    count = 0
    for x in prt:
        if count == 0:
            header = x.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(x.values())
    file.close()

def savePortfolioJSON(data):
    with open(os.getcwd() + "/savedat/portfolio.json", 'w') as jsonfile:
        json.dump(data, jsonfile, indent= 4)
    jsonfile.close()

def loadPortfolioJSON():
    if(path.exists(os.getcwd() + "/savedat/portfolio.json") and os.stat(os.getcwd() + "/savedat/portfolio.json").st_size > 0):
        new = []
        file = open(os.getcwd() + "/savedat/portfolio.json")
        data = json.load(file)
        for i in data["portfolio"]:
            loadAddCoin(i)
    else:
        #This is where a tutorial menu could be placed
        return []

def saveSettingsJSON(inp):
    data = {}
    data['settings'] = []
    data['settings'].append(inp)
    with open(os.getcwd() + "/savedat/userSettings.json", 'w') as jsonfile:
        json.dump(data, jsonfile, indent= 4)
    jsonfile.close()
    

def loadSettingsJSON(data):
    if(path.exists(os.getcwd() + "/savedat/userSettings.json") and os.stat(os.getcwd() + "/savedat/userSettings.json").st_size > 0):
        new = []
        file = open(os.getcwd() + "/savedat/userSettings.json")
        data = json.load(file)
        
        for i in data['settings']:
            global freeCalls
            freeCalls = i['freeCalls']
            global historyCalls
            historyCalls = i['historyCalls']
            global updateCalls
            updateCalls = i['updateCalls']
            

def saveDebugJSON(data):
    pass

def loadDebugJSON(data):
    pass




'''
██████╗ ███████╗██╗    ██╗██████╗ ██╗████████╗███████╗
██╔══██╗██╔════╝██║    ██║██╔══██╗██║╚══██╔══╝██╔════╝
██████╔╝█████╗  ██║ █╗ ██║██████╔╝██║   ██║   █████╗  
██╔══██╗██╔══╝  ██║███╗██║██╔══██╗██║   ██║   ██╔══╝  
██║  ██║███████╗╚███╔███╔╝██║  ██║██║   ██║   ███████╗
╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝
'''



'''
██████╗ ██████╗ ██╗██╗   ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██║██║   ██║██╔════╝██╔══██╗
██║  ██║██████╔╝██║██║   ██║█████╗  ██████╔╝
██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
'''

def item_chosen(button, choice):
    if choice == "Input Coins":
        inputCoinMenu()
    elif choice == "List Coins":
        listCoinMenu()
    elif choice == "Portfolio":
        portfolioMenu()
    elif choice == "Settings":
        settingMenu()
    elif choice == "Debug":
        debugMenu()
    elif choice == "Yes":
        savePortfolio()
        exit_program(button)
    elif choice == "Run Test":
        x = apiManager.ApiManager(portfolio, freeCalls, historyCalls, updateCalls)
        x.historyCall()
    elif choice == "No":
        exit_program(button)
    elif choice == "Exit":
        if saved == True or saved == None:
            exit_program(button)
        else:
            savePrompt()

selectedCoins = loadPortfolioJSON()

pal = [
    ('reversed','light magenta', 'black'),
    ('blackTextRedBox', 'black', 'dark red'),
    ('redText', 'dark red', 'black'),
    ('greenText', 'light green', 'black'),
    ('yellowText', 'yellow', 'black'),
    ('headerMagenta', 'dark magenta', 'black'),
    ('cyanText', 'light cyan', 'black'),
    ('lightBlueText', 'light gray', 'dark gray'),
    (None,  'dark cyan', 'black')]

main = urwid.Padding(menu(), left=2, right=2)
top = urwid.Frame(main)
urwid.MainLoop(top, palette=pal, unhandled_input=unhandled).run()