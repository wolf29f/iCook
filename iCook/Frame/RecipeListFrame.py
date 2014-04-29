import tkinter as tk
from tkinter import ttk

from . import *
from .. import Recipe, DataBase

class RecipeListFrame(ttk.Frame):

    def __init__(self,parent=None,recipeList=[],**kwarg):
        assert type(recipeList) in (list,tuple)
        ttk.Frame.__init__(self,parent,**kwarg)
        self.recipeLineList = []
        self.parent = parent

        for index, element in enumerate(recipeList):
            self.recipeLineList.append(RecipeLine(self,element,borderwidth=5,relief='ridge'))
            self.recipeLineList[-1].grid(row=index,column=0,sticky=tk.E+tk.W)

    def updateRecipeList(self,recipeList=[]):
        for i in self.recipeLineList:
            i.destroy()

        for index, element in enumerate(recipeList):
            self.recipeLineList.append(RecipeLine(self,element,borderwidth=5,relief='ridge'))
            self.recipeLineList[-1].grid(row=index,column=0,sticky=tk.E+tk.W)

    def chooseRecipe(self,caller):
        self.parent.chooseRecipe(caller.recipe)

class RecipeLine(ttk.Frame):
    def __init__(self,parent,recipe,**kwarg):
        assert type(recipe) is Recipe.Recipe
        ttk.Frame.__init__(self,parent,**kwarg)
        self.parent = parent
        self.recipe = recipe

        self.label = ttk.Label(self,text=self.recipe.name)
        # self.picture = None

        self.label.grid(row=0,column=1,sticky=tk.E+tk.W)
        self.label.bind("<Button-1>", self.callback)
        # self.picture.bind("<Button-1>", self.callback)
        # self.picture.grid(row=0,column=0)

        self.bind("<Button-1>", self.callback)

    def callback(self,event):
        self.parent.chooseRecipe(self)





