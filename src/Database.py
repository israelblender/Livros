# -*- coding: Latin-1 -*-
import sqlite3
class DatabaseBooks(object):
    def __new__(self):
        if not hasattr(DatabaseBooks, "_instance"): self._instance = super(DatabaseBooks, self).__new__(self)
        return self._instance
    
    def __init__(self):
        self.db = sqlite3.connect("Database/Books.db")
        self.cursor = self.db.cursor()
        self._createDatabase()
        
    def _createDatabase(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(80), total_paginas INTEGER(4), paginas_lidas INTEGER(4), inicio_leitura INTEGER(2))")
        self.db.commit()

    def getRecords(self, id_record=None):
        if id_record:self.cursor.execute("SELECT * FROM books WHERE id={}".format(id_record))
        else: self.cursor.execute("SELECT * FROM livros")
        return self.cursor.fetchall()
    
    def getSizeRecords(self):
        self.cursor.execute("select count(nome) from livros")
        return self.cursor.fetchall()[0][0]
    
    def createRecord(book_name, total_pages=0, summary_end_page=0, read_pages=0):
        query = "INSERT INTO livros(id, nome, total_paginas, paginas_lidas, fim_do_sumario) VALUES('{}',{},{},{})".format(book_name, total_pages, summary_end_page, read_pages)
        self.cursor.execute(query.decode("windows-1252"))
        self.db.commit()
        
    def close(self):
        self.db.close()

if __name__ == "__main__":
    db = DatabaseBooks()
    print ("Conexão bem sucessida")
    print ("{} registros encontrados.".format(len(db.getRecords())))
