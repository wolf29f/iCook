import tkinter as tk
from tkinter import ttk

from . import *
from .. import Recipe, DataBase

class UpdateDBFrame(Frame.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        Frame.Frame.__init__(self,parent,mainFrame,**kwarg)        
        db = DataBase.DataBase()


    def updateDB(self):
        pass

    def dbUpdateErrorMessage(self):
        pass

    def dbUpdateSuccesMessage(self):
        pass