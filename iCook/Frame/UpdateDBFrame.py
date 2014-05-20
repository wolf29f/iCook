import tkinter as tk
from tkinter import ttk


import tkinter.messagebox as messagebox
from . import *
from .. import Recipe, DataBase

class UpdateDBFrame(Frame.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        Frame.Frame.__init__(self,parent,mainFrame,**kwarg)        
        self.db = DataBase.DataBase()
        self.updateDBButton = tk.Button(self,text="Mettre a jour",command=self.updateDB)
        self.updateDBButton.pack(fill=tk.BOTH, expand=1)
        self.progress = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(self,  mode='determinate')
        self.progressbar.pack(fill=tk.BOTH, expand=1)

    def updateDB(self):
        self.progress.set(0)
        # self.progressbar.start()
        self.db = DataBase.DataBase()
        if not self.db.updateDB(self.progress):
            # self.progressbar.stop()
            self.dbUpdateErrorMessage()
        else:
            # self.progressbar.stop()
            self.dbUpdateSuccesMessage()
        

    def dbUpdateErrorMessage(self):
        messagebox.showerror("Erreur de connexion'", "Une erreur de connexion est survenue, veuillez ré-essayer plus tard")            

    def dbUpdateSuccesMessage(self):
        messagebox.showinfo("Succes", "Mise à jour reussie") 
