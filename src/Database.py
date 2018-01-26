# -*- coding: Latin-1 -*-
import sqlite3
import os

class DatabaseBooks(object):
    def __new__(self):
        if not hasattr(DatabaseBooks, "_instance"): self._instance = super(DatabaseBooks, self).__new__(self)
        return self._instance
    
    def __init__(self):
        print os.getcwd()
        self.db = sqlite3.connect("Database/Books.db")
        self.cursor = self.db.cursor()
        self._createDatabase()
        
    def _createDatabase(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(80), total_paginas INTEGER(4), paginas_lidas INTEGER(4), inicio_leitura INTEGER(2))")
            self.db.commit()
            return True
        except: return False


    def getRecords(self, id_record=None):
        
        if id_record:
            query = "SELECT * FROM livros WHERE id={}".format(id_record)
            self.cursor.execute(query)
            result = self.cursor.fetchall()[0]
        else:
            query = "SELECT * FROM livros"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        return result
    
    def getSizeRecords(self):
        self.cursor.execute("SELECT COUNT(nome) FROM livros")
        return self.cursor.fetchall()[0][0]
    
    def createRecord(self, book_name, total_pages=0, summary_end_page=0, read_pages=0):
        query = "INSERT INTO livros(nome, total_paginas, pagina_pausada, inicio_leitura) VALUES('{}',{},{},{})".format(book_name, total_pages, summary_end_page, read_pages)
        try:
            self.cursor.execute(query.decode("windows-1252"))
            self.db.commit()
            return True
        except Exception("Erro ao inserir registro no banco de dados"):
            print query
            return False
        
        
    def close(self):
        self.db.close()



	    
if __name__ == "__main__":
    db = DatabaseBooks()
    
    #print sys._getframe(1).f_lineno
    
    print ("Conexão bem sucessida")
    #print ("{} registros encontrados.".format(len(db.getRecords())))
