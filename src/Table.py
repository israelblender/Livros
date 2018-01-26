# -*- coding: Latin-1 -*-
__author__ = "Israel"
__date__ = "$30/12/2017 21:54:12$"

import Tkinter as tk
from collections import namedtuple

class Table(object, tk.Frame):
    def __new__(cls, *args, **kwargs):
        return super(Table, cls).__new__(cls, *args, **kwargs)

    def __init__(self, master, headers, **kwargs):
        tk.Frame.__init__(self, master, cnf=kwargs)
        frameCanvasScrolly = tk.Frame(self)
        frameCanvasScrolly.pack(side=tk.TOP, fill="both", expand=True)
        self.canvas = canvas = tk.Canvas(frameCanvasScrolly, scrollregion=(0, 0, 1100, 1000), background="#CAE1FF")
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        
        self.frameCelulas = tk.Frame(canvas)
        canvas.create_window(0, 0, window=self.frameCelulas, anchor=tk.NW)

        scrolly = tk.Scrollbar(frameCanvasScrolly, orient=tk.VERTICAL, command=canvas.yview)
        scrolly.pack(side=tk.LEFT, fill="y")
        #scrolly.grid(row=0, column=1)
        canvas['yscrollcommand'] = scrolly.set
        
        scrollx = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollx.pack(side=tk.TOP, fill="x")
        canvas['xscrollcommand'] = scrollx.set
        
        self.master = master
        self.row = 0
        #self._bindStringDict = {}#1: "<Button-1>", 2: "<Button-2>", 3: "<Button-3>"}
        self.bindList = {}
        self._lastWidgetsSelecteds = None
        self.ColunasBind = namedtuple("ColunasBind", "string,function")

        self.configColors(bg="#B4CDCD", bg_header="#68838B")
        self.configHeader(headers)
        self._unique_id_selected = None
    def configSize(self, width, height):
        self.config(width=width, height=height)#Muda tamanho do frame Table
        #self.canvas.config(width=width, height=height)
    
    def configHeader(self, headers):
        self.headers = headers
        self.infoSizeCols = dict(headers)
        self.dict_headers = {}
        for index, elem in enumerate(headers):
            self.dict_headers[index] = elem[0]
        self.insertLine(-1, self.dict_headers, "header")

    def configColors(self, bg, bg_header):
        self._colorBgPatern = bg
        self._colorBgHeader = bg_header
    
    def insertRow(self, unique_id, elements):
        if len(elements) != len(self.infoSizeCols):
            raise Exception("Erro", u"A quantidade de elementos informados nao e igual a quantidade registrada!")
        return self.insertLine(unique_id, elements, "cel")

    def insertLine(self, unique_id, elements, type):
        self._insertCelulasByElement(unique_id, elements, type)
        self.row += 1
    
    def _updateRegion(self):#Atualiza a região para que o scroll se encaixe no quadro da tabela
        self.frameCelulas.update()
        self.canvas.config(scrollregion=(0, 0, self.frameCelulas.winfo_width(), self.frameCelulas.winfo_height()))
        
    def _insertCelulasByElement(self, unique_id, cols_values, type):
        col = 0
        if type == "cel":
            for index in range(len(cols_values)):
                col_key = self.dict_headers.get(index)
                cel = self._insertCelula(row=self.row, col=col, 
                    unique_id = unique_id, 
                    width = self.infoSizeCols.get(col_key),
                    value = cols_values.get(col_key),
                    background=self._colorBgPatern)
                self._addBinds(cel)
                col += 1
        elif type == "header":
            for index in range(len(cols_values)):
                col_key = self.dict_headers.get(index)
                self._insertCelula(row=0, col=col, 
                        unique_id = unique_id, 
                        width = self.infoSizeCols.get(col_key),
                        value = self.dict_headers.get(index),
                        relief=tk.GROOVE,
                        background=self._colorBgHeader)
                col += 1
    
    #def _bindFunction(self, events):
        #print events.char, events.delta, events.height, events.keycode, events.keysym, events.keysym_num, events.num, events.send_event, events.serial, events.state, events.time, events.type, events.widget, events.width, events.x, events.x_root, events.y, events.y_root
            
    def _insertCelula(self, row, col, unique_id, width, value="", **cnf):
        cel = tk.Label(self.frameCelulas, width=width, text=value, cnf=cnf)
        cel.grid(row=row, column=col)
        cel.unique_id = unique_id
        return cel

    def _addBinds(self, celula):
        for bindKeyStr in self.bindLine.dictFunctions:
            celula.bind(bindKeyStr, self.bindLine.dictFunctions.get(bindKeyStr))
            
    class bindLine:
	dictFunctions = {}
	def __init__(self, string, myFunction):
		self.string = string
		self.myFunction = myFunction
		self.dictFunctions[string] = self._funcao
                
	def _funcao(self, events):
		unique_id = events.widget.unique_id
                #print events, unique_id
		self.myFunction(events, unique_id)
        
    def selectRow(self, events, unique_id):
        self._unique_id_selected = unique_id#events.widget.unique_id
        widget = events.widget
        self.selectRowByNumberLine(widget = widget, line = int(widget.grid_info().get("row")) )
            
    def selectRowByNumberLine(self, widget, line):
        widgetsInLine = widget.grid_info().get("in").grid_slaves(row=line)
        self._diselectLastWidgets()#Se nao for a primeira selecao, diselecione os ultimos widgets selecionados
        self.selectWidgets(widgetsInLine)
        
    
    def getIdSelected(self):#Retorna o id retornado por selectRow
        return self._unique_id_selected
        
    def selectWidgets(self, widgets):
        for widget in widgets:
            widget.config(background="#008B8B")
        self._lastWidgetsSelecteds = widgets
            
    def _diselectLastWidgets(self):
        if self._lastWidgetsSelecteds:
            for widget in self._lastWidgetsSelecteds:
                widget.config(background=self._colorBgPatern)

