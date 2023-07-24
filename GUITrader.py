import yfinance as yf
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class user:
    qBase = {
            "questions":[f"Hey there, what ticker would you like to get (type \"o\" for other or \"q\" to quit)? ",
                        f"Please enter the start date \"year-month-day\": ",
                        f"Please enter the end date \"year-month-day\": ",
                        "Choose \"p\" to plot or \"d\" to display dataset: ",
                        "Which ticker would you like to plot? ",
                        "Which ticker would you like to display data for? ",
                        "Return (y to continue)"],
            "answers":["n",
                       None,
                       None,
                       ["p","d","n"]]
        }

    def __init__(self) -> None:

        self.tickers = {}
        self.question = self.qBase["questions"]
        self.answer = self.qBase["answers"]
        self.Qtracker = 0
        self.other = False
        self.edit = None
        self.tempTIK = []
        self.default = True


    def run(self) -> bool:
        #self.personalise()
        layout = [[sg.Text(f""), sg.Text(size=(60, 1), key='-OUTPUT-',background_color="LightBlue1",text_color="black")],
          [sg.Text(""), sg.Text(size=(60, 1), key='-OUTPUTA-',background_color="LightBlue1",text_color="black")],
          [sg.Text('Answer here:'), sg.InputText(size=(60, 1), key='-INPUT-',background_color="LightBlue1",text_color="black"),sg.Button('Submit'), sg.Button('Cancel')],
          [sg.Canvas(size=(500,500),key='-CANVAS-',background_color="LightBlue1")]
          ]
        sg.theme("Python")
        window = sg.Window('yfinance data', layout,finalize=True,element_justification="center",size=(800,800))
        
        while True:
            event, values = window.read()
            if self.default:
                window['-OUTPUT-'].update(self.question[0])
                self.default = False

            elif event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            
            elif values['-INPUT-'] == "q":
                break

            elif values['-INPUT-'] == "o":
                window['-OUTPUT-'].update(self.question[3])
                window['-INPUT-'].update('')
                self.other = True

            elif values['-INPUT-'] == "p":
                s= self.tickerDisplay()
                window['-OUTPUT-'].update(self.question[4])
                window['-OUTPUTA-'].update(s)
                window['-INPUT-'].update('')
                self.edit = "p"

            elif values['-INPUT-'] == "d":
                s= self.tickerDisplay()
                window['-OUTPUT-'].update(self.question[5])
                window['-OUTPUTA-'].update(s)
                window['-INPUT-'].update('')
                self.edit = "d"

            elif self.edit == "p" and self.other: #Where the propgram plots the diagram
                FIGURE_obj = self.plot(values['-INPUT-'])
                self.draw_figure(window['-CANVAS-'].TKCanvas,FIGURE_obj)
                window['-OUTPUT-'].update(self.question[6])
                window['-INPUT-'].update('')
                self.edit = None
                self.other = False

            elif self.edit == "d" and self.other:
                FIGURE_obj = self.display(values['-INPUT-'],window['-CANVAS-'].TKCanvas)
                self.draw_figure(window['-CANVAS-'].TKCanvas,FIGURE_obj)
                window['-OUTPUT-'].update(self.question[0])
                window['-INPUT-'].update('')
                self.edit = None
                self.other = False
            
            elif len(values['-INPUT-']) == 4:
                self.tempTIK.append(values['-INPUT-'])
                window['-OUTPUT-'].update(self.question[1])
                window['-INPUT-'].update('')
                self.edit = "s"
            
            elif self.edit == "s":
                self.tempTIK.append(values['-INPUT-'])
                window['-OUTPUT-'].update(self.question[2])
                window['-INPUT-'].update('')
                self.edit = "e"

            elif self.edit == "e":
                self.tempTIK.append(values['-INPUT-'])
                self.adding_ticker(self.tempTIK)
                self.tempTIK.clear()
                window['-OUTPUT-'].update(self.question[0])
                window['-INPUT-'].update('')
                self.edit = None
            
            elif values['-INPUT-'] == 'y':
                window['-OUTPUT-'].update(self.question[0])
                window['-INPUT-'].update('')
                window['-OUTPUTA-'].update('')
                window["-CANVAS-"].TKCanvas.delete('all')
                
        window.close()

    def tickerDisplay(self):
        s = "---TICKERS---"
        for values in self.tickers.values():
            print(values.getName())
            s += f"    {values.getName()}    "
        return s

    
    def plot(self,t):
        obj = self.tickers[t].getData()
        obj['Adj Close'].plot()
        plt.title("Closing Prices")
        plt.grid(True)
        return plt.gcf()

    def display(self,t,canvas):
        tkc = canvas
        obj = self.tickers[t].getData()
        print(obj.head())
        print(obj.tail())
        fig = [tkc.create_rectangle(100, 100, 600, 400, outline='white'),
        tkc.create_line(50, 50, 650, 450, fill='red', width=5),
        tkc.create_oval(150,150,550,350, fill='blue'),
        tkc.create_text(350, 250, text="Hello World",
        fill='white', font=('Arial Bold', 16))]
        return fig

    def adding_ticker(self, t):

        TICKER = ticker(t[0],t[1],t[2])
        self.tickers[t[0]] = TICKER

    def personalise(self) -> None:
        self.username = input("What is your name? ")

    def draw_figure(self,canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg


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

u = user()
u.run()
exit()

