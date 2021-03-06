import tkinter as tk
from tkinter import ttk
from tkinter import font

from . import *
from .. import Recipe, DataBase, rootUrl

import tkinter.messagebox as messagebox
import urllib.request

class RecipeFrame(Frame.Frame):

    def __init__(self,parent=None,mainFrame=None,**kwarg):
        Frame.Frame.__init__(self,parent,mainFrame,padding=5,**kwarg)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.recipe = Recipe.Recipe()
        self.pic = None
        self.editButton = ttk.Button(self, text="Edit", command=self.editRecipe)

        self.favChoice = tk.IntVar()
        self.favButton = ttk.Checkbutton(self, text="Ajouter aux favoris",variable=self.favChoice,command=self.addToFav)
        self.favButton.grid(row=0,column=0,sticky=tk.E+tk.W)

        self.textContent = tk.Text(self,state="disable")
        self.textContent.tag_config("header",font=font.Font(size=22),justify="center")
        self.textContent.tag_config("header2",font=font.Font(size=18),justify="center")
        self.textContent.tag_config("bold",font=font.Font(weight="bold"))
        
        self.textContent.tag_config("pic",justify="right")

        self.textContent.tag_config("list",lmargin1=20,lmargin2=20)
        self.textContent.grid(row=1,column=0,sticky=tk.E+tk.W+tk.S+tk.N,columnspan=2)

        self.picLabel = tk.Label(self)
        self.picLabel.grid(row=1,column=0,sticky=tk.E+tk.N,padx=(5,5),pady=(5,5),columnspan=2)


    def editRecipe(self):
        self.mainFrame.getToAddRecipeFrame(self.recipe)


    def loadRecipe(self, recipe):
        assert type(recipe) is Recipe.Recipe

        self.recipe = recipe
        picPath = os.path.dirname(os.path.realpath(__file__))+"/../res/pic/"+self.recipe.pictureLocation
        try:
            if not self.recipe.isLocal: #TODO : Allow the user to add picture for their recipe
                self.pic = tk.PhotoImage(file=picPath)
        except tk.TclError as e:            
            self.pic = None
            if recipe.isLocal:
                messagebox.showerror("Pas d'image", "Aucun image n'a été trouvé sur votre ordinateur, veuillez re-selection l'image en éditant la recette")
            else:
                try:
                    urllib.request.urlretrieve(rootUrl+"res/pic/"+self.recipe.pictureLocation, picPath)
                    try:
                        self.pic = tk.PhotoImage(file=picPath)
                    except tk.TclError:
                        messagebox.showerror("Pas d'image", "Aucun image n'a été trouvé, il n'a pas été possible de la charger, veuillez ré-essayer plus tard")
                except (urllib.request.HTTPError,urllib.request.URLError):
                        messagebox.showerror("Erreur de connexion'", "Une erreur de connexion est survenue, veuillez ré-essayer plus tard")            
        if self.pic:
            self.picLabel.config(image=self.pic)
        else:
            self.picLabel.grid_forget()
        if self.recipe.isLocal:
            self.editButton.grid(column=1,row=0) 
        else:
            self.editButton.grid_forget()

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



        while 1:
            content = self.textContent.get("1.1", "end")
        
            i1 = content.find("<b>")
            i2 = content.find("</b>")
            if i1 >= 0 and i2 >= 0:
                self.textContent.tag_add("bold","1.0 + "+str(i1+3)+" char","1.0 + "+str(i2+4)+" char")
                self.textContent.delete("1.0 + "+str(i2)+" char", "1.0 + "+str(i2+4)+" char")
                self.textContent.delete("1.0 + "+str(i1)+" char", "1.0 + "+str(i1+3)+" char")
            else:
                break




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
