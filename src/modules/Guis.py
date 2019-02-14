# -*- coding: Utf-8 -*-

#Todas as classes de interface
from Tkinter import *
from ttk import Button as TButton, Progressbar, Separator
import tkMessageBox as tkmsg
from datetime import datetime, date
from modules.Datepicker import Datepicker
from modules.Popuphelp import PopupHelp

def getDaysRest(date_final_dict):#Calcula a quantidade de dias que faltam para ler com base na data recebida
        try: dt_final = date(year=date_final_dict.get("year"), month=date_final_dict.get("month"), day=date_final_dict.get("day"))
        except ValueError:
            date_final_dict["day"] -= 1
            return getDaysRest(date_final_dict)
        
        days_rest = dt_final - dt_final.today()
        days_rest = days_rest.days
        return days_rest


class PageMarkerGui:
	def __init__(self, master, book, id_line_selected, x=0, y=0):
		self.book = book
		self.id_line_selected = id_line_selected

		if master:
			topwindow = Toplevel(master)
			topwindow.title("Marcador de página")
        	topwindow.geometry("+{}+{}".format(x, y))
	        topwindow.maxsize(500, 270)
	        topwindow.transient(master)
	        
	        self.labelNameBookVar = StringVar(master)
	        self.inputPagePausedVar = StringVar(master)
	        self.progressVar = IntVar(master)
	        
	        Label(topwindow, textvar=self.labelNameBookVar, foreground="#008B8B", background="#B4CDCD",\
	         font=("Arial", 12, "bold"), pady=10).pack(side=TOP, fill=X)
	        Label(topwindow, text="LIVRO", foreground="white", background="#B4CDCD",\
	         font=("Arial", 7, "bold")).place(x=0, y=-3)
	        
	        panelInput = Frame(topwindow)
	        panelInput.pack(side=TOP, padx=20, pady=20)

	        Label(panelInput, text=u"Página atual").pack(side=LEFT)
	        self.inputPagePaused = Spinbox(panelInput, textvariable=self.inputPagePausedVar, width=4, increment=1, command=self.updateProgress)
	        self.inputPagePaused.pack(side=LEFT, padx=10)

	        panelProgressMain = Frame(topwindow)
	        panelProgressMain.pack(side=TOP, fill=X, padx=20, pady=20)
	        panelProgress = Frame(panelProgressMain)
	        panelProgress.pack(side=LEFT, expand=True, fill=X)

	        self.labelProgress = Label(panelProgress, foreground="#008B8B",\
	        font=("Arial", 10, "bold"))
	        self.labelProgress.pack(side=LEFT)
	        
	        progressFrame = Frame(panelProgress)
	        progressFrame.pack(side=TOP, expand=True, fill=X, padx=15, pady=10)

	        self.progress = Progressbar(progressFrame, variable=self.progressVar)
	        self.progress.pack(fill=X)
	        
	        
	        Separator(topwindow).pack(side=TOP, fill=X)

	        panelDown = Frame(topwindow)
	        panelDown.pack(side=TOP, padx=20, pady=20)

	        TButton(panelDown, text="Salvar", width=10, command=self.actionUpdatePagePausedBook).pack(side=LEFT)
	        TButton(panelDown, text="Cancelar", width=10, command=lambda: topwindow.destroy()).pack(side=LEFT)

	        self.setDatas()
	        #topwindow.resizable(False, False)

	        self.progressVar.trace("w", lambda a, b, c: self.labelProgress.config(text="Progresso"+str(self.progressVar.get())+"%"))

	def updateProgress(self):
		"Atualiza a barra de progresso"
		p = (100*(int(self.inputPagePaused.get())-int(self.start_read)) / (int(self.total_pages)-int(self.start_read)))
		self.progressVar.set(p)

	def setDatas(self):
		"Inputa as informacoes necessarias do book"
		book_name, self.page_paused, self.start_read, self.total_pages = self.book.getBook("nome, pagina_pausada, inicio_leitura, total_paginas", self.id_line_selected)
		percent = self.book.getPercentReadBook(self.id_line_selected)

		self.labelNameBookVar.set(book_name.upper())
		self.inputPagePausedVar.set(self.page_paused)
		self.inputPagePaused.config(from_=self.start_read, to=self.total_pages)
		self.progressVar.set(percent)

		#print self.progressVar.get()
		
		#self.labelProgress.config(text=)

	def actionUpdatePagePausedBook(self):
		"Atualiza o banco de dados com a página atual do marcador de página"
		pageCurrent = self.inputPagePausedVar.get()
		if pageCurrent:
		    self.book.updatePagePaused(self.id_line_selected, pageCurrent)
		    tkmsg.showinfo("Atualizado", "Marcador atualizado")
		    self.topwindow.destroy()
		else:
		    tkmsg.showwarning("Alerta", u"Não é possível salvar o campo vazio")

class InputBookGui:
	def __init__(self, master, title):
		self.labelNameBookVar = StringVar(master)
		self.inputNameBookVar = StringVar(master)
		self.inputAuthorBookVar = StringVar(master)
		self.inputCategoryVar = StringVar(master)
		self.inputYearVar = StringVar(master)
		self.inputTotalPagesVar = StringVar(master)
		self.inputStartReadVar = StringVar(master)

		self.inputNameBookVar.trace("w", lambda a, b, c:self.labelNameBookVar.set(self.inputNameBookVar.get().upper()),)

		self.topwindow = Toplevel(master)
		self.topwindow.title(title)
		#topwindow.geometry("400x150+150+150")
		#topwindow.maxsize(500, 200)
		self.topwindow.transient(master)
		self.topwindow.resizable(False, False)

		Label(self.topwindow, textvar=self.labelNameBookVar, foreground="#008B8B", background="#B4CDCD",\
		 font=("Arial", 12, "bold"), pady=10).pack(side=TOP, fill=X)
		Label(self.topwindow, text="LIVRO", foreground="white", background="#B4CDCD",\
		 font=("Arial", 7, "bold")).place(x=0, y=-3)

		panelTop = Frame(self.topwindow)
		panelTop.pack(side=TOP, padx=20, pady=20)

		panelDown = Frame(self.topwindow)
		panelDown.pack(side=TOP, padx=20, pady=20)

		self.inputAuthorBookVar = StringVar()
		Label(panelTop, text=u"Nome").pack(side=LEFT)
		self.inputNameBook = Entry(panelTop, textvariable=self.inputNameBookVar, width=30)
		self.inputNameBook.pack(side=LEFT, padx=10)

		Label(panelTop, text=u"Autor").pack(side=LEFT)
		Entry(panelTop, textvariable=self.inputAuthorBookVar).pack(side=LEFT, padx=10)
		Label(panelTop, text=u"Categoria").pack(side=LEFT)
		Entry(panelTop, textvariable=self.inputCategoryVar).pack(side=LEFT, padx=10)

		Label(panelDown, text=u"Ano").pack(side=LEFT)
		self.inputYear = Spinbox(panelDown, textvariable=self.inputYearVar, width=5, increment=1, from_=1980, to=datetime.now().year)
		self.inputYear.pack(side=LEFT, padx=10)
		Label(panelDown, text=u"Total de páginas").pack(side=LEFT)
		self.inputTotalPages = Spinbox(panelDown, textvariable=self.inputTotalPagesVar, width=5, command=self.updateLimitInputStartRead, increment=1, from_=1, to=2000)
		self.inputTotalPages.pack(side=LEFT, padx=10)
		Label(panelDown, text=u"Início da Leitura").pack(side=LEFT)
		self.inputStartRead = Spinbox(panelDown, textvariable=self.inputStartReadVar, width=5, increment=1, from_=1, to=1)
		self.inputStartRead.pack(side=LEFT, padx=10)

		self.buttonSave = TButton(panelDown, text="Salvar", width=10)
		self.buttonSave.pack(side=LEFT, padx=5, ipadx=15)
		TButton(panelDown, text="Cancelar", width=10, command=lambda: self.topwindow.destroy()).pack(side=LEFT, padx=5)
	
	def updateLimitInputStartRead(self):
		self.inputStartRead.config(from_=1, to=self.inputTotalPagesVar.get())

	def configCommandSave(self, commandSave):
		self.buttonSave.config(command=commandSave)
	
	def setValuesDefaults(self):
		self.inputStartReadVar.set(1)
		self.focusFirstField()

	def focusFirstField(self):
	    self.inputNameBook.focus_force()

class AddBookGui(InputBookGui):
	def __init__(self, master, book, x=0, y=0):
		self.master = master
		self.book = book
		if master:
			InputBookGui.__init__(self, master, title="Novo Livro")
			self.topwindow.geometry("+{}+{}".format(x, y))

			self.setValuesDefaults()
			self.configCommandSave(self.actionSaveNewBook)

	def actionSaveNewBook(self):
		"Atualiza o banco de dados com o novo Livro"

		if self.inputNameBookVar.get():
		    self.book.saveNewBook(self.inputNameBookVar.get().lower(),self.inputAuthorBookVar.get().lower(),\
			self.inputYearVar.get(), self.inputCategoryVar.get(),\
			self.inputTotalPagesVar.get(),self.inputStartReadVar.get())

		    tkmsg.showinfo("Salvo", "Novo Livro({}) salvo com sucesso.".format(self.inputNameBookVar.get().upper()[:15]+"..."))
		    self.topwindow.destroy()
		else:
		    tkmsg.showwarning("Alerta", u"Informe o nome do livro para continuar.")

class ChangeBookGui(InputBookGui):
	def __init__(self, master, book, id_selected, x=0, y=0):
		self.master = master
		self.book = book
		self.id_selected = id_selected

		InputBookGui.__init__(self, master, title="Alterar Livro")
		print x, y
		self.topwindow.geometry("+{}+{}".format(x, y))

		self.focusFirstField()
		self.setValuesFields()
		self.configCommandSave(self.actionUpdateBook)


	def setValuesFields(self):
		fields = self.book.getBook("nome, autor, ano, categoria, total_paginas, pagina_pausada, inicio_leitura", self.id_selected)
		self.inputNameBookVar.set(fields[0])
		self.inputAuthorBookVar.set(fields[1] or "")
		self.inputYearVar.set(fields[2])
		self.inputCategoryVar.set(fields[3] or "")
		self.inputTotalPagesVar.set(fields[4])
		self.inputStartReadVar.set(fields[5])

	def actionUpdateBook(self):
		self.book.updateBook(self.id_selected, self.inputNameBookVar.get(), self.inputAuthorBookVar.get(), self.inputYearVar.get(), self.inputCategoryVar.get(), self.inputTotalPagesVar.get(), self.inputStartReadVar.get())
		
		#PopupHelp(self.toplevel, self.dp, text="Informe uma data para finalizar\n a leitura de todos os livros")


class CalculatorGui:
    def __init__(self, master, book):
        self.master = master
        self.book = book
        self.setVars()
        self.createGui()

    def createGui(self):
        self.toplevel = Toplevel(self.master)
        self.toplevel.transient(self.master)
        self.toplevel.title("Calculadora de meta")
        self.toplevel.geometry("300x250+200+150")
        self.toplevel.resizable(False, False)

        Label(self.toplevel, text="CALCULAR META", foreground="#008B8B", background="#B4CDCD",\
	         font=("Arial", 12, "bold"), pady=10).pack(side=TOP, fill=X)

        inputDateFields = Frame(self.toplevel)
        inputDateFields.place(x=10, y=50)
        
        Label(inputDateFields, text="Data").pack(side=LEFT)
    	self.dp = Datepicker(inputDateFields, dateformat="%d/%m/%Y", datevar=self.dateLabelVar)
    	self.dp.pack(anchor="w", side=LEFT)

    	PopupHelp(self.toplevel, self.dp, text="Informe uma data para finalizar\n a leitura de todos os livros")
        
        showMediaPagesDayFrame = Frame(self.toplevel)#Contem os Labels de exibição de resultado
        showMediaPagesDayFrame.place(x=10, y=100)
        
        Label(showMediaPagesDayFrame, textvariable=self.mediaPagesDayVar, width=6, foreground="#008B8B", background="#B4CDCD", font=("Arial", 12, "bold")).grid(row=0, column=0, stick=W)
        Label(showMediaPagesDayFrame, text=u"Páginas por dia.", foreground="#66CD00", font=("Arial", 12, "bold")).grid(row=0, column=1, stick=W)
        Label(showMediaPagesDayFrame, text=u"Durante X dias ininterruptos.", textvariable=self.daysRestVar, foreground="#66CD00", font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, stick=W)
        #Label(showMediaPagesDayFrame, text=u"Durante X dias ininterruptos.", foreground="#66CD00", font=("Arial", 12, "bold")).grid(row=0, column=1, stick=E)
    
    def setVars(self):
        self.daysRestVar = StringVar()
        self.mediaPagesDayVar = StringVar()
        self.dateLabelVar = StringVar()

        self.daysRestVar.set("Durante X dias ininterruptos.")
        self.mediaPagesDayVar.set("0")
        self.dateLabelVar.set("00/00/0000")
        self.dateLabelVar.trace("w", self.actionShowMediaPagesDay)
        self.data = {}
    
    def actionShowMediaPagesDay(self, a, b, c):
    	dateCurrent = self.dp.current_date
        days_rest = getDaysRest({"day": dateCurrent.day, "month": dateCurrent.month, "year": dateCurrent.year})#Calcula os dias restantes
        
        if days_rest > 0:
        	self.setMediaPagesDayVar(self.book.getMediaPagesDay(self.book.getTotalPagesNotReads(), days_rest))#Escreve na Label a media de pagina para ler por dia
        	self.setDaysRestLabel(days_rest)#Escreve na Label os dias restantes
        	
     	else:
     		self.setDaysRestLabel("0")
    		self.setMediaPagesDayVar("0")
    
    def setDaysRestLabel(self, days_rest):
        self.daysRestVar.set(u"Durante {} dias ininterruptos.".format(days_rest))
    
    def setMediaPagesDayVar(self, mediaPagesDay):
        self.mediaPagesDayVar.set(mediaPagesDay)

    def setDatas(self):
        days_rest = getDaysRest({"day": 31, "month": 12, "year": 2018})
        self.setDaysRestLabel(days_rest)
        mediaPagesDay = self.book.getMediaPagesDay(self.book.getTotalPagesNotReads(), days_rest)#Retorna a media de páginas por dia
        self.setMediaPagesDayVar(mediaPagesDay)

class FindRowGui:
    def __init__(self, table, master):
        self.master = master
        self.table = table

        self.frameOptions = Frame(master, background="#B4CDCD")
        self.frameOptions.pack(side=BOTTOM, fill="both", pady=5)

        Label(self.frameOptions, text="Procurar Livro", background="#B4CDCD").pack(side=TOP, fill=X, padx=5, pady=5)
        self.inputWordVar = StringVar()
        self.inputWordVar.trace("w", self.updateFindRow)
        inputWord = Entry(self.frameOptions, font=("Arial", 11), textvariable=self.inputWordVar)
        inputWord.pack(side=TOP, padx=5, pady=5, fill=X)
        #b = Button(self.frameOptions, text="Procurar", command=self.actionFindRow, padx=10)
        #b.pack(side=TOP, padx=5, pady=5)
        PopupHelp(master, inputWord, u"Procura livros por palavra")

        self.activeFind = False

    def updateFindRow(self, a, b, c):
        if not self.activeFind:
            self.activeFind = True
            self.master.after(100, self.findRow)


    def findRow(self):
        #self.table.showAllRows()
        self.table.hiddenRowsWithWord(self.inputWordVar.get().lower())
        self.activeFind = False
        self.table.actionPageUp()
if __name__ == "__main__":
	from Books import Books
	root = Tk()
	ab = AddBookGui(root, Books())
	root.mainloop()
