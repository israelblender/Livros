# -*- coding: Utf-8 -*-

execfile('ambiente27clean/scripts/activate_this.py', dict(__file__='ambiente27clean/scripts/activate_this.py'))
#import Tkinter as tk
from Tkinter import *
import tkMessageBox as tkmsg
from ttk import Combobox, Style
from Books import Books
from Table import Table
from datetime import date
from collections import namedtuple

from PIL import Image, ImageTk

class AreaMenu():
    def __init__(self, master):

        menuBar = Menu(master)

        master.config(menu=menuBar)
        iniciarMenu = Menu(menuBar, tearoff=0)
        ajustesMenu = Menu(menuBar, tearoff=0)
        sobreMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Iniciar", menu=iniciarMenu)
        menuBar.add_cascade(label="Ajustes", menu=ajustesMenu)
        menuBar.add_cascade(label="Sobre", menu=sobreMenu)
        
        iniciarMenu.add_command(label="Criar usuário")#, command=confComando.tituloAplicativo)
        iniciarMenu.add_command(label="Adicionar um livro")
        iniciarMenu.add_command(label="Adicionar vários livros")

        sobreMenu.add_command(label="Desenvolvedor")

class PanelPerfil:
    def setPerfil(self, name):
        global img
        img_ = Image.open("Images/profile.png")
        img_.thumbnail((80, 80), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_)
        
        Label(self.frameMenu, foreground="#66CD00", font=("Arial", 12, "bold"), image=img, compound=LEFT).pack(side=LEFT)
        self.cb = Combobox(self.frameMenu)
        self.cb.pack(side=LEFT)
        values = ("Israel Gomes", "Andreza Dantas", "Sandra Noronha")
        self.cb.config(value=values)
        self.cb.config(state="readonly", style="C.TCombobox")
        self.cb.set(values[0])
        #Style().configure("TButton", padding=6, relief="flat")
    
    def __init__(self, master, name):
        self.frameMenu = Frame(master, height=110)
        self.frameMenu.pack(side=TOP, pady=0)
        self.setPerfil(name)

class PanelInfo:        
    def __init__(self, master, book):

        painelTopInfo = Frame(master)
        painelTopInfo.pack(side=BOTTOM)
    
        self.book = book
        
        self.totalBooksVar = StringVar()
        self.totalPagesVar = StringVar()
        self.totalPagesReadsVar = StringVar()
        self.totalPagesNotReadsVar = StringVar()
        self.mediaPagesDayVar = StringVar()
        self.mediaPagesBooksVar = StringVar()
        self.daysRestVar = StringVar()
        
        Label(painelTopInfo, text="Total de livros:").grid(row=0, column=0, stick=W)
        Label(painelTopInfo, text="Total de páginas com conteúdo:").grid(row=1, column=0, stick=W)
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
        
        painelBottomInfo = Frame(master)
        painelBottomInfo.pack(side=TOP)
        
        inputDateFrame = Frame(painelBottomInfo)#Contem todos os Labels e Entrys
        inputDateFrame.pack(side=TOP)
        
        showMediaPagesDayFrame = Frame(painelBottomInfo)#Contem os Labels de exibição de resultado
        showMediaPagesDayFrame.pack(side=TOP)

        Label(inputDateFrame, text="Dia").grid(row=0, column=0, stick=W)
        Entry(inputDateFrame, textvariable=self.finalDayVar, width=3).grid(row=0, column=1, stick=E, padx=2)
        Label(inputDateFrame, text="Mês").grid(row=0, column=2, stick=W)
        Entry(inputDateFrame, textvariable=self.finalMonthVar, width=3).grid(row=0, column=3, stick=E, padx=2)
        Label(inputDateFrame, text="Ano").grid(row=0, column=4, stick=W)
        Entry(inputDateFrame, textvariable=self.finalYearVar, width=5).grid(row=0, column=5, stick=E, padx=2)
        Button(inputDateFrame, text="Calcular", command=self.actionShowMediaPagesDay, padx=5).grid(row=0, column=6, stick=E)
        
        Label(showMediaPagesDayFrame, textvariable=self.daysRestVar, foreground="#66CD00", font=("Arial", 10, "bold")).grid(row=0, column=0, stick=W)
        Label(showMediaPagesDayFrame, textvariable=self.mediaPagesDayVar).grid(row=0, column=1, stick=E)
        
        self.setDatas()#Inputa todos os dados nos labels    
    
    def setDatas(self):
        "Inputa todos os dados das Vars do painel esquerdo\n\"date\" recebe dicionario com year, month e day"
        days_rest = self.getDaysRest({"day": 31, "month": 12, "year": 2018})
        totalBooks = self.book.getTotalBooks()

        totalPages = self.book.getTotalPagesContent()
        totalPagesReads = self.book.getTotalPagesReads()
        totalPagesNotReads = self.book.getTotalPagesNotReads()
        self.setDaysRestLabel(days_rest)
        mediaPagesDay = self.book.getMediaPagesDay(totalPagesNotReads, days_rest)#Retorna a media de páginas por dia

        self.totalBooksVar.set(totalBooks)
        self.totalPagesVar.set(totalPages)
        self.totalPagesReadsVar.set(totalPagesReads)
        self.totalPagesNotReadsVar.set(totalPagesNotReads)

        if totalPages:mediaPages = str(int(totalPages/totalBooks))
        else: mediaPages = "0"
        self.mediaPagesBooksVar.set(mediaPages)
        self.setMediaPagesDayVar(mediaPagesDay)
        

        
    def getDaysRest(self, date_final_dict):#Calcula a quantidade de dias que faltam para ler com base na data recebida
        #print type(date_final.get("year"))
        try:
            print date_final_dict
            dt_final = date(year=date_final_dict.get("year"), month=date_final_dict.get("month"), day=date_final_dict.get("day"))
        except ValueError:
            date_final_dict["day"] -= 1
            return self.getDaysRest(date_final_dict)
            
            #dt_final = setDate(date_final)
        
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

