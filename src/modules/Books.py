# -*- coding: Utf-8 -*-

from Database import DatabaseBooks
import datetime
from collections import namedtuple

class Books(DatabaseBooks):
    def __init__(self):
        super(Books, self).__init__()
        #self.db = DatabaseBooks()
        self._totalPages = None
        self._totalPagesNotReads = None

    def getAllBooks(self, columns_str):
        "Retorna a informacao completa de todos os livros"
        return self.getRecordsDb(columns_str=columns_str)

    def getBook(self, columns_str, id_record):
        "Retorna a informacao completa do livro"
        return self.getRecordsDb(columns_str=columns_str, id_record=id_record)[0]

    def getTotalPagesReads(self):
        "Retorna o total de paginas lidas"
        return self.getTotalPagesReadDb()
    
    def getTotalPagesContent(self):
        "Retorna o total de paginas com conteudo que podem ser lidas"
        self._totalPages = self.getTotalPagesContentDb()
        return self._totalPages

    def getTotalPagesNotReads(self):
        "Retorna o total de paginas nao lidas"
        print (self.getTotalPagesNotReadDb())
        self._totalPagesNotReads = self.getTotalPagesNotReadDb()
        return self._totalPagesNotReads

    def getTotalBooks(self):
        "Retorna o total de livros registrados"
        self._totalBooks = self.getAmountBooksDb()
        return self._totalBooks

    def getCategoriesAmount(self):
        return self.getCategoriesAmount()

    def getMediaPagesDay(self, total_pages, days):
        "Retorna a media de paginas que devem ser lidas por dia"
        #if total_pages % 2 != 0:  total_pages -= 1
        pagesPerDay = total_pages / days #Total de p�ginas para ler por dia
        totalPagesCheck = days * pagesPerDay#Total de p�ginas para ler em x(number_of_months) meses
        #restDays = total_pages - totalPagesCheck#Resto das p�ginas para realizar a leitura
        return pagesPerDay

    def getCategoriesAmount(self):
        "Retorna quantidade de livros classificados em cada categoria"
        return self.getCategoriesAmountDb()

    def getPercentReadBook(self, book_id):
        "Retorna o percentual de leitura do livro informado"
        return self.getPercentReadBooksDb(book_id)[0]

    def getPercentReadAllBooks(self):
        "Retorna o progresso de todos os livros"
        return self.getPercentBooksDb()

    def getPercentReadCategories(self, category):
        "Retorna o percentual de livros lidos na categoria informada"
        return self.getPercentReadCategoriesDb(category)

    def getPercentReadCategories(self):
        "Retorna o percentual de livros lidos em cada categoria"
        return self.getPercentReadCategoriesDb()

    def updatePagePaused(self, book_id, page_paused):
        "Atualiza a p�gina atual do marcador"
        self.updatePagePausedDb(book_id, page_paused)

    def saveNewBook(self, book_name, author, year, category, total_pages, start_read):
        "Salva um novo livro"
        self.saveNewBookDb(book_name, author, year, category, total_pages, start_read, path="")

    def updateBook(self, book_id, book_name, author, year, category, total_pages, start_read):
        "Atualiza as informa��es do livro existente"
        self.updateBookDb(book_id, book_name, author, year, category, total_pages, start_read, path="")
        


if __name__ == "__main__":
    b = Books()
    
    dt_final = datetime.date(2018, 12, 31)
    days_rest = dt_final - dt_final.today()
    days_rest = days_rest.days
    
    totalBooks = b.getTotalBooks()
    totalPages = b.getTotalPagesContent()
    totalPagesReads = b.getTotalPagesReads()
    totalPagesNotReads = b.getTotalPagesNotReads()
    mediaPagesDay = b.getMediaPagesDay(totalPagesNotReads, days_rest)
    
    print ("""
    Total de livros: \t\t\t{}
    Total de p�ginas com conte�do: \t{}
    Total de p�ginas lidas: \t\t{}
    Total de p�ginas n�o lidas: \t{}
    M�dia de p�ginas em cada livro: \t{:.0f}
    Leia {} p�ginas por dia em {} dias.""".format(
    totalBooks, totalPages, totalPagesReads, totalPagesNotReads, totalPages/totalBooks, int(mediaPagesDay), days_rest))
    try: input("\n\nPrecione qualquer tecla para sair")
    except: pass
