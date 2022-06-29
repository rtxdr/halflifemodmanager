import sys
import os
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

debugmode = False
color1 = "#252525" #darkgrey
color2 = "#474747" #grey
color3 = "#FF5900" #accentcolor
changedcolors = False


class appmain(QWidget):

   def __init__(self):
      super().__init__()

      self.initUI()


   def initUI(self):
      app = QApplication(sys.argv)

      self.b = QLabel(self)
      self.b.setText("Half-Life Mod Manager 1.0")
      self.b.setFont(QFont("Trebuchet MS", 25))
      self.b.move(0,0)


      self.btn = QPushButton(self)
      self.btn.setText("Start Game")
      self.btn.move(20,350)
      self.btn.clicked.connect(self.startgame)

      self.btnexit = QPushButton(self)
      self.btnexit.setText("Exit")
      self.btnexit.move(385,350)
      self.btnexit.clicked.connect(self.close)

      self.btnrefresh = QPushButton(self)
      self.btnrefresh.setText("Refresh")
      self.btnrefresh.move(385,300)
      self.btnrefresh.clicked.connect(self.refreshgames)

      self.cb = QComboBox(self)
      self.cb.resize(200,30)
      self.cb.move(20,100)
      self.cb.currentTextChanged.connect(self.oncbchange)
      self.cb.currentTextChanged.connect(self.stylechange)
      detectmods()
      self.cb.addItems(detectedmods)

      self.setFixedHeight(400)
      self.setFixedWidth(490)
      self.setWindowTitle("HLMM")
      self.show()
      sys.exit(app.exec_())

   def stylechange(self):
      self.b.setStyleSheet("color: %s;background-color: %s;padding: 12px" % (color3, color1)) #main
      self.cb.setStyleSheet("background-color: %s;color: %s" % (color1, color3)) #COMBOBOX
      self.btn.setStyleSheet("background-color: %s;color: %s" % (color1, color3)) #START BUTTON
      self.btnexit.setStyleSheet("background-color: %s;color: %s" % (color1, color3)) #EXIT BUTTON
      self.btnrefresh.setStyleSheet("background-color: %s;color: %s" % (color1, color3)) #REFRESH BUTTON
      self.setStyleSheet("background-color: %s;" % color2)

   def oncbchange(self, value):
      global color3
      global color2
      global color1
      global changedcolors
      if value == "Counter-Strike":
         color3 = "#fff719" #yelow
         color1 = "#2c4793" #blue
         color2 = "#192547"
      if value == "Brutal Half-Life - beta 2":
         color3 = "#ff0000" #red
         color1 = "#252525" #darkgrey
         color2 = "#171717"
      if value == "Blue Shift":
         color3 = "#0f68e7" #blue
         color1 = "#353844" #iron
         color2 = "#1d1e24"
      if value == "Deathmatch Classic ":
         color3 = "#b88e39" #orange? darker
         color1 = "#351808" #dark orange
         color2 = "#211007"
      if value == "Opposing Force":
         color3 = "#00ff00" #green
         color1 = "#181e14" #green dark
         color2 = "#11140e"
      if value == "Team Fortress":
         color3 = "#9fa361" #accent
         color1 = "#1f1e13" #dark
         color2 = "#12110b"
      if value == "Half-Life":
         color3 = "#b4a74d" #trad
         color1 = "#4c5844" #
         color2 = "#404434"


      self.stylechange()

   def startgame(self):
      current_value = self.cb.currentIndex()
      if debugmode == True:
         print(detectedmodsdir[current_value])
      self.close()
      gametorun = detectedmodsdir[current_value]
      if gametorun == "valve":
         subprocess.run(["hl.exe"])
      else:
         subprocess.run(["hl.exe", "-game", "%s" % detectedmodsdir[current_value]])

   def refreshgames(self):
      self.cb.clear()
      detectmods()
      self.cb.addItems(detectedmods)

def detectmods():
   global game_ln
   global detectedmods
   global detectedmodsdir
   detectedmods = []
   detectedmodsdir = []
   initialpath = os.getcwd()
   for file in os.listdir(initialpath):
    d = os.path.join(initialpath, file)
    if os.path.isdir(d):
      for File in os.listdir(d):
         if File.endswith(".gam"):
            splitmodname = d.split("\\")
            modname = (splitmodname[-1])
            detectedmodsdir.append(modname)
            liblistfile = open(d+"\\\\"+File)
            for ln in liblistfile:
               if ln.startswith('game '):
                  game_ln = ln[0:]
                  modname = game_ln[6:-2]
                  detectedmods.append(modname)
   if debugmode == True:
      print(detectedmodsdir)
      print(detectedmods)
                  
def main():
   detectmods()
   app = QApplication(sys.argv)
   widgetmain = appmain()

   sys.exit(app.exec_())

if __name__ == '__main__':
   main()