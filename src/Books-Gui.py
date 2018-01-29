# -*- coding: Latin-1 -*-

#import Tkinter as tk
from Tkinter import Frame, Tk, LEFT, TOP, BOTTOM, Label, W, E, StringVar, IntVar, Button, Entry
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
        
        painelTopInfo = Frame(self.frameInfo)
        painelTopInfo.pack(side=TOP)
        
        Label(painelTopInfo, text="Total de livros:").grid(row=0, column=0, stick=W)
        Label(painelTopInfo, text="Total de páginas sem sumários:").grid(row=1, column=0, stick=W)
        Label(painelTopInfo, text="Total de páginas lidas:").grid(row=2, column=0, stick=W)
        Label(painelTopInfo, text="Total de páginas não lidas:").grid(row=3, column=0, stick=W)
        Label(painelTopInfo, text="Média de páginas em cada livro:").grid(row=4, column=0, stick=W)
        
        Label(painelTopInfo, textvariable=self.totalBooksVar).grid(row=0, column=1, stick=E)
        Label(painelTopInfo, textvariable=self.totalPagesVar).grid(row=1, column=1, stick=E)
        Label(painelTopInfo, textvariable=self.totalPagesReadsVar).grid(row=2, column=1, stick=E)
        Label(painelTopInfo, textvariable=self.totalPagesNotReadsVar).grid(row=3, column=1, stick=E)
        Label(painelTopInfo, textvariable=self.mediaPagesBooksVar).grid(row=4, column=1, stick=E)
        
        
        self.finalDayVar = IntVar()
        self.finalMonthVar = IntVar()
        self.finalYearVar = IntVar()
        
        self.finalDayVar.set("31")
        self.finalMonthVar.set("12")
        self.finalYearVar.set("2018")
        
        painelBottomInfo = Frame(self.frameInfo)
        painelBottomInfo.pack(side=TOP)
        
        inputDateFrame = Frame(painelBottomInfo)
        inputDateFrame.pack(side=TOP)
        
        showMediaPagesDayFrame = Frame(painelBottomInfo)
        showMediaPagesDayFrame.pack(side=TOP)
        
        Label(showMediaPagesDayFrame, textvariable=self.daysRestVar, foreground="#66CD00", font=("Arial", 10, "bold")).grid(row=0, column=0, stick=W)
        Label(showMediaPagesDayFrame, textvariable=self.mediaPagesDayVar).grid(row=0, column=1, stick=E)
        
        Label(inputDateFrame, text="Dia").grid(row=0, column=0, stick=W)
        Entry(inputDateFrame, textvariable=self.finalDayVar, width=3).grid(row=0, column=1, stick=E)
        Label(inputDateFrame, text="Mês").grid(row=0, column=2, stick=W)
        Entry(inputDateFrame, textvariable=self.finalMonthVar, width=3).grid(row=0, column=3, stick=E)
        Label(inputDateFrame, text="Ano").grid(row=0, column=4, stick=W)
        Entry(inputDateFrame, textvariable=self.finalYearVar, width=5).grid(row=0, column=5, stick=E)
        Button(inputDateFrame, text="Calcular", command=self.actionShowMediaPagesDay).grid(row=0, column=6, stick=E)
        
        self.setDatas()#Inputa todos os dados nos labels
        
        self.frameTableOptions = Frame(master)
        self.frameTableOptions.pack(expand=True, fill="both")
        
        self.table = table = Table(self.frameTableOptions, 
        ( ("namebook", ("nome do livro", 50)), 
        ("totalpages", ("total pags", 10)), 
        ("pagebreak", ("pag pausada", 10)), 
        ("initRead", ("inicio leitura", 10)) ))
        
        table.bind("<Button-1>", table.selectRowEvent)
        table.bind("<Up>", table.selectPreviousRowEvent, "all")
        table.bind("<Down>", table.selectNextRowEvent, "all")
        table.bind("<MouseWheel>", table.mouseWheelEvent)   
        table.pack(side=TOP, padx=5, pady=5, expand=True, fill="both")
        
        self.setDatasTable()#Funcao para inserir as linhas de acordo com os dados do self.book.getRecords
        table._updateRegion()
        table.selectRowByNumberLine(row=1)
        
        self.frameOptions = Frame(self.frameTableOptions, background="#B4CDCD")
        self.frameOptions.pack(side=BOTTOM, fill="both", padx=5, pady=5)
        Button(self.frameOptions, text="Alterar dados", command=self.actionWindowEdit).pack(side=LEFT, padx=5, pady=5)
    
    def actionWindowEdit(self):
        id_line_selected = self.table.getIdSelected()
        if id_line_selected:
            print "ActionWindowEdit"
        else: print "Id not selected"  
    
    def setDatasTable(self):#inserte as linbhas na tabela
        "Inputa todas as linhas do banco de dados na tabela"
        Records = namedtuple("Records", "id, nome, total_paginas, pagina_pausada, inicio_leitura")
        for element in map(Records._make, self.book.getRecords()):
            self.table.insertRow(element.id, \
                {"namebook":element.nome.encode("Latin-1"),
                "totalpages":str(element.total_paginas),
                "pagebreak":str(element.pagina_pausada),
                "initRead":str(element.inicio_leitura)})
            #break
            #print element.id, element.nome.encode("Latin-1"), element.total_paginas
    
    def setDatas(self):
        "Inputa todos os dados das Vars do painel esquerdo\n\"date\" recebe dicionario com year, month e day"
        days_rest = self.getDaysRest({"day": 31, "month": 12, "year": 2018})
        
        totalBooks = self.book.getTotalBooks()
        totalPages = self.book.getTotalPages()
        totalPagesReads = self.book.getTotalPagesReads()
        totalPagesNotReads = self.book.getTotalPagesNotReads()
        self.setDaysRestLabel(days_rest)
        mediaPagesDay = self.book.getMediaPagesDay(totalPagesNotReads, days_rest)#Retorna a media de páginas por dia
        
        self.totalBooksVar.set(totalBooks)
        self.totalPagesVar.set(totalPages)
        self.totalPagesReadsVar.set(totalPagesReads)
        self.totalPagesNotReadsVar.set(totalPagesNotReads)
        self.mediaPagesBooksVar.set(str(int(totalPages/totalBooks)))
        self.setMediaPagesDayVar(mediaPagesDay)
        
    def getDaysRest(self, date_final):#Calcula a quantidade de dias que faltam para ler com base na data recebida
        print type(date_final.get("year"))
        dt_final = date(date_final.get("year"), date_final.get("month"), date_final.get("day"))
        days_rest = dt_final - dt_final.today()
        days_rest = days_rest.days
        return days_rest
    def setDaysRestLabel(self, days_rest):
        self.daysRestVar.set("Paginas/dia durante {} dias:".format(days_rest))
    
    def setMediaPagesDayVar(self, mediaPagesDay):
        self.mediaPagesDayVar.set(mediaPagesDay)
    
    def actionShowMediaPagesDay(self):
        days_rest = self.getDaysRest({"day": self.finalDayVar.get(), "month": self.finalMonthVar.get(), "year": self.finalYearVar.get()})#Calcula os dias restantes
        self.setDaysRestLabel(days_rest)#Escreve na Label os dias restantes
        self.setMediaPagesDayVar(self.book.getMediaPagesDay(self.book.getTotalPagesNotReads(), days_rest))#Escreve na Label a media de pagina para ler por dia
        


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
