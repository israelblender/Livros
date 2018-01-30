# -*- coding: Latin-1 -*-
__author__ = "Israel"
__date__ = "$30/12/2017 21:54:12$"

import Tkinter as tk
from collections import namedtuple

class BindTable:
    """Configurar funcao para bind necessitando de dois parametros na funcao de callback:\n\tdef funcao(events, unique_id)"""
    dictFunctions = {}
    def __init__(self, string, myFunction, type="only", action=""): #type pode ser only ou all para ser acionado de qualquer widget
        self.string = string
        self.myFunction = myFunction
        self.dictFunctions[string] = self._subFunction, type, action
        self.action = action
        
    def _subFunction(self, events):
        unique_id = None
        if not self.action: #Se action for nulo
            unique_id = events.widget.unique_id
        else: #Se action for up ou down
            if self.action == "up":
                unique_id_ = Table.frameCelulas.grid_slaves(row=Table.rowCurrent-1, column=0)[0].unique_id
                unique_id = unique_id_
            elif self.action == "down":
                unique_id_ = Table.frameCelulas.grid_slaves(row=Table.rowCurrent+1, column=0)[0].unique_id
                unique_id = unique_id_
            
        self.myFunction(events, unique_id)
                
class Binds:
    """Retem todas as binds registradas na table"""
    def __init__(self): pass
    def _delBinds(self, widget):
        for bindKeyStr in BindTable.dictFunctions:
            if not BindTable.dictFunctions.get(bindKeyStr)[1] == "all":
                widget.unbind_all(bindKeyStr)#, BindTable.dictFunctions.get(bindString))
    
    def _addBinds(self, widget):
        for bindKeyStr in BindTable.dictFunctions:
            widget.bind_all(bindKeyStr, BindTable.dictFunctions.get(bindKeyStr)[0])
    
class Table(object, tk.Frame, Binds):
    """Widget para gerar tabela numa Gui
    Funcoes principais:
    
    """
    _idBindMouse = None
    frameCelulas = []
    canvas = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(Table, "_instance"):
                cls._instance = super(Table, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self, master, headers, **kwargs):
        tk.Frame.__init__(self, master, cnf=kwargs)
        Binds.__init__(self)
        #BindTable.__init__(self)
        Table.bind = BindTable
        frameCanvasScrolly = tk.Frame(self)
        frameCanvasScrolly.pack(side=tk.TOP, fill="both", expand=True)
        Table.canvas = self.canvas = canvas = tk.Canvas(master = frameCanvasScrolly, scrollregion=(0, 0, 1100, 1000), background="#CAE1FF")
        
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        canvas.bind_all("<Motion>", self.activeBind)#acionado quando entra no widget table
        canvas.bind("<Leave>", self.deactiveBind)#acionado quando sai do widget table
        
        Table.frameCelulas = tk.Frame(canvas)
        #BindTable.reportWidgetEvent(Table.frameCelulas)
        canvas.create_window(0, 0, window=Table.frameCelulas, anchor=tk.NW)

        self.scrolly = scrolly = tk.Scrollbar(frameCanvasScrolly, orient=tk.VERTICAL, command=canvas.yview)
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
            
    def configHeader(self, headers):
        self.headers = headers
        self.infoSizeCols = dict(headers)
        self.dict_idname_colname = {}
        self.dict_idname_index = {}
        for index, elem in enumerate(headers):
            self.dict_idname_colname[index] = elem[0], elem[1][0]
            self.dict_idname_index[elem[0]] = index
        self.insertLine(-1, self.dict_idname_colname, "header")
        
    def mouseWheelEvent(self, event, unique_id):
        if event.delta < 0: #Move para cima
            self.canvas.yview_scroll(1, tk.UNITS)
        elif event.delta > 0: #Move para baixo
            self.canvas.yview_scroll(-1, tk.UNITS)
    
    def updateRegion(self):#Atualiza a região para que o scroll se encaixe no quadro da tabela
        Table.frameCelulas.update()
        self.canvas.config(scrollregion=(0, 0, Table.frameCelulas.winfo_width(), Table.frameCelulas.winfo_height()))#Atualiza scroll x e y para o tamanho da tabela
        
    def configSize(self, width, height):
        self.config(width=width, height=height)#Muda tamanho do frame Table
        #self.canvas.config(width=width, height=height)
        
    def configColors(self, bg, bg_header):
        self._colorBgPatern = bg
        self._colorBgHeader = bg_header
    
    def insertRow(self, unique_id, elements):
        if len(elements) != len(self.infoSizeCols):
            raise Exception("Erro", u"A quantidade de elementos informados nao e igual a quantidade registrada!")
        return self.insertLine(unique_id, elements, "cel")
    
    def insertLine(self, unique_id, elements, type):
        col = 0
        
        if type == "cel":
            for index in range(len(elements)):
                idname = self.dict_idname_colname.get(index)[0]

                cel = self._insertCelula(row=self.row, col=col, 
                    unique_id = unique_id, 
                    width = self.infoSizeCols.get(idname)[1],
                    value = elements.get(idname),
                    background=self._colorBgPatern)
                self._addBinds(widget=cel)
                col += 1
        elif type == "header":
            for index in range(len(elements)):
                idname = self.dict_idname_colname.get(index)[0]
                
                self._insertCelula(row=0, col=col, 
                        unique_id = unique_id, 
                        width = self.infoSizeCols.get(idname)[1],
                        value = self.dict_idname_colname.get(index)[1],
                        relief=tk.GROOVE,
                        background=self._colorBgHeader)
                col += 1
        self.row += 1
    
    def _insertCelula(self, row, col, unique_id, width, value="", **cnf):
        cel = tk.Label(Table.frameCelulas, width=width, text=value, cnf=cnf)
        cel.grid(row=row, column=col)
        cel.unique_id = unique_id
        cel.widgetName = "table"
        return cel
        
    def selectRowEvent(self, events, unique_id):
        self._unique_id_selected = unique_id#events.widget.unique_id
        print "UNIQUEID: ", unique_id
        widget = events.widget
        #self.rowSelected = widget.grid_info().get("row")
        self.selectRowByNumberLine(row = int(widget.grid_info().get("row")) )
    
    def selectPreviousRowEvent(self, events, unique_id=None):
        """Função para selecionar a linha antecessora acima acionada por um evento"""
        self._unique_id_selected = unique_id
        print "UNIQUEID: ", unique_id
        self.selectRowByNumberLine( row = Table.rowCurrent - 1 )
        
    def selectNextRowEvent(self, events, unique_id=None):
        """Função para selecionar a proxima linha abaixo acionada por um evento"""
        self._unique_id_selected = unique_id
        print "UNIQUEID: ", unique_id
        self.selectRowByNumberLine( row = Table.rowCurrent + 1 )
    
    def selectRowByNumberLine(self, row):

        #widgetsInLine = widget.grid_info().get("in").grid_slaves(row=row)
        self._diselectLastWidgetsBackgroundColors() #Se nao for a primeira selecao, diselecione os ultimos widgets selecionados
        Table.rowCurrent = row # Obtem a linha atual
        widgetsInLine = Table.frameCelulas.grid_slaves(row=row)# Widgets presentes nessa linha
        self._selectCurrentWidgetsBackgroundColors(widgetsInLine)
        self._unique_id_selected = widgetsInLine[0].unique_id
    
    def getIdSelected(self):#Retorna o id retornado por selectRow
        return self._unique_id_selected
    def getRowCurrent(self):#Retorna a linha selecionada atualmente
        try: 
            return Table.rowCurrent
        except: print "CALL selectRowByNumberLine(row=?) FUNCTION!"
        
    def _selectCurrentWidgetsBackgroundColors(self, widgets):
        for widget in widgets:
            widget.config(background="#008B8B")
        self._lastWidgetsSelecteds = widgets
            
    def _diselectLastWidgetsBackgroundColors(self):
        if self._lastWidgetsSelecteds:
            for widget in self._lastWidgetsSelecteds:
                widget.config(background=self._colorBgPatern)
    
    def activeBind(self, event):
        if hasattr(event.widget, "widgetName") and event.widget.widgetName == "table":
            if not self._idBindMouse:
                #self._idBindMouse = self.canvas.bind_all("<MouseWheel>", self.mouseWheelEvent)                
                self._addBinds(widget = self.canvas)
    def deactiveBind(self, event):
        self._delBinds(widget = self.canvas)
        #self.canvas.unbind_all("<MouseWheel>")
        self._idBindMouse = None

