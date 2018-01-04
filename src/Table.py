# -*- coding: Latin-1 -*-
__author__ = "Israel"
__date__ = "$30/12/2017 21:54:12$"

import Tkinter as tk
from collections import namedtuple

class Table(object, tk.Frame):
    def __new__(cls, *args, **kwargs):
        return super(Table, cls).__new__(cls, *args, **kwargs)

    def __init__(self, master, headers):
        tk.Frame.__init__(self, master)
        self.master = master
        self.row = 0
        #self._bindStringDict = {}#1: "<Button-1>", 2: "<Button-2>", 3: "<Button-3>"}
        self.bindList = {}
        self._lastWidgetsSelecteds = None
        self.ColunasBind = namedtuple("ColunasBind", "string,function")

        self.configColors(bg="#B4CDCD")
        self.configHeader(headers)
        
    
    def configHeader(self, headers):
        self.headers = headers
        self.infoSizeCols = dict(headers)
        self.dict_headers = {}
        for index, elem in enumerate(headers):
            self.dict_headers[index] = elem[0]
        self.insertLine(-1, self.dict_headers, "header")

    def configColors(self, bg):
        self._colorBgPatern = bg
        
    
    def insertRow(self, unique_id, elements):
        
        #print elements, self.infoSizeCols
        if len(elements) != len(self.infoSizeCols):
            raise Exception("Erro", u"A quantidade de elementos informados nao e igual a quantidade registrada!")
        return self.insertLine(unique_id, elements, "cel")

    def insertLine(self, unique_id, elements, type):
        self._insertCelulasByElement(unique_id, elements, type)
        self.row += 1
        
    def _insertCelulasByElement(self, unique_id, cols_values, type):
        col = 0
        if type == "cel":
            for index in range(len(cols_values)):
                col_key = self.dict_headers.get(index)
                cel = self._insertCelula(row=self.row, col=col, 
                    unique_id = unique_id, 
                    width = self.infoSizeCols.get(col_key),
                    value = cols_values.get(col_key))
                self._addBinds(cel)
                col += 1
        elif type == "header":
            for index in range(len(cols_values)):
                col_key = self.dict_headers.get(index)
                self._insertCelula(row=0, col=col, 
                        unique_id = unique_id, 
                        width = self.infoSizeCols.get(col_key),
                        value = self.dict_headers.get(index), relief=tk.GROOVE)
                
                col += 1
    
    def _addBinds(self, celula):
        #print "BINDLIST da funcao _insertBind: {}".format(self.getBinds())
        for bindKeyStr in self.bindList:
            #print "Bind", bind.string, "inserido"
            celula.bind(bindKeyStr, self.bindList.get(bindKeyStr))
            #print type(celula), window._w, str(celula)
            #window.tk.call('bind', str(celula), "<Button-1>", self.teste)

    #def _bindFunction(self, events):
        
        #unique_id = events.widget.unique_id
        #print events.char, events.delta, events.height, events.keycode, events.keysym, events.keysym_num, events.num, events.send_event, events.serial, events.state, events.time, events.type, events.widget, events.width, events.x, events.x_root, events.y, events.y_root
        #self._bindStringDict.get(events.num)
        #self._bfunc(events, unique_id)
        
    #def getBinds(self):
        #return self.bindList
        
    def _insertCelula(self, row, col, unique_id, width, value="", **cnf):
        #print "\n", row, col, width, value#, type(row), type(col), type(width), type(value)
        cel = tk.Label(self, width=width, text=value, background=self._colorBgPatern, cnf=cnf)
        cel.grid(row=row, column=col)
        cel.unique_id = unique_id
        return cel
    
    def bindLine(self, str_type, function):
        #print "Bind adicionado"
        self.bindList[str_type] = function#Adiciona o bind a lista de binds
        #print "BINDLIST: {}".format(self.bindList)
        
    def selectRow(self, events):
        #unique_id = events.widget.unique_id
        #print dir(events.widget)
        widget = events.widget
        widgetsInLine = widget.grid_info().get("in").grid_slaves(row=int(widget.grid_info().get("row")))
        
        self.diselectLastWidgets()#Se nao for a primeira selecao, diselecione os ultimos widgets selecionados
        self.selectWidgets(widgetsInLine)
        
    def selectWidgets(self, widgets):
        for widget in widgets:
            widget.config(background="#008B8B")
        self._lastWidgetsSelecteds = widgets
            
    def diselectLastWidgets(self):
        if self._lastWidgetsSelecteds:
            for widget in self._lastWidgetsSelecteds:
                widget.config(background=self._colorBgPatern)

    def _selectLine(self, row):
        
        pass
    
    




if __name__ == "__main__":
    def action():
        gui.configHeader((("numero", 15), ("nome completo", 40), ("idade",10)))
        
    def clickCel(events):
        unique_id = events.widget.unique_id
        print "ClickCel precionado"
        print unique_id
        
    window = tk.Tk()
    window.title("Tabela")
    window.geometry("700x400+250+150")
    gui = Table(window, (("id", 8), ("nome", 40), ("idade",10)))
    
    gui.bindLine("<Button-1>", gui.selectRow)
    gui.bindLine("<Button-2>", clickCel)
    gui.bind("<Button-3>", clickCel)
    gui.bindLine("<KeyPress-k>", clickCel)
    
    gui.insertRow(unique_id=5, elements={"id": "5", "nome": "Alguma pessoa", "idade":"18"})
    gui.insertRow(unique_id=12, elements={"id": "12", "nome": "Fulano", "idade":"15"})
    gui.insertRow(unique_id=14, elements={"id": "14", "nome": "Ciclano", "idade":"22"})

    
    
        
    gui.pack(side=tk.TOP, expand=True)
    
    tk.Button(window, text="Change Header", command=action).pack()
    window.mainloop()
