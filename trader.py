import yfinance as yf
import matplotlib.pyplot as plt
import PySimpleGUI as sg

class user:

    def __init__(self) -> None:
        self.username = None
        self.tickers = {}

    def run(self) -> bool:
        self.personalise()
        while True:
            event, values = window.read()
            t = input(f"Hey {self.username}, what ticker would you like to get (type \"n\" for other)? ")
            if t == 'n':
                result,tickername = self.alternative()
                print(result)
                if result == "n":
                    return True
                elif result == "p":
                    self.plot(tickername)
                elif result == "d":
                    self.display(tickername)
            else:
                self.adding_ticker(t)

    
    def plot(self,t):
        obj = self.tickers[t].getData()
        obj['Adj Close'].plot()
        plt.show()

    def display(self,t):
        obj = self.tickers[t].getData()
        print(obj.head())
        print(obj.tail())
    
    def alternative(self) -> str:
        print("p for plot")
        print("d for display")
        print("n to exit")
        x = input("Choose: ")
        print("If you didn't choose n, please select a ticker:")
        for values in self.tickers.values():
            print(values.getName())
        y = input("Ticker(click enter if n was chosen):")
        return x,y

    def adding_ticker(self, t):
        s = input(f"{self.username}, please enter the start date \"year-month-day\": ")
        e = input(f"{self.username}, please enter the end date \"year-month-day\": ")
        TICKER = ticker(t,s,e)
        self.tickers[t] = TICKER

    def personalise(self) -> None:
        self.username = input("What is your name? ")


class ticker:

    def __init__(self,ticker,start,end) -> None:
        self.name = ticker
        self.start = start
        self.end = end
        self.data = yf.download(ticker,start,end)
    
    def getData(self):
        return self.data
    
    def getName(self):
        return self.name
    
#sg setup
layout = [
    [sg.Text("QUESTIONS"),sg.Text(size=(20,1) ,key='-OUT-')],
    [sg.Input(key="-IN-")],
    [sg.Button('Ok'), sg.Button("Quit")]
]
window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event in ('Quit',None):
        break
    if event == 'OK' and len(values) > 0:
        window['-OUT-'].update(values['-IN-'])
window.close()
exit()
# while True:
#     u = user()
#     if u.run():
#         exit()
#     del u
    