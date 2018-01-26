# -*- coding: Latin-1 -*-

#import Tkinter as tk
from Tkinter import Frame, Tk, LEFT, TOP, BOTTOM, Label, W, E, StringVar, Button
from Books import Books
from Table import Table
from datetime import date
from collections import namedtuple

class PanelInfo:

    def __init__(self, master):
        self.frameInfo = Frame(master)
        self.frameInfo.pack(side=LEFT)
        
        self.book = Books()
        
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
        
        self.frameTableOptions = Frame(master)
        self.frameTableOptions.pack(expand=True, fill="both")
        
        self.table = table = Table(self.frameTableOptions, (("nome do livro", 50), ("total paginas", 10), ("pagina pausada", 10), ("inicio leitura", 10)))
        table.bindLine("<Button-1>", table.selectRow)
        table.pack(side=TOP, padx=5, pady=5, expand=True, fill="both")
        self.setDatasTable()#Funcao para inserir as linhas de acordo com os dados do self.book.getRecords
        table._updateRegion()
        
        self.frameOptions = Frame(self.frameTableOptions, background="#B4CDCD")
        self.frameOptions.pack(side=BOTTOM, fill="both", padx=5, pady=5)
        Button(self.frameOptions, text="Alterar dados", command=self.actionWindowEdit).pack(side=LEFT, padx=5, pady=5)
        
    def setDatasTable(self):
        Records = namedtuple("Records", "id, nome, total_paginas, pagina_pausada, inicio_leitura")
        for element in map(Records._make, self.book.getRecords()):
            self.table.insertRow(element.id, \
                {"nome do livro":element.nome.encode("Latin-1"),
                "total paginas":str(element.total_paginas),
                "pagina pausada":str(element.pagina_pausada),
                "inicio leitura":str(element.inicio_leitura)})
                
            #print element.id, element.nome.encode("Latin-1"), element.total_paginas
    
    def actionWindowEdit(self):
        id_line_selected = self.table.getIdSelected()
        if id_line_selected:
            print "ActionWindowEdit"
        else: print "Id not selected"
        
    def setDatas(self):
        dt_final = date(2018, 12, 31)
        days_rest = dt_final - dt_final.today()
        days_rest = days_rest.days
        
        totalBooks = self.book.getTotalBooks()
        totalPages = self.book.getTotalPages()
        totalPagesReads = self.book.getTotalPagesReads()
        totalPagesNotReads = self.book.getTotalPagesNotReads()
        self.daysRestVar.set("Páginas para ler por dia durante {} dias:".format(days_rest))
        mediaPagesDay = self.book.getMediaPagesDay(totalPagesNotReads, days_rest)
        
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
    window.geometry("900x400+250+150")
    #window.resizable(False, False)
    
    gui = Gui(window)
    gui.pack(fill="x")

    window.mainloop()
