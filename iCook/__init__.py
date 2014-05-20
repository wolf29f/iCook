import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
rootUrl = "http://bad-wolf.fr/tmp_partage/iCook/"      #the url where are all data


from . import DataBase
from . import Recipe
from . import Frame

app = Frame.MainFrame.MainFrame()