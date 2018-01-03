# -*- coding: Latin-1 -*-
__author__ = "Israel"
__date__ = "$30/12/2017 21:54:12$"

import Tkinter as tk

class Table(object, tk.Frame):
    def __new__(cls, *args, **kwargs):
        return super(Table, cls).__new__(cls, *args, **kwargs)

    def __init__(self, master, headers):
        tk.Frame.__init__(self, master)
        self.master = master
        self.row = 0
        self.infoSizeCols = None
        #print headers
        self.headers = headers
        self.infoSizeCols = dict(headers)
        
        self.insertLine(headers, "header")
        
    
    def insertRow(self, elements):
        if len(elements[0]) != len(self.infoSizeCols):
            raise Exception("Erro", u"A quantidade de elementos informados nao e igual a quantidade registrada!")
        return self.insertLine(elements, "cel")

    def insertLine(self, elements, type):
        if type=="header": #recebe lista de dois elementos em cada elemento
            self._insertCelulasByElement(elements)
        elif type=="cel":#recebe uma lista com apenas 
            self._insertCelulasByElement(elements, relief=tk.GROOVE)
        self.row += 1
        
    def _insertCelulasByElement(self, elements, **kwargs):
        col = 0
        for elem in elements:
            self._insertCelula(row=self.row, col=col, width=self.infoSizeCols.get(col_name), value=elements.get(col_name), **kwargs)
            col += 1
        
    def _insertCelula(self, row, col, width, value="", **cnf):
        print "\n", row, col, width, value#, type(row), type(col), type(width), type(value)
        cel = tk.Label(self, width=width, text=value, cnf=cnf)
        cel.grid(row=row, column=col)
        return cel
                
    
        
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Tabela")
    
    window.geometry("700x400+250+150")
    
    #gui = Table(window, ("id", 8),("nome", 30),("idade", 10))
    gui = Table(window, {"id": 8, "nome": 30, "idade":10})
    
    gui.insertRow({"id": "5", "nome": "Alguma pessoa", "idade":"18"})
    gui.insertRow({"id": "12", "nome": "Fulano", "idade":"15"})
    gui.insertRow({"id": "14", "nome": "Ciclano", "idade":"22"})
    
    gui.pack(side=tk.TOP, expand=True)
    window.mainloop()