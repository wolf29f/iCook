
from . import Recipe
import sqlite3
import tkinter.messagebox as messagebox
import ast
import time

from . import rootUrl
import urllib.request


class DataBase(object):

    def __init__(self):
        self.dbName = "iCook/res/recipeBDD"

        conn = sqlite3.connect(self.dbName,detect_types= sqlite3.PARSE_COLNAMES)
        c=conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        r = c.fetchall()

        if not ("onlineRecipe",) in r:
            self.noDBMessage()
        if not ("localRecipe",) in r:        
            self.createLocalDB()
        c.close()
        
    def searchRecipe(self,ingredientList=[],name="",favorite=False):
        assert type(ingredientList) in (list,tuple)
        assert type(name) is str
        result = {}

        conn = sqlite3.connect(self.dbName,detect_types= sqlite3.PARSE_COLNAMES)
        c=conn.cursor()

        resultOnline = []
        resultLocal = []
        try:
            #online DB
            if favorite:
                if ingredientList == [] and name!="":
                    c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients,numberPeople FROM onlineRecipe WHERE (name LIKE ? AND isFav='True') """, ["%"+name+"%",])        
                    resultOnline += c.fetchall()                    
                else:
                    for ingredient in ingredientList:
                        c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients, numberPeople FROM onlineRecipe WHERE (ingredients LIKE ? AND name LIKE ? AND isFav='True') """, ["%"+ingredient+"%","%"+name+"%"])
                        resultOnline += c.fetchall()
            else:
                if ingredientList == [] and name!="":
                    c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients,numberPeople FROM onlineRecipe WHERE (name LIKE ?) """, ["%"+name+"%",])        
                    resultOnline += c.fetchall()
                else:
                    for ingredient in ingredientList:
                        c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients, numberPeople FROM onlineRecipe WHERE (ingredients LIKE ? AND name LIKE ?) """, ["%"+ingredient+"%","%"+name+"%"])
                        resultOnline += c.fetchall()    

            for index, val in enumerate(resultOnline):
                resultOnline[index]=val+(False,)  #Last element allow to know if the recipe is local

            #local DB
            if favorite:
                if ingredientList == [] and name!="":
                    c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients, numberPeople FROM localRecipe WHERE (name LIKE ? AND isFav='True') """, ["%"+name+"%",])
                    resultLocal += c.fetchall()
                else:
                    for ingredient in ingredientList:
                        c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients, numberPeople FROM localRecipe WHERE (ingredients LIKE ? AND name LIKE ? AND isFav='True') """, ["%"+ingredient+"%","%"+name+"%"])
                        resultLocal += c.fetchall()
            else:
                if ingredientList == [] and name!="":
                    c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients, numberPeople FROM localRecipe WHERE (name LIKE ?) """, ["%"+name+"%",])
                    resultLocal += c.fetchall()
                else:
                    for ingredient in ingredientList:
                        c.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients, numberPeople FROM localRecipe WHERE (ingredients LIKE ? AND name LIKE ?) """, ["%"+ingredient+"%","%"+name+"%"])
                        resultLocal += c.fetchall()


            for index, val in enumerate(resultLocal):
                resultLocal[index]=val+(True,)  #Last element allow to know if the recipe is local

        except sqlite3.OperationalError:
            self.noDBMessage()
            return None
        result = set(resultLocal+resultOnline)
        sortedResult = []


        for r in result:
            score = 0
            if name in r[0]:
                score+=1
            for ingredient in ingredientList:
                if ingredient in r[5]:
                    score+=1
            sortedResult.append([r,score])
        sortedResult = sorted(sortedResult,key=lambda r: -r[1])
        for r, score in sortedResult:
            yield Recipe.Recipe(r[0],r[1],r[2],r[3],ast.literal_eval(r[4]),r[5],r[6],isLocal=r[-1])

    def addRecipe(self,recipe):

        assert type(recipe) is Recipe.Recipe
        conn = sqlite3.connect(self.dbName,detect_types= sqlite3.PARSE_COLNAMES)
        c=conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='localRecipe';""")
        if c.fetchall() == []:
            c.close()
            self.createLocalDB()

        c.execute("""SELECT * FROM localRecipe WHERE (recipeId = ?)""", [recipe.recipeId])
        result = c.fetchall()
        
        if recipe.recipeId:
            c.execute("""UPDATE localRecipe
            SET name = ?, pictureLocation = ?, recipe = ?, isFav = ?, ingredients = ?, numberPeople = ?
            WHERE recipeId = ?""",
            [recipe.name, recipe.pictureLocation, recipe.recipe, recipe.isFav, recipe.ingredients, recipe.nbrPeople, recipe.recipeId])
        else:
            c.execute("""INSERT INTO localRecipe (name, pictureLocation, recipe, isFav, ingredients, numberPeople)
                                    VALUES (?, ?, ?, ?, ?, ?)""",
                                    [recipe.name, recipe.pictureLocation, recipe.recipe, "False", recipe.ingredients, recipe.nbrPeople])

        conn.commit()
        c.close()
                                
    def noDBMessage(self):
        messagebox.showerror("Pas de base de données", "Aucun base de données n'a été trouvé, veuillez mettre a jour votre base de données de recette")

    def createLocalDB(self):
        conn = sqlite3.connect(self.dbName,detect_types= sqlite3.PARSE_COLNAMES)
        c=conn.cursor()
        c.execute("""CREATE TABLE localRecipe (name TEXT, pictureLocation TEXT, recipe TEXT, recipeId TEXT, isFav TEXT, ingredients TEXT, numberPeople INTEGER)""")
        conn.commit()
        c.close()
        self.localDBCreationMessage()

    def addFav(self,recipeId):
        assert type(recipeId) is str
        conn = sqlite3.connect(self.dbName,detect_types= sqlite3.PARSE_COLNAMES)
        c=conn.cursor()

        result = []
        c.execute("""SELECT * FROM onlineRecipe WHERE isFav='True' AND recipeId = (?)""", [recipeId,])
        result += c.fetchall()
        c.execute("""SELECT * FROM localRecipe WHERE isFav='True' AND recipeId = (?)""", [recipeId,])
        result += c.fetchall()

        if result == []: #no favorite found
            c.execute("""UPDATE onlineRecipe SET isFav='True' WHERE recipeId = (?)""", [recipeId,])    
            c.execute("""UPDATE localRecipe SET isFav='True' WHERE recipeId = (?)""", [recipeId,])    
        else:
            c.execute("""UPDATE onlineRecipe SET isFav='False' WHERE recipeId = (?)""", [recipeId,])    
            c.execute("""UPDATE localRecipe SET isFav='False' WHERE recipeId = (?)""", [recipeId,])
        conn.commit()
        c.close()

    def localDBCreationMessage(self):
        messagebox.showinfo("Creation de la base de données", "Creation de la base de données locale contenant vos recettes") 

    def updateDB(self,progress):
        try:
            urllib.request.urlretrieve(rootUrl+"recipeBDD",self.dbName+"tmp")
        except (urllib.request.HTTPError,urllib.request.URLError) as e:
            print(e)
            return 0
        connNew = sqlite3.connect(self.dbName+"tmp",detect_types= sqlite3.PARSE_COLNAMES)
        cNew=connNew.cursor()
        
        cNew.execute("""SELECT name,pictureLocation,recipe,recipeId,isFav,ingredients,numberPeople FROM onlineRecipe""")
        result = cNew.fetchall()

        connOld = sqlite3.connect(self.dbName,detect_types= sqlite3.PARSE_COLNAMES)
        cOld=connOld.cursor()
        iMax = float(len(result))
        # progressbar.configure(maximum=iMax)
        # progressbar.start()
        last = 0.0
        for i, r in enumerate(result):
            cOld.execute("""UPDATE onlineRecipe SET name=?,pictureLocation=?,recipe=?,isFav=?,ingredients=?,numberPeople=? where recipeId = ?""",
                [r[0],r[1],r[2],r[4],r[5],r[6],r[3]])
            delta = i/iMax-last
            last = i/iMax
            print(last*100)
            progress.set(last*100)
            # progressbar.step(1)
            time.sleep(0.05)
        # progressbar.stop()
        return 1



