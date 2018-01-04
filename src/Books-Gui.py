# -*- coding: Latin-1 -*-

#import Tkinter as tk
from Tkinter import Frame, Tk, LEFT, Label, W, E, StringVar
from Books import Books
from Table import Table
from datetime import date

class PanelInfo:

    def __init__(self, master):
        self.frameInfo = Frame(master)
        self.frameInfo.pack(side=LEFT)
        
        self.books = Books()
        
        self.totalBooksVar = StringVar()
        self.totalPagesVar = StringVar()
        self.totalPagesReadsVar = StringVar()
        self.totalPagesNotReadsVar = StringVar()
        self.mediaPagesDayVar = StringVar()
        self.mediaPagesBooksVar = StringVar()
        self.daysRestVar = StringVar()
        
        Label(self.frameInfo, text="Total de livros:").grid(row=0, column=0, stick=W)
        Label(self.frameInfo, text="Total de páginas sem sumários:").grid(row=1, column=0, stick=W)
        Label(self.frameInfo, text="Total de páginas lidas:").grid(row=2, column=0, stick=W)
        Label(self.frameInfo, text="Total de páginas não lidas:").grid(row=3, column=0, stick=W)
        Label(self.frameInfo, text="Média de páginas em cada livro:").grid(row=4, column=0, stick=W)
        Label(self.frameInfo, textvariable=self.daysRestVar, foreground="#66CD00").grid(row=5, column=0, stick=W)
        
        Label(self.frameInfo, textvariable=self.totalBooksVar).grid(row=0, column=1, stick=E)
        Label(self.frameInfo, textvariable=self.totalPagesVar).grid(row=1, column=1, stick=E)
        Label(self.frameInfo, textvariable=self.totalPagesReadsVar).grid(row=2, column=1, stick=E)
        Label(self.frameInfo, textvariable=self.totalPagesNotReadsVar).grid(row=3, column=1, stick=E)
        Label(self.frameInfo, textvariable=self.mediaPagesBooksVar).grid(row=4, column=1, stick=E)
        Label(self.frameInfo, textvariable=self.mediaPagesDayVar).grid(row=5, column=1, stick=E)
        
        self.setDatas()
        
        self.frameTable = Frame(master)
        
        self.frameTable.pack(side=LEFT)
        
    def setDatas(self):
        dt_final = date(2018, 12, 31)
        days_rest = dt_final - dt_final.today()
        days_rest = days_rest.days
        
        totalBooks = self.books.getTotalBooks()
        totalPages = self.books.getTotalPages()
        totalPagesReads = self.books.getTotalPagesReads()
        totalPagesNotReads = self.books.getTotalPagesNotReads()
        self.daysRestVar.set("Páginas para ler por dia durante {} dias:".format(days_rest))
        mediaPagesDay = self.books.getMediaPagesDay(totalPagesNotReads, days_rest)
        
        self.totalBooksVar.set(totalBooks)
        self.totalPagesVar.set(totalPages)
        self.totalPagesReadsVar.set(totalPagesReads)
        self.totalPagesNotReadsVar.set(totalPagesNotReads)
        self.mediaPagesBooksVar.set(str(int(totalPages/totalBooks)))
        self.mediaPagesDayVar.set(mediaPagesDay)
        


class Gui(object, Frame):
    def __new__(cls, *args, **kwargs):
        return super(Gui, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, master):
        Frame.__init__(self, master)
        pf = PanelInfo(master)
        
        #print pf.setDatas
        pass
if __name__  == "__main__":
    window = Tk()
    window.title("Gerenciador de livros")
    window.geometry("700x400+250+150")
    window.resizable(False, False)
    
    gui = Gui(window)
    gui.pack()

    window.mainloop()
