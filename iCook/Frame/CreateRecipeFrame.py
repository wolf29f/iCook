import tkinter as tk
from tkinter import ttk
from uuid import uuid4
import tkinter.messagebox as messagebox

from . import *
from .. import Recipe, DataBase

class CreateRecipeFrame(Frame.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        Frame.Frame.__init__(self,parent,mainFrame,padding=5,**kwarg)
        
        self.recipe = Recipe.Recipe()
        self.recipe.recipeId = uuid4().hex

        self.recipeName = tk.StringVar()
        # self.recipePicLocation = ""
        # self.recipeComponent = ""
        # self.recipeContent = ""
        
        self.recipeNameLabel = ttk.Label(self,text="Nom de la recette :")
        self.recipeNameLabel.grid(column=0)

        self.newRecipe = ttk.Button(self, text="Nouvelle recette", command=self.editRecipe)
        self.newRecipe.grid(row=0,column=3)

        self.recipeNameEntry = ttk.Entry(self,textvariable=self.recipeName) 
        self.recipeNameEntry.grid(column=1,stick='w')

        self.nbrPeople= tk.IntVar()
        self.nbrPeople.set(4)
        self.nbrPeopleLabel = ttk.Label(self, text="Ce plat est prévu pour :")
        self.nbrPeopleLabel.grid(column=0)

        self.nbrPeopleSpinbox = tk.Spinbox(self, textvariable=self.nbrPeople, values=(1,2,3,4,5,6,7,8,9,10,11,12))
        self.nbrPeopleSpinbox.grid(column=1,stick='w')

        self.recipeComponentLabel = ttk.Label(self,text="Ingredients :")
        self.recipeComponentLabel.grid(column=0)

        self.recipeComponentText = tk.Text(self,height = 10)
        self.recipeComponentText.grid(column=1)

        self.recipeContentLabel = ttk.Label(self,text="Recette :")
        self.recipeContentLabel.grid(column=0)

        self.recipeContentText = tk.Text(self)
        self.recipeContentText.grid(column=1)
        
        self.saveButton = ttk.Button(self, text="Enregistrer", command=self.saveRecipe)
        self.saveButton.grid(columnspan=2,pady=(5,0))

        self.editRecipe()

    def editRecipe(self,recipe=None):
        if recipe:
            self.recipe = recipe
            self.recipeName.set(self.recipe.name)
            # self.pictureLocation = pictureLocation
            self.recipeContentText.delete('1.0','end')
            self.recipeContentText.insert('1.0', self.recipe.recipe) 

            self.recipe.recipeId = self.recipe.recipeId
            
            self.recipeComponentText.delete('1.0','end') 
            self.recipeComponentText.insert('1.0', self.recipe.ingredients)

            self.nbrPeople.set(self.recipe.nbrPeople)
        else:
            self.recipeName.set("")
            # self.pictureLocation = pictureLocation
            self.recipeContentText.delete('1.0','end')
            self.recipe.recipeId = uuid4().hex
            self.recipe.isFav = False
            self.recipeComponentText.delete('1.0','end')
            self.nbrPeople.set(4)

    def saveRecipe(self):
        self.recipe.name = self.recipeName.get()
        # self.pictureLocation = pictureLocation
        self.recipe.recipe = self.recipeContentText.get('1.0','end')

        ingredients=self.recipeComponentText.get('1.0','end')
        ingredients=ingredients.split("\n")
        if len(ingredients)>=0:
            for index, val in enumerate(ingredients):                
                if len(val)>=1:
                    while len(val)>0 and val[0] in (" ","\t","-"):
                        val=val[1:]
                    ingredients[index]="-"+val
            self.recipe.ingredients = "\n".join(ingredients)
        else:
            self.recipe.ingredients = ""   
        self.recipe.nbrPeople=self.nbrPeople.get()
        db = DataBase.DataBase()
        db.addRecipe(self.recipe)
        self.succesSaveMessage()

    def succesSaveMessage(self):
        messagebox.showinfo("Succes", "Votre recette à bien été enregistré, félicitation ! Vous pourez desormais la retrouver avec les autres recettes") 