class PanelTable:
    def __init__(self, master, book):
        self.master = master
        self.book = book
        self.frameTableOptions = Frame(master)
        self.frameTableOptions.pack(expand=True, fill="both")
        
        self.frameOptions = Frame(self.frameTableOptions, background="#B4CDCD")
        self.frameOptions.pack(side=BOTTOM, fill="both", padx=5, pady=5)
        Button(self.frameOptions, text="Alterar Marcador", command=self.actionWindowEditMarker).pack(side=LEFT, padx=5, pady=5)
        Button(self.frameOptions, text="Alterar Informações", command=self.actionWindowEditInfo).pack(side=LEFT, padx=5, pady=5)
        
        
        self.table = table = Table(self.frameTableOptions, 
        ( ("namebook", ("nome do livro", 50)), 
        ("totalpages", ("total pags", 10)), 
        ("pagebreak", ("pag pausada", 10)), 
        ("initRead", ("inicio leitura", 10)) ),
        #height_cel=4
        )
        
        table.bind("<Button-1>", table.selectRowEvent)
        table.bind("<Up>", table.selectPreviousRowEvent, type="only", action="up")
        table.bind("<Down>", table.selectNextRowEvent, type="only", action="down")
        table.bind("<MouseWheel>", table.mouseWheelEvent, action="wheel")   
        table.pack(side=TOP, padx=5, pady=5, expand=True, fill="both")
        
        self.setDatasTable()#Funcao para inserir as linhas de acordo com os dados do self.book.getRecordsDb
        table.updateRegion()
        table.selectRowByNumberLine(row=1)
    def actionWindowEditInfo(self):
        "Atualizar informacoes do livro"
        pass

    def actionWindowEditMarker(self):
        "Atualizar a pagina atual do marcador"
        id_line_selected = self.table.getIdSelected()
        if id_line_selected:
            print "ActionWindowEdit"
            self.topwindow = topwindow = Toplevel(self.master)
            topwindow.geometry("350x100+150+150")
            topwindow.transient(self.master)
            
            self.labelNameBookVar = StringVar()
            self.inputPagePausedVar = StringVar()

            Label(topwindow, textvar=self.labelNameBookVar, foreground="blue", font=("Arial", 12, "bold")).pack(side=TOP)
            panel = Frame(topwindow)
            panel.pack(side=TOP, padx=20, pady=20)
            Label(panel, text=u"Página pausada").pack(side=LEFT)
            Entry(panel, textvariable=self.inputPagePausedVar, width=4).pack(side=LEFT)

            Button(panel, text="Salvar Marcador", \
                command=lambda id_line_selected=id_line_selected: self.actionUpdatePagePausedBook(id_line_selected)).pack(side=LEFT, padx=10)



            self.setPagePausedBook(id_line_selected)
        else: print "Id not selected" 

    def setPagePausedBook(self, id_line_selected):
        "Inputa as informacoes necessarias do book"
        book_name, page_paused = self.book.getBook("nome, pagina_pausada", id_line_selected)
        percent = self.book.getPercentReadBook(id_line_selected)

        self.labelNameBookVar.set(book_name.upper())
        self.inputPagePausedVar.set(page_paused)
    def actionUpdatePagePausedBook(self, id_line_selected):
        "Atualiza o banco de dados com a página atual do marcador de página"
        self.book.updatePagePaused(id_line_selected, self.inputPagePausedVar.get())
        tkmsg.showinfo("Atualizado", "Marcador atualizado")
    
    def setDatasTable(self):#inserte as linbhas na tabela
        "Inputa todas as linhas do banco de dados na tabela"
        Records = namedtuple("Records", "id, nome, total_paginas, pagina_pausada, inicio_leitura")
        for element in map(Records._make, self.book.getAllBooks(columns_str="id, nome, total_paginas, pagina_pausada, inicio_leitura")):
            self.table.insertRow(element.id, \
                {"namebook":element.nome.encode("Latin-1"),
                "totalpages":str(element.total_paginas),
                "pagebreak":str(element.pagina_pausada),
                "initRead":str(element.inicio_leitura)})
            #break
            #print element.id, element.nome.encode("Latin-1"), element.total_paginas

class Gui(object, Frame):
    "Classe main de todas as classes controladoras de interface"
    def __new__(cls, *args, **kwargs):
        return super(Gui, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, master):
        Frame.__init__(self, master)
        
        books = Books()
        
        AM = AreaMenu(master)
        
        frameInfo = Frame(master)
        frameInfo.pack(side=LEFT)
        
        PP = PanelPerfil(frameInfo, "Carla Santos")    
        PF = PanelInfo(frameInfo, books)
        PT = PanelTable(master, books)
        
        #PP.setPerfil()
        
        
        
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
