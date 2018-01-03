# -*- coding: Latin-1 -*-
import sqlite3
import unittest

class DatabaseBooks(object):
    def __new__(self):
        if not hasattr(DatabaseBooks, "_instance"): self._instance = super(DatabaseBooks, self).__new__(self)
        return self._instance
    
    def __init__(self):
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


class TestStringMethods(unittest.TestCase):

    def test_database_create(self):
        self.db = DatabaseBooks()
        self.assertTrue(self.db._createDatabase())
        print "Processo de criação de banco de dados funcionando"
        
    def test_records(self):
        self.db = DatabaseBooks()
        self.assertTrue(self.db.getRecords())

    def test_size(self):
        self.db = DatabaseBooks()
        self.assertEqual(43, self.db.getSizeRecords())
        print "O banco de dados assume 43 registros como esperado"
        
    def test_field(self):
        self.db = DatabaseBooks()
        self.assertEqual(u'marketing na era digital'.lower(), self.db.getRecords(id_record=26)[1])
        print "O livro com id 26 foi testado e foi retornado com sucesso"

    def test_create_book(self):
        testar = False
        if testar:
            self.db = DatabaseBooks()
            self.assertTrue(self.db.createRecord("Meu livro", 420, 12))
            print "O metodo createRecord criou registro 'Meu livro' com sucesso"
        else: print "Teste de criação de livro não realizado"
        

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        #with self.assertRaises(TypeError):
            #s.split(2)
	    
if __name__ == "__main__":
    unittest.main()
    #db = DatabaseBooks()
    #test(db.getRecords(0))
    #print sys._getframe(1).f_lineno
    
    #print ("Conexão bem sucessida")
    #print ("{} registros encontrados.".format(len(db.getRecords())))
