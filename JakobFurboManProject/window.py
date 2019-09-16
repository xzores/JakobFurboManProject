from tkinter import *

from pprint import pprint

def callback():
    print("callback")

class Window:

    def configure(self):
        ratio = min(self.x / self.y, 1);
        self.frame.place(relx = 0, rely = 0, relwidth = 1, relheight = ratio);
        self.frame2.place(relx = 0, rely = ratio, relwidth = 1, relheight = 1-ratio);

    def onResize(self, event):
        pprint(event)
        self.x = event.width
        self.y = event.height
        self.configure();

    def keyPress(self, key):
        self.callKeyPress(key);

    def __init__(self, width: int = 600, height: int = 600, titel : str = "window name"):
        self.x = width
        self.y = height
        self.titel = titel

        self.window = Tk();
        self.window.title(self.titel);
        self.window.resizable(False, False)
        #self.window.bind('<Configure>', lambda e : self.onResize(e))
        self.window.bind('<Key>', self.keyPress) 
        self.window.geometry(str(width) + "x" + str(height))
        
        self.frame = Frame(self.window, bg = "blue");
        self.frame2 = Frame(self.window, bg = "grey");

        self.wallBotton = Button(self.frame2, bg = "grey", text = "wall");
        self.startBotton = Button(self.frame2, bg = "red", text = "start");
        self.endBotton = Button(self.frame2, bg = "green", text = "end");
        self.emptyBotton = Button(self.frame2, bg = "white", text = "empty");

        self.wallBotton.grid(row = 0, column = 0)
        self.startBotton.grid(row = 0, column = 1)
        self.endBotton.grid(row = 0, column = 2)
        self.emptyBotton.grid(row = 0, column = 3)

        class e():
            def __init__(self, width: int = 600, height: int = 600):
                self.width = width
                self.height = height

        self.onResize(e(width,height));
        

    def makeButton(self, x : float, y : float, width : float, height : float):
            b = Button(self.frame, text = "", command = callback, bg = "white", highlightthickness = 0, bd = 0, anchor=NW, font=('Helvetica', '8'));
            b.place(relx = x / 1000, rely = y / 1000, relwidth = width / 1000, relheight = height / 1000);
            return b;

    def run(self):
        self.window.mainloop();