if __name__ == "__main__":
    global datas_
    def action():
        table.configHeader((("number", "numero", 15), ("name", "nome completo", 40), ("old","old",10)))
    def actionChangeCanvasSize():
        table.configSize(100, 700)

    def windowEdit(master, position, unique_id):
        global nomeVar, idadeVar
        window = tk.Toplevel(master)
        window.resizable(False, False)
        #print dir(window), window.winfo_screenwidth(), 
        
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
        
        window.update()
        window.geometry(str(window.winfo_width())+"x"+str(window.winfo_height())+"+"+str(position[0])+"+"+str(position[1]))
        setDatas(unique_id)
        
    def setDatas(unique_id):
        
        data = datas_.get(str(unique_id))    
        nomeVar.set(data.get("name"))
        idadeVar.set(data.get("old"))
        
    def callWindowEditEvent(events, unique_id):
        #print dir(events)
        print events.x, events.y, events.x_root, events.y_root
        windowEdit(window, (events.x_root, events.y_root), table.getIdSelected())
        
    window = tk.Tk()
    window.title("Tabela")
    window.geometry("1050x550+250+100")
    table = Table(window, (("id", ("id", 8)), ("name", ("nome", 40)), ("old", ("idade",10))), background="green", relief=tk.RIDGE)
    
    table.bind("<Button-1>", table.selectRowEvent)
    table.bind("<Button-3>", callWindowEditEvent)
    
    table.insertRow(unique_id=5, elements={"id": "5", "name": "Alguma pessoa", "old":"18"})
    table.insertRow(unique_id=12, elements={"id": "12","name": "Fulano","old":"15"})
    table.insertRow(unique_id=14, elements={"id": "14","name": "Ciclano","old":"22"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.insertRow(unique_id=18, elements={"id": "18","name": "Beltrano","old":"26"})
    table.updateRegion()
    #table.bind("<Up>", table.selectPreviousRowEvent)
    table.bind("<Up>", table.selectPreviousRowEvent, "only", action="up")
    table.bind("<Down>", table.selectNextRowEvent, "only", action="down")

    datas_ ={"5":{"name": "Alguma pessoa","old":"18"},
    "12":{"name": "Fulano","old":"15"},
    "14":{"name": "Ciclano","old":"22"},
    "18":{"name": "Beltrano","old":"26"}}
        
    table.pack(fill="both", expand=True, padx=10, pady=10)

    
    tk.Button(window, text="Change Header", command=action).pack()
    tk.Button(window, text="Change Size Canvas", command=actionChangeCanvasSize).pack()
    window.mainloop()
