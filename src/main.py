# -*- coding: Utf-8 -*-

execfile('ambiente27clean/scripts/activate_this.py', dict(__file__='ambiente27clean/scripts/activate_this.py'))
#import Tkinter as tk
from Tkinter import *
import tkMessageBox as tkmsg
from ttk import Combobox, Style, Button as TButton
from modules.Books import Books
from modules.Guis import PageMarkerGui, AddBookGui, CalculatorGui, FindRowGui, ChangeBookGui
from modules.Table import Table
from collections import namedtuple
from modules.Popuphelp import PopupHelp

from PIL import Image, ImageTk

import ttk
class AreaMenu():
    def __init__(self, master):

        menuBar = Menu(master)

        master.config(menu=menuBar)
        iniciarMenu = Menu(menuBar, tearoff=0)
        toolsMenu = Menu(menuBar, tearoff=0)
        ajustesMenu = Menu(menuBar, tearoff=0)
        sobreMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Livro", menu=iniciarMenu)
        menuBar.add_cascade(label="Ferramentas", menu=toolsMenu)
        menuBar.add_cascade(label="Ajustes", menu=ajustesMenu)
        menuBar.add_cascade(label="Sobre", menu=sobreMenu)
        
        iniciarMenu.add_command(label="Criar usuário")#, command=confComando.tituloAplicativo)
        iniciarMenu.add_command(label="Adicionar um livro", command=lambda:AddBookGui(window, Books()))
        iniciarMenu.add_command(label="Adicionar vários livros")

        toolsMenu.add_command(label="Calcular meta de leitura", command=lambda:CalculatorGui(window, Books()))

        sobreMenu.add_command(label="Software")
        sobreMenu.add_command(label="Desenvolvedor")

class PanelPerfilGui:   
    def __init__(self, master, name):
        self.frameMenu = Frame(master, background="#B4CDCD", pady=5)
        self.frameMenu.pack(side=TOP, fill=X)
        self.setPerfil(name)

    def setPerfil(self, name):
        global img
        img_ = Image.open("Images/profile.png")
        img_.thumbnail((80, 80), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_)
        
        Label(self.frameMenu, foreground="#66CD00", background="#B4CDCD", font=("Arial", 12, "bold"), image=img, compound=LEFT).pack(side=LEFT)
        self.cb = Combobox(self.frameMenu, width=18)
        self.cb.pack(side=LEFT, fill=X)
        values = ("Israel Gomes", "Andreza Dantas", "Sandra Noronha")
        self.cb.config(value=values)
        self.cb.config(state="readonly", style="C.TCombobox")
        self.cb.set(values[0])
        #Style().configure("TButton", padding=6, relief="flat")

