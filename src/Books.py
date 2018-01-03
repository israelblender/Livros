# -*- coding: Latin-1 -*-

from Database import DatabaseBooks
import datetime

class Books(DatabaseBooks):
    def __init__(self):
        super(Books, self).__init__()
        #self.db = DatabaseBooks()
        self.books = self.getRecords()
        self._totalPages = None
        self._totalPagesNotReads = None

    def getTotalPagesReads(self):
        if not self._totalPages: self._totalPages = self.getTotalPages()
        if not self._totalPagesNotReads: self.getTotalPagesNotReads()
        return self._totalPages - self._totalPagesNotReads
    
    def getTotalPages(self):
        self._totalPages = sum([element[2]-element[4] for element in self.books])
        return self._totalPages

    def getTotalPagesNotReads(self):
        self._totalPagesNotReads = sum([element[2]-element[3]-element[4] for element in self.books])
        return self._totalPagesNotReads

    def getTotalBooks(self):
        self._totalBooks = self.getSizeRecords()
        return self._totalBooks

    def getMediaPagesDay(self, totalPages, days):
        if totalPages % 2 != 0:  totalPages -= 1
        pagesPerDay = totalPages / days #Total de p�ginas para ler por dia
        totalPagesCheck = days * pagesPerDay#Total de p�ginas para ler em x(number_of_months) meses
        #restDays = totalPages - totalPagesCheck#Resto das p�ginas para realizar a leitura
        return pagesPerDay

if __name__ == "__main__":
    b = Books()
    
    dt_final = datetime.date(2018, 12, 31)
    days_rest = dt_final - dt_final.today()
    days_rest = days_rest.days
    
    totalBooks = b.getTotalBooks()
    totalPages = b.getTotalPages()
    totalPagesReads = b.getTotalPagesReads()
    totalPagesNotReads = b.getTotalPagesNotReads()
    mediaPagesDay = b.getMediaPagesDay(totalPagesNotReads, days_rest)
    
    print ("""
    Total de livros: \t\t\t{}
    Total de p�ginas sem sum�rios: \t{}
    Total de p�ginas lidas: \t\t{}
    Total de p�ginas n�o lidas: \t{}
    M�dia de p�ginas em cada livro: \t{:.0f}
    Leia {} p�ginas por dia em {} dias.""".format(
    totalBooks, totalPages, totalPagesReads, totalPagesNotReads, totalPages/totalBooks, int(mediaPagesDay), days))
    try: input("\n\nPrecione qualquer tecla para sair")
    except: pass
