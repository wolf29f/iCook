
import tkinter as tk
from tkinter import ttk
import Pmw

from . import Frame, RecipeFrame, SearchFrame, UpdateDBFrame, CreateRecipeFrame
from .. import Recipe


class SplashFrame(tk.Toplevel):

    def __init__(self,app):
        tk.Toplevel.__init__(self,None)
        
        self.app = app
        self.app.master.withdraw()
        # self.master.winfo_screenwidth()
        # self.master.winfo_screenheight()
        self.logo = tk.PhotoImage(file="iCook/res/logo.gif")
        pic_height=self.logo.height()
        pic_width =self.logo.width() 

        self.geometry(str(pic_width)+"x"+str(pic_height)+'+'+
            str(int((self.master.winfo_screenwidth()-pic_width)/2))+"+"+str(int((self.master.winfo_screenheight()-pic_height)/2)))
        
        self.overrideredirect(1)

        self.wait_visibility(self)
        self.alpha = 0
        
        # self.wm_attributes('-alpha', 1)

        self.attributes('-alpha', self.alpha)

        self.canvas = tk.Canvas(self)        
        # self.canvas.attributes('-alpha', 1)
        self.canvas.create_image(int(400/2),int(330/2),image=self.logo)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        # self.pack(fill=tk.BOTH, expand=1)
        self.after(100,self.fadeIn)
        # help(self)
    def fadeIn(self):
        self.alpha += 0.1
        self.attributes('-alpha', self.alpha)
        if self.alpha >=1:
            self.after(1000,self.fadeOut)
        else:
            self.after(100,self.fadeIn)

    def fadeOut(self):
        self.alpha -= 0.1
        self.attributes('-alpha', self.alpha)
        if self.alpha <=0:
            self.app.master.overrideredirect(0)

            self.app.master.deiconify()

        else:
            self.after(10,self.fadeOut)        


