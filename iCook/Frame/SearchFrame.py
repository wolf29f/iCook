import tkinter as tk
import Pmw
from tkinter import ttk
import tkinter.messagebox as messagebox

from . import *
from .. import Recipe, DataBase

class SearchFrame(Frame.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        Frame.Frame.__init__(self,parent,mainFrame,padding=5, **kwarg)
        self.recipe = []

        self.menu = ttk.Frame(self)
        self.menu.pack(side=tk.LEFT,fill=tk.Y)

        self.searchValidationReg = self.register(self.searchValidation)

        self.nameLabel = ttk.Label(self.menu,text='Nom de la recette : ')
        self.nameLabel.grid(row=0,column=0,sticky=tk.W)

        self.nameEntry = ttk.Entry(self.menu,validate='key',validatecommand=(self.searchValidationReg,'%P','%W'))
        self.nameEntry.grid(row=1,column=0,sticky=tk.W)

        self.elementsLabel = ttk.Label(self.menu,text='Ingredients (un par ligne) : ')
        self.elementsLabel.grid(row=2,column=0,sticky=tk.W)

        self.elementEntrys = []
        for i in range(5):
            self.elementEntrys.append(ttk.Entry(self.menu,validate='key',validatecommand=(self.searchValidationReg,'%P','%W')))
        for index, element in enumerate(self.elementEntrys):
            element.grid(row=3+index,column=0,sticky=tk.W)

        self.favChoice = tk.IntVar() 
        self.favButton = ttk.Checkbutton(self.menu, text="Recherche favoris",variable=self.favChoice,command=self.searchValidation)
        self.favButton.grid(row=8,column=0,sticky=tk.W)

        self.recipeListFrame = RecipeListFrame.RecipeListFrame(self)    
        self.recipeListFrame.pack(side=tk.RIGHT,fill=tk.BOTH, expand=1)

    def chooseRecipe(self, recipe):
        assert type(recipe) is Recipe.Recipe
        self.mainFrame.getToRecipeFrame(recipe)

    def displayRecipe(self, recipeList):
        assert type(recipeList) in (list,tuple)
        self.recipeListFrame.updateRecipeList(recipeList)

    def searchValidation(self,newValue="",widget=None):
        db = DataBase.DataBase()
        ingredients = []
        caller = self.nametowidget(widget) if widget else None
        for element in self.elementEntrys:
            if element != caller :
                if element.get()!="":
                    ingredients.append(element.get())
            elif newValue!="":
                    ingredients.append(newValue)

        name = self.nameEntry.get() if caller !=self.nameEntry else newValue 

        recipeList = list(db.searchRecipe(ingredientList=ingredients,name=name,favorite=self.favChoice.get()))
        self.displayRecipe(recipeList)        

        return True