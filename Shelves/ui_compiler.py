import sys, pprint
from pysideuic import compileUi
currentDir = "/Users/sachabest/Documents/gits/cis099/MayaApp"     
file = open(currentDir+"/mainwindow.ui", "w")
compileUi(currentDir+"mainwindow.ui", file, False, 4, False)
file.close()