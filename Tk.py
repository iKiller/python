#!/usr/bin/env python

import Tkinter as tk

def Next():
    print 'Next !'
    
def Last():
    print 'Last !'

def Play():
    print 'Play !'
    
def hello():
    print 'hello menu!'

class Application(tk.Frame:
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        top = self.winfo_toplevel()
        self.menubar = tk.Menu(top)
        self.filemenu = tk.Menu(self.menubar, activebackground='blue', activeborderwidth='1c', cursor='mouse', tearoff = 0)
        for item in ['Open Playlist', 'Add Songs', 'Add Document', 'Exit']:
            self.filemenu.add_command(label = item, command = hello)
        self.menubar.add_cascade(label = 'file', menu = self.filemenu)
        top['menu'] = self.menubar
        self.grid()

        self.quitButton = tk.Button(self, text='Exit', command=self.quit)
        self.quitButton.grid(row=5, column=0, columnspan=3)

        self.NextButton = tk.Button(self, text='Next', command=Next)
        self.NextButton.grid(row=5, column=1, columnspan=3)

        self.LastButton = tk.Button(self, text='Last', command=Last)
        self.LastButton.grid(row=5, column=2, columnspan=3)

        self.PlayButton = tk.Button(self, text='Play', command=Play)
        self.PlayButton.grid(row=5, column=3, columnspan=3)        

app = Application()
app.master.title('Goddess Music Player')
app.mainloop()


