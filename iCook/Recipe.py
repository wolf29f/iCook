
class Recipe(object):

    def __init__(self, name = "", pictureLocation = "", recipe = "", recipeId = None, isFav = False, ingredients = [],nbrPeople=0,isLocal=False):
        self.name = name
        self.pictureLocation = pictureLocation
        self.recipe = recipe
        self.recipeId = recipeId
        self.isFav = isFav
        self.ingredients = ingredients
        self.nbrPeople = nbrPeople
        self.isLocal = isLocal

    def __str__(self):
        return "Recette : %s\n Image : %s\n Pour %d personnes\n Ingredients : \n%s Recette: %s Id: %s Favoris: %s Local: %s"%(
            self.name,
            self.pictureLocation,
            self.nbrPeople,
            self.ingredients,
            self.recipe,
            self.recipeId,
            self.isFav,
            self.isLocal)
