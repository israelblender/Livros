# -*- coding: Latin-1 -*-

import Tkinter as tk
from Books import Books

class Gui(object, tk.Frame):
    def __new__(cls, *args, **kwargs):
        return super(Gui, cls).__new__(cls, *args, **kwargs)
    
    def __init__(cls, master):
        tk.Frame.__init__(cls, master)



if __name__  == "__main__":
    window = tk.Tk()
    window.title("Gerenciador de livros")
    window.geometry("700x400+250+150")
    window.resizable(False, False)
    
    gui = Gui(window)
    gui.pack()

    window.mainloop()