class PanelInfoGui:
    def __init__(self, master):
        self.book = Books()

        painelTopInfo = Frame(master, background="#B4CDCD", padx=5, pady=5)
        painelTopInfo.pack(side=BOTTOM)
        
        self.totalBooksVar = StringVar()
        self.totalPagesVar = StringVar()
        self.totalPagesReadsVar = StringVar()
        self.totalPagesNotReadsVar = StringVar()
        self.mediaPagesDayVar = StringVar()
        self.mediaPagesBooksVar = StringVar()
        
        Label(painelTopInfo, background="#B4CDCD", text="Total de livros:").grid(row=0, column=0, stick=W)
        Label(painelTopInfo, background="#B4CDCD", text="Total de páginas com conteúdo:").grid(row=1, column=0, stick=W)
        Label(painelTopInfo, background="#B4CDCD", text="Total de páginas lidas:").grid(row=2, column=0, stick=W)
        Label(painelTopInfo, background="#B4CDCD", text="Total de páginas não lidas:").grid(row=3, column=0, stick=W)
        Label(painelTopInfo, background="#B4CDCD", text="Média de páginas em cada livro:").grid(row=4, column=0, stick=W)
        
        Label(painelTopInfo, foreground="#008B8B", background="#B4CDCD", textvariable=self.totalBooksVar).grid(row=0, column=1, stick=E)
        Label(painelTopInfo, foreground="#008B8B", background="#B4CDCD", textvariable=self.totalPagesVar).grid(row=1, column=1, stick=E)
        Label(painelTopInfo, foreground="#008B8B", background="#B4CDCD", textvariable=self.totalPagesReadsVar).grid(row=2, column=1, stick=E)
        Label(painelTopInfo, foreground="#008B8B", background="#B4CDCD", textvariable=self.totalPagesNotReadsVar).grid(row=3, column=1, stick=E)
        Label(painelTopInfo, foreground="#008B8B", background="#B4CDCD", textvariable=self.mediaPagesBooksVar).grid(row=4, column=1, stick=E)
        
        self.setDatas()#Inputa todos os dados nos labels    
    
    def setDatas(self):
        "Inputa todos os dados das Vars do painel esquerdo\n\"date\" recebe dicionario com year, month e day"
        
        totalBooks = self.book.getTotalBooks()

        totalPages = self.book.getTotalPagesContent()
        totalPagesReads = self.book.getTotalPagesReads()
        totalPagesNotReads = self.book.getTotalPagesNotReads()

        self.totalBooksVar.set(totalBooks)
        self.totalPagesVar.set(totalPages)
        self.totalPagesReadsVar.set(totalPagesReads)
        self.totalPagesNotReadsVar.set(totalPagesNotReads)

        if totalPages:mediaPages = str(int(totalPages/totalBooks))
        else: mediaPages = "0"
        self.mediaPagesBooksVar.set(mediaPages)

class PanelTable:
    def __init__(self, master):
        self.master = master
        self.book = Books()

        self.frameTableOptions = Frame(master)
        self.frameTableOptions.pack(expand=True, fill="both")
        
        self.frameOptions = Frame(self.frameTableOptions, background="#B4CDCD")
        self.frameOptions.pack(side=BOTTOM, fill="both", padx=5, pady=5)
        b1 = TButton(self.frameOptions, text="Marcar", command=self.actionWindowEditMarker)
        b1.pack(side=LEFT, padx=5, pady=5)

        b2 = TButton(self.frameOptions, text="Alterar Info", command=self.actionWindowEditInfo)
        b2.pack(side=LEFT, padx=5, pady=5)

        PopupHelp(master, b1, u"Move o marcador para a página atual de leitura do livro")
        PopupHelp(master, b2, u"Altera informações do livro")
        
        headers = (("namebook", ("nome do livro",  50)), 
            ("totalpages", ("total pags",   10)), 
            ("pagebreak", ("pag pausada", 10)), 
            ("initRead", ("inicio leitura", 10)))

        self.table = table = Table(master=self.frameTableOptions, headers=headers, find_field="namebook")
        
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
        id_line_selected = self.table.getIdSelected()
        if id_line_selected >= 0:
            ChangeBookGui(self.master, self.book, id_line_selected)

    def actionWindowEditMarker(self):
        "Atualizar a pagina atual do marcador"
        id_line_selected = self.table.getIdSelected()

        if id_line_selected >= 0:
            print "ActionWindowEdit", self.master
            PageMarkerGui(self.master, self.book, id_line_selected)
        else: print "Id not selected" 

    
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

class Gui(object):
    "Classe main de todas as classes controladoras de interface"
    def __new__(cls, *args, **kwargs):
        return super(Gui, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, master):       
        AM = AreaMenu(master)
        
        frameInfo = Frame(master)
        frameInfo.pack(side=LEFT)
        
        PT = PanelTable(master)
        FR = FindRowGui(PT.table, frameInfo)
        PP = PanelPerfilGui(frameInfo, "Israel")    
        PI = PanelInfoGui(frameInfo)

        
        #PP.setPerfil()
        
        #print pf.setDatas
        pass
if __name__  == "__main__":
    window = Tk()
    window.title("Gerenciador de livros")
    window.geometry("900x400+250+150")
    #window.resizable(False, False)
    #window.positionfrom("user")
    
    gui = Gui(window)
    window.mainloop()
