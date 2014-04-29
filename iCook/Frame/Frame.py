
import tkinter as tk
from tkinter import ttk


class Frame(ttk.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        ttk.Frame.__init__(self,parent,**kwarg)
        self.mainFrame=mainFrame

    def hide(self):
        pass

    def show(self):
        pass