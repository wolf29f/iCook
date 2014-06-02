import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
rootUrl = "http://bad-wolf.fr/partage/iCook/"      #the url where are all data
if not os.path.isdir(os.path.dirname(os.path.realpath(__file__))+"/res"):
    os.mkdir(os.path.dirname(os.path.realpath(__file__))+"/res")
if not os.path.isdir(os.path.dirname(os.path.realpath(__file__))+"/res/pic"):
    os.mkdir(os.path.dirname(os.path.realpath(__file__))+"/res/pic")


from . import Recipe
from . import Frame
from . import DataBase

app = Frame.MainFrame.MainFrame()