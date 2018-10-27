from Tkinter import *

class PopupHelp():
    def __init__(self, root, master, text, timeout=700):
        self.root = root
        self.master = master
        self.text = text
        self.timeout = timeout
        
        self.motion = self.master.bind("<Motion>", self.EventStart)
        self.leave = self.master.bind("<Leave>", self.EventStop)
        

        self.waitEvent = False
        self.listPopups = []
        self.coord = [0, 0]
    
    def EventStart(self, event):
        #print "start event"
        #self.master.unbind(self.motion)
        #self.leave = self.master.bind("<Leave>", self.EventStop)
        if not self.waitEvent:
            self.DestroyAllPopups()
            self.coord[0] = event.x_root
            self.coord[1] = event.y_root
            self.master.after(self.timeout, lambda: self.CreateTextHelp(self.coord))
            
            self.waitEvent = True

    def CreateTextHelp(self, coordinates):
        if self.waitEvent:
            self.popup = popup = Toplevel(self.master)
            #popup.transient(self.master)
            popup.attributes("-toolwindow", True)
            popup.attributes("-alpha", 0.7)
            #popup.attributes("-topmost", True)
            popup.overrideredirect(True)
            
            popup.geometry("+{}+{}".format(coordinates[0]-30, coordinates[1]+20))
            f = Frame(popup, highlightbackground="grey51", highlightthickness=1, height=1)
            f.pack()
            Label(f, text=self.text, background="khaki1").pack()
            
            self.listPopups.append(popup)

    def EventStop(self, event):
        #print "stop event", event.keysym_num, event.keycode
        self.EventDestroy()
        #self.motion = self.master.bind("<Motion>", self.EventStart)
        #self.master.unbind(self.leave)

    def EventDestroy(self):
        self.waitEvent = False
        self.DestroyAllPopups()       

    def DestroyAllPopups(self):
        [popup.destroy() for popup in self.listPopups]
        self.listPopups = []
        
        
if __name__ == "__main__":
    root = Tk()
    root.title("Teste")

    b = Button(root, text="OK")
    b.place(x=0, y=10)
    
    p = PopupHelp(root, b, "Move o cursor para determinado local\noutra ajuda aqui")
    root.mainloop()


