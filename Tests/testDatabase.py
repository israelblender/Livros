# -*- coding: Latin-1 -*-
import unittest

import os
import sys

parent_dir = os.path.dirname(os.getcwd())
sys.path.insert(0, parent_dir)

from src import Database


class TestStringMethods(unittest.TestCase):

    def test_database_create(self):
        self.db = Database.DatabaseBooks()
        self.assertTrue(self.db._createDatabase())
        print u"Processo de criação de banco de dados funcionando"
        
    def test_records(self):
        self.db = Database.DatabaseBooks()
        self.assertTrue(self.db.getRecords())

    def test_size(self):
        self.db = Database.DatabaseBooks()
        self.assertEqual(43, self.db.getSizeRecords())
        print "O banco de dados assume 43 registros como esperado"
        
    def test_field(self):
        self.db = Database.DatabaseBooks()
        self.assertEqual(u'marketing na era digital'.lower(), self.db.getRecords(id_record=26)[1])
        print "O livro com id 26 foi testado e foi retornado com sucesso"

    def test_create_book(self):
        testar = False
        if testar:
            self.db = Database.DatabaseBooks()
            self.assertTrue(self.db.createRecord("Meu livro", 420, 12))
            print "O metodo createRecord criou registro 'Meu livro' com sucesso"
        else: print "Teste de criação de livro não realizado"
        

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        #with self.assertRaises(TypeError):
            #s.split(2)

if __name__ == '__main__':
    #unittest.main()
    db = Database.DatabaseBooks()