if __name__ == "__main__":
    global datas_
    def action():
        table.configHeader((("numero", 15), ("nome completo", 40), ("idade",10)))
    def actionChangeCanvasSize():
        table.configSize(100, 700)

    def windowEdit(master, unique_id):
        global nomeVar, idadeVar
        window = tk.Toplevel(master)
        window.resizable(False, False)
        #window.attributes("-topmost", 1)
        window.transient(master)
        frame = tk.Frame(window)
        frame.pack(padx=20, pady=20)
        nomeVar = tk.StringVar()
        tk.Label(frame, text="Nome").grid(row=0, column=0)
        tk.Entry(frame, textvariable=nomeVar).grid(row=0, column=1)

        idadeVar = tk.StringVar()
        tk.Label(frame, text="Idade").grid(row=1, column=0)
        tk.Entry(frame, textvariable=idadeVar).grid(row=1, column=1)
        setDatas(unique_id)
        
    def setDatas(unique_id):
        data = datas_.get(str(unique_id))        
        nomeVar.set(data.get("nome"))
        idadeVar.set(data.get("idade"))
        
    def callWindowEdit(events, unique_id):
        #print "callWindowEdit Chamado"
        windowEdit(window, table.getIdSelected())
        
    window = tk.Tk()
    window.title("Tabela")
    window.geometry("1050x550+250+100")
    table = Table(window, (("id", 8), ("nome", 40), ("idade",10)), background="green", relief=tk.RIDGE)
    
    table.bindLine("<Button-1>", table.selectRow)
    table.bindLine("<Button-3>", callWindowEdit)
    
    table.insertRow(unique_id=5, elements={"id": "5", "nome": "Alguma pessoa", "idade":"18"})
    table.insertRow(unique_id=12, elements={"id": "12", "nome": "Fulano", "idade":"15"})
    table.insertRow(unique_id=14, elements={"id": "14", "nome": "Ciclano", "idade":"22"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    table.insertRow(unique_id=18, elements={"id": "18", "nome": "Beltrano", "idade":"26"})
    

    datas_ ={"5":{"nome": "Alguma pessoa", "idade":"18"},
    "12":{"nome": "Fulano", "idade":"15"},
    "14":{"nome": "Ciclano", "idade":"22"},
    "18":{"nome": "Beltrano", "idade":"26"}}
        
    table.pack(fill="both", expand=True, padx=10, pady=10)

    
    tk.Button(window, text="Change Header", command=action).pack()
    tk.Button(window, text="Change Size Canvas", command=actionChangeCanvasSize).pack()
    window.mainloop()
