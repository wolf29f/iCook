import tkinter as tk
from tkinter import ttk
from tkinter import font

from . import *
from .. import Recipe, DataBase

import tkinter.messagebox as messagebox


class RecipeFrame(Frame.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        Frame.Frame.__init__(self,parent,mainFrame,padding=5,**kwarg)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        self.recipe = Recipe.Recipe()
        self.pic = None
        self.editButton = ttk.Button(self, text="Edit", command=self.editRecipe)
        # self.saveButton.pack(side=tk.TOP)

        self.favChoice = tk.IntVar()
        self.favButton = ttk.Checkbutton(self, text="Ajouter aux favoris",variable=self.favChoice,command=self.addToFav)
        # self.favButton.pack(side=tk.TOP)
        self.favButton.grid(row=0,column=0,sticky=tk.E+tk.W)


        self.textContent = tk.Text(self,state="disable")
        self.textContent.tag_config("header",font=font.Font(size=22),justify="center")
        self.textContent.tag_config("header2",font=font.Font(size=18),justify="center")        
        self.textContent.tag_config("pic",justify="right")

        self.textContent.tag_config("list",lmargin1=20,lmargin2=20)

        # self.textContent.pack(fill=tk.BOTH, expand=1)
        self.textContent.grid(row=1,column=0,sticky=tk.E+tk.W+tk.S+tk.N)

        self.picLabel = tk.Label(self)
        self.picLabel.grid(row=1,column=0,sticky=tk.E+tk.N,padx=(5,5),pady=(5,5))



    def editRecipe(self):
        self.mainFrame.getToAddRecipeFrame(self.recipe)

    def loadRecipe(self, recipe):
        assert type(recipe) is Recipe.Recipe
        self.recipe = recipe

        # print(os.path.dirname(os.path.realpath(__file__))+"/../res/pic/")
        # try:
        print(os.path.dirname(os.path.realpath(__file__))+"/../res/pic/"+self.recipe.pictureLocation)
        self.pic = tk.PhotoImage(file=os.path.dirname(os.path.realpath(__file__))+"/../res/pic/"+self.recipe.pictureLocation)
        self.picLabel.config(image=self.pic)

        if self.recipe.isLocal:
            self.editButton.pack(side=tk.TOP,anchor="e") 
        else:
            self.editButton.pack_forget()


        if self.recipe.isFav:
            self.favChoice.set(1)
        else:
            self.favChoice.set(0)

        self.textContent['state'] = 'normal'

        self.textContent.delete('1.0','end')

        self.textContent.insert('end',"\n"+self.recipe.name+"\n\n",("header",))
        
        self.textContent.insert('end',"Recette pour %i personne(s)"%self.recipe.nbrPeople+"\n\n")

        self.textContent.insert('end',"Ingredients :\n")
        self.textContent.insert('end',recipe.ingredients+"\n","list") 

        self.textContent.insert('end',"Réalisation\n\n",("header2"))


        self.textContent.insert('end',self.recipe.recipe)
        self.textContent['state'] = 'disable'
        

    def addToFav(self):
        db = DataBase.DataBase()
        db.addFav(self.recipe.recipeId)
        self.recipe.isFav = not self.recipe.isFav

        self.succesFavMessage()

    def succesFavMessage(self):
        if self.recipe.isFav:
            messagebox.showinfo("Favoris", "Recette ajouté aux favoris") 
        else:
            messagebox.showinfo("Favoris", "Recette supprimé des favoris")
