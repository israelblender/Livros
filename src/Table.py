# -*- coding: Latin-1 -*-
__author__ = "Israel"
__date__ = "$30/12/2017 21:54:12$"

import Tkinter as tk
from collections import namedtuple
            
class Bind:
    """Configurar funcao para bind necessitando de dois parametros na funcao de callback:\n\tdef funcao(events, unique_id)"""
    dictFunctions = {}
    def __init__(self, string, myFunction, type="only"): #type pode ser only ou all para ser acionado de qualquer widget
            self.string = string
            self.myFunction = myFunction
            self.dictFunctions[string] = self._subFunction, type

    def _subFunction(self, events):
            #unique_id = events.widget.unique_id
            unique_id = Table.frameCelulas
            #print events, unique_id
            self.myFunction(events, unique_id)
                
class Binds:
    """Retem todas as binds registradas na table"""
    def __init__(self): pass
    def _delBinds(self, widget):
        for bindKeyStr in Bind.dictFunctions:
            if not Bind.dictFunctions.get(bindKeyStr)[1] == "all":
                widget.unbind_all(bindKeyStr)#, Bind.dictFunctions.get(bindString))
    
    def _addBinds(self, widget):
        for bindKeyStr in Bind.dictFunctions:
            widget.bind_all(bindKeyStr, Bind.dictFunctions.get(bindKeyStr)[0])

class Table(object, tk.Frame, Binds):
    _idBindMouse = None
    frameCelulas = []
    canvas = None
    def __new__(cls, *args, **kwargs):
        if not hasattr(Table, "_instance"):
                cls._instance = super(Table, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def activeBind(self, event):
        if hasattr(event.widget, "widgetName") and event.widget.widgetName == "table":
            if not self._idBindMouse:
                #self._idBindMouse = self.canvas.bind_all("<MouseWheel>", self.mouseWheelEvent)                
                self._addBinds(widget = self.canvas)
    def deactiveBind(self, event):
        self._delBinds(widget = self.canvas)
        #self.canvas.unbind_all("<MouseWheel>")
        self._idBindMouse = None
        
    def __init__(self, master, headers, **kwargs):
        tk.Frame.__init__(self, master, cnf=kwargs)
        Binds.__init__(self)
        #Bind.__init__(self)
        Table.bind = Bind
        frameCanvasScrolly = tk.Frame(self)
        frameCanvasScrolly.pack(side=tk.TOP, fill="both", expand=True)
        Table.canvas = self.canvas = canvas = tk.Canvas(master = frameCanvasScrolly, scrollregion=(0, 0, 1100, 1000), background="#CAE1FF")
        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        canvas.bind_all("<Motion>", self.activeBind)#acionado quando entra no widget table
        canvas.bind("<Leave>", self.deactiveBind)#acionado quando sai do widget table
        
        self.frameCelulas = tk.Frame(canvas)
        canvas.create_window(0, 0, window=self.frameCelulas, anchor=tk.NW)

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
    
    def _updateRegion(self):#Atualiza a região para que o scroll se encaixe no quadro da tabela
        self.frameCelulas.update()
        self.canvas.config(scrollregion=(0, 0, self.frameCelulas.winfo_width(), self.frameCelulas.winfo_height()))#Atualiza scroll x e y para o tamanho da tabela
        
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
        
    #def _bindFunction(self, events):
        #print events.char, events.delta, events.height, events.keycode, events.keysym, events.keysym_num, events.num, events.send_event, events.serial, events.state, events.time, events.type, events.widget, events.width, events.x, events.x_root, events.y, events.y_root
    
    def _insertCelula(self, row, col, unique_id, width, value="", **cnf):
        cel = tk.Label(self.frameCelulas, width=width, text=value, cnf=cnf)
        cel.grid(row=row, column=col)
        cel.unique_id = unique_id
        cel.widgetName = "table"
        return cel
        
    def selectRowEvent(self, events, unique_id):
        self._unique_id_selected = unique_id#events.widget.unique_id
        widget = events.widget
        self.selectRowByNumberLine(row = int(widget.grid_info().get("row")) )
    
    def selectPreviousRowEvent(self, events, unique_id=None):
        """
        Função para selecionar a linha antecessora acima acionada por um evento
        """
        self._unique_id_selected = unique_id
        self.selectRowByNumberLine( row = self.rowCurrent - 1 )
        
    def selectNextRowEvent(self, events, unique_id=None):
        """
        Função para selecionar a proxima linha abaixo acionada por um evento
        """
        self._unique_id_selected = unique_id
        self.selectRowByNumberLine( row = self.rowCurrent + 1 )
    
    def selectRowByNumberLine(self, row):
        #widgetsInLine = widget.grid_info().get("in").grid_slaves(row=row)
        widgetsInLine = self.frameCelulas.grid_slaves(row=row)
        self._diselectLastWidgetsBackgroundColors()#Se nao for a primeira selecao, diselecione os ultimos widgets selecionados
        self.rowCurrent = row#self.getRowNumber(widgetsInLine)
        self._selectCurrentWidgetsBackgroundColors(widgetsInLine)
    
    def getIdSelected(self):#Retorna o id retornado por selectRow
        return self._unique_id_selected
        
    def _selectCurrentWidgetsBackgroundColors(self, widgets):
        for widget in widgets:
            widget.config(background="#008B8B")
        self._lastWidgetsSelecteds = widgets
            
    def _diselectLastWidgetsBackgroundColors(self):
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
    
    table.Bind("<Button-1>", table.selectRow)
    table.Bind("<Button-3>", callWindowEdit)
    
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
