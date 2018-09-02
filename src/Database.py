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
        self.execute = self.cursor.execute
        self.fetchall = self.cursor.fetchall
        self.fetchone = self.cursor.fetchone
        
    def _createDatabase(self):
        try:
            self.execute("""CREATE TABLE livros (
            id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            nome  VARCHAR ( 80 ) NOT NULL,
            autor VARCHAR ( 80 ),
            ano   INTEGER ( 4 ),
            categoria VARCHAR ( 80 ),
            total_paginas INTEGER ( 4 ),
            pagina_pausada    INTEGER ( 4 ),
            inicio_leitura    INTEGER ( 2 ),
            caminho_imagem    TEXT
        );""")

            self.db.commit()
            return True
        except: return False


    def getRecordsDb(self, columns_str="", id_record=None):

        if id_record:
            query = "SELECT {} FROM livros WHERE id={}".format(columns_str, id_record)
            self.execute(query)
            result = self.cursor.fetchall()[0]
        else:
            query = "SELECT {} FROM livros".format(columns_str)
            self.execute(query)
            result = self.cursor.fetchall()
        return result
    
    def getAmountBooksDb(self):
        self.execute("SELECT COUNT(nome) FROM livros")
        return self.fetchone()[0]

    def getTotalPagesContentDb(self):
        query = "select sum(total_paginas - inicio_leitura) from livros"
        self.execute(query)
        return self.fetchone()[0]

    def getTotalPagesReadDb(self):
        query = "select sum(pagina_pausada - inicio_leitura) from livros"
        self.execute(query)
        return self.fetchone()[0]

    def getTotalPagesNotReadDb(self):
        query = "select sum(total_paginas - pagina_pausada - inicio_leitura) from livros"
        self.execute(query)
        return self.fetchone()[0]
    
    def createRecordDb(self, book_name, total_pages=0, summary_end_page=0, read_pages=0):
        query = "INSERT INTO livros(nome, total_paginas, pagina_pausada, inicio_leitura) VALUES('{}',{},{},{})".format(book_name, total_pages, summary_end_page, read_pages)
        try:
            self.execute(query.decode("windows-1252"))
            self.db.commit()
            return True
        except Exception("Erro ao inserir registro no banco de dados"):
            print query
            return False

    def getCategoriesAmountDb(self):
        query = "select categoria, count(*) from livros group by categoria order by count(*) desc"
        self.execute(query)
        return self.fetchall()

    def getPercentReadBooksDb(self, book_id):
        if book_id:
            query = """select id, nome, 
            ((100*(pagina_pausada-inicio_leitura)) / (total_paginas-inicio_leitura)) as porcentagem_lida from livros
             where id = {}
             order by porcentagem_lida desc
            """.format(book_id)
        else:
            query = """select id, nome, 
            ((100*(pagina_pausada-inicio_leitura)) / (total_paginas-inicio_leitura)) as porcentagem_lida from livros
             order by porcentagem_lida desc
            """

        self.execute(query)
        return self.fetchall()

    def getPercentReadCategoriesDb(self, category):
        if category:
            query = """select sum(pagina_pausada - inicio_leitura) as paginas_lidas, categoria,
(sum(pagina_pausada - inicio_leitura) * 100) / sum(total_paginas - inicio_leitura) as porcentagem_lida
 from livros group by categoria order by paginas_lidas desc"""

        else:
            query = """select sum(pagina_pausada - inicio_leitura) as paginas_lidas, categoria,
(sum(pagina_pausada - inicio_leitura) * 100) / sum(total_paginas - inicio_leitura) as porcentagem_lida
 from livros where categoria='{}'' group by categoria order by paginas_lidas desc""".format(category)

        self.execute(query)
        return self.fetchall()
        
        
    def close(self):
        self.db.close()



	    
if __name__ == "__main__":
    db = DatabaseBooks()
    
    #print sys._getframe(1).f_lineno
    
    print ("Conexão bem sucessida")
    #print ("{} registros encontrados.".format(len(db.getRecords())))
