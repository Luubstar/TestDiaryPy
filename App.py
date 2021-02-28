from PyQt5 import QtWidgets, QtGui
from datetime import date,time
from test import Ui_MainWindow
import sys
import sqlite3
from functools import partial
import matplotlib.pyplot as mpl
import os
path = os.path.realpath(__file__)
path = path.replace("App.py","")
db = sqlite3.connect(path + "Entries.db")
cursor = db.cursor()
Entries = []
EntriesID = []
Feelings = []
EntryCount = 0
EditingEntry = int
ID = int
def converTuple(tup):
    str = ''.join(tup)
    return str
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PlusButt.clicked.connect(self.AddEntry)
        self.ui.AddButton.clicked.connect(self.EditEntry)
        self.ui.DelButt.clicked.connect(self.DeleteEntry)
        self.ui.SentimientosColor.clicked.connect(self.ColorPick)
        self.ui.SentimientosAdd.clicked.connect(self.AddFeeling)
        self.ui.Menu.clicked.connect(self.MenuTravel)
        self.ui.MenuCon.setEnabled(False)
        self.ui.PerfilCon.setEnabled(False)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.SentimientosColor.setStyleSheet("background-color: white" )
        self.ui.SentimientosDrop.activated.connect(self.LoadFeeling)
        self.ui.SentimientosDropEdic.activated.connect(self.LoadFeeling)
        self.ui.SentimientosRemove.clicked.connect(self.DeleteFeeling)
        self.ui.BackMenu.clicked.connect(self.BackMenu)
        self.ui.Perfil.clicked.connect(self.GoPerfil)
        self.ui.BackPerfil.clicked.connect(self.BackPerfil)
        self.ReloadFeelings()
        self.LoadFeeling()
        self.CargarEntradas()
    def EnterEntry(self,ID):
        global EditingEntry
        print(ID)
        if (EditingEntry != ID):
            self.CleanText()
        if (self.ui.Entrada.isEnabled != True):
            self.ui.Entrada.setEnabled(True)
        try:
            self.LeerEntrada(int(ID))
        except:
            pass
        self.ui.tabWidget.setCurrentIndex(1)
        EditingEntry = ID    
    def AddEntry(self):
        layout = self.ui.scrollAreaContent.layout()
        button = QtWidgets.QPushButton( date.today().__str__())
        button.setMinimumSize(0,76)
        global EntryCount
        global Entries
        button.setProperty("ID", EntryCount)
        button.setProperty("Data",date.today().__str__())
        EntryCount += 1
        layout.addWidget(button)
        Entries.append(button)
        button.clicked.connect(lambda: self.EnterEntry(button.property("ID")))
        color = self.ui.SentimientosColor.palette().color(1).name()
        button.setStyleSheet("background-color: " + color)
        self.EnterEntry(int(button.property("ID")))
        self.ui.Lista.setEnabled(False)
        self.CleanText()
    def EditEntry(self):
        self.ui.Lista.setEnabled(True)
        global EditingEntry
        global Entries
        for button in Entries:
            if (button.property("ID") == EditingEntry):
                button.setText( date.today().__str__() + "  " + self.ui.TituloEdit.text())
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.Entrada.setEnabled(False)
                self.ActualizaGuardar(button.property("ID"),button.property("Data"))
                color = self.ui.ColorEdit.palette().color(1).name()
                button.setStyleSheet("background-color: " + color)
        for item in Entries:
            layout = self.ui.scrollAreaContent.layout()
            layout.removeWidget(item)
        for entry in Entries:
            EntriesID.append(entry.property("ID"))
        EntriesID.sort(reverse=True)
        for button in EntriesID:
            for item in Entries:
                if (item.property("ID") == button):
                    layout = self.ui.scrollAreaContent.layout()
                    layout.addWidget(item)
        self.CleanText()
    def GoPerfil(self):
        self.ui.PerfilCon.setEnabled(True)
        self.ui.tabWidget.setCurrentIndex(3)
        self.ui.Lista.setEnabled(False)
        self.ReloadFeelings()
    def BackPerfil(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.PerfilCon.setEnabled(False)
        self.ui.Lista.setEnabled(True)
    def MenuTravel(self):
        self.ui.MenuCon.setEnabled(True)
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.Lista.setEnabled(False)
    def BackMenu(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.MenuCon.setEnabled(False)
        self.ui.Lista.setEnabled(True)
    #############################
    def ActualizaGuardar(self,ID,Data):
        try:
            cursor.execute(
                "INSERT INTO Entradas VALUES (?,?,?,?,?,?,?);",(ID,self.ui.TituloEdit.text().__str__(),self.ui.SentimientosDropEdic.currentIndex(),self.ui.Razon.text().__str__(),self.ui.Ideas.text().__str__(),self.ui.Reflexion.toPlainText().__str__(),Data))
            self.CleanText()
            db.commit()
        except:
            cursor.execute( "DELETE FROM Entradas WHERE ID = (?)",(ID,))
            db.commit()
            cursor.execute(
                "INSERT INTO Entradas VALUES (?,?,?,?,?,?,?);",(ID,self.ui.TituloEdit.text().__str__(),self.ui.SentimientosDropEdic.currentIndex(),self.ui.Razon.text().__str__(),self.ui.Ideas.text().__str__(),self.ui.Reflexion.toPlainText().__str__(),Data))
            self.CleanText()
            db.commit()
    def CargarEntradas(self):
            global EntryCount
            global Entries
            cursor.execute("SELECT * FROM Entradas")
            Entradas = cursor.fetchall()
            layout = self.ui.scrollAreaContent.layout()
            
            for n in Entradas:
                try:
                    n = n[0]
                    cursor.execute("SELECT Titulo FROM Entradas WHERE ID = (?);",(n,))
                    Titulos = cursor.fetchall()
                    cursor.execute("SELECT Data FROM Entradas WHERE ID = (?);",(n,))
                    Dts = cursor.fetchall()
                    Data =  converTuple(Dts[0])
                    Titulo = converTuple(Titulos[0])
                    button = None
                    button = QtWidgets.QPushButton( date.today().__str__())
                    button.setMinimumSize(0,76)
                    button.setProperty("ID", n)
                    button.setProperty("Data",Data)
                    button.setText(Data + "  " + Titulo)
                    Entries.append(button)
                    layout.addWidget(button)
                    cursor.execute("SELECT Como FROM Entradas WHERE ID = (?);",(n,))
                    Como = cursor.fetchall()
                    self.ui.SentimientosDrop.setCurrentIndex(int(Como[0][0]))
                    text = self.ui.SentimientosDrop.currentText()
                    cursor.execute("SELECT Color FROM Sentimientos WHERE Nombre = (?);",(text,))
                    color = cursor.fetchall()
                    color = converTuple(color[0])
                    button.setStyleSheet("background-color: " + color)
                    EntryCount = n + 1
                except:
                    pass
            for entry in Entries:
                EntriesID.append(entry.property("ID"))
            EntriesID.sort(reverse=True)
            for button in EntriesID:
                print(button)
                for item in Entries:
                    if (item.property("ID") == button):
                        layout = self.ui.scrollAreaContent.layout()
                        item.clicked.connect(partial(self.EnterEntry,item.property("ID")))                           
    def LeerEntrada(self,ID):
        cursor.execute("SELECT * FROM Entradas WHERE ID = (?);", (ID,))
        resultados = cursor.fetchall()
        res = int(resultados[0][2])
        self.ui.TituloEdit.setText(resultados[0][1])
        self.ui.Razon.setText(resultados[0][3])
        self.ui.Ideas.setText(resultados[0][4])
        self.ui.Reflexion.setPlainText(resultados[0][5])
        self.ui.SentimientosDropEdic.setCurrentIndex(res)

        self.LoadFeeling()
    def CleanText(self):
        self.ui.TituloEdit.setText("")
        #Vaciar Sentimiento ?
        self.ui.Razon.setText("")
        self.ui.Ideas.setText("")
        self.ui.Reflexion.setPlainText("")
    def DeleteEntry(self): 
        global EditingEntry
        ID = EditingEntry
        cursor.execute( "DELETE FROM Entradas WHERE ID = (?)",(ID,))
        db.commit()
        self.CleanText()
        self.ui.tabWidget.setCurrentIndex(0)
        for item in Entries:
            if (item.property("ID") == ID):
                layout = self.ui.scrollAreaContent.layout()
                layout.removeWidget(item)
                layout.addWidget(item)
                item.deleteLater()
                item = None      
    def ColorPick(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.ui.SentimientosColor.setStyleSheet("background-color: " + color.name())
    #############################
    def AddFeeling(self):
        Nombre = self.ui.SentimientosNombre.text()
        Color = self.ui.SentimientosColor.palette().color(1).name()
        try:
            cursor.execute(
                "INSERT INTO Sentimientos VALUES (?,?);",(Nombre,Color))
            db.commit()
        except:
            cursor.execute( "UPDATE Sentimientos SET Color = (?) WHERE Nombre = (?)",(Color,Nombre,))
            db.commit()
        self.ReloadFeelings()
    def ReloadFeelings(self):
        try:
            Feelings.clear()
            self.ui.SentimientosDrop.clear()
            self.ui.SentimientosDropEdic.clear()
            cursor.execute( "SELECT * FROM Sentimientos")
            Sentimientos = cursor.fetchall()
            for i in Sentimientos:
                self.ui.SentimientosDrop.addItem(i[0])
                self.ui.SentimientosDropEdic.addItem(i[0])
            for i in Entries:
                self.LeerEntrada(i.property("ID"))
                fln = self.ui.SentimientosDropEdic.currentText()
                color = self.ui.ColorEdit.palette().color(1).name()
                i.setStyleSheet("background-color: " + color)
                Feelings.append(fln)
            self.CleanText()
            self.MakeGraph()
        except:
            pass
    def LoadFeeling(self):
        try:
            text = self.ui.SentimientosDrop.currentText()
            self.ui.SentimientosNombre.setText(text)
            cursor.execute( "SELECT Color FROM Sentimientos WHERE Nombre = (?)", (text,))
            color = cursor.fetchall()
            self.ui.SentimientosColor.setStyleSheet("background-color: " + color[0][0])

            text = self.ui.SentimientosDropEdic.currentText()
            cursor.execute( "SELECT Color FROM Sentimientos WHERE Nombre = (?)", (text,))
            color = cursor.fetchall()
            self.ui.ColorEdit.setStyleSheet("background-color: " + color[0][0])
        except:
            pass
    def DeleteFeeling(self):
            text = self.ui.SentimientosDrop.currentText()
            ent = self.ui.SentimientosDrop.currentIndex()
            cursor.execute( "DELETE FROM Sentimientos WHERE Nombre = (?)",(text,))
            db.commit()
            self.ui.SentimientosDrop.removeItem(ent)
            self.ui.SentimientosDropEdic.removeItem(ent)
            self.ui.SentimientosDrop.setCurrentIndex(ent-1)
            self.ui.SentimientosDropEdic.setCurrentIndex(ent-1)
            self.ReloadFeelings()
            self.LoadFeeling()
    def MakeGraph(self):
        CleanFeels = []
        NumFeels = []
        ColorFeels = []
        for i in Feelings:
            num = CleanFeels.count(i)
            if num <= 0:
                CleanFeels.append(i)
                NumFeels.append(Feelings.count(i))
        for i in CleanFeels:
            cursor.execute( "SELECT Color FROM Sentimientos WHERE Nombre = (?)",(i,))
            Color = cursor.fetchall()
            ColorFeels.append(converTuple(Color[0]))
        mpl.subplot().pie(NumFeels,
        labels = CleanFeels,
        colors = ColorFeels,
        shadow = True)
        mpl.suptitle('Resumen global', fontsize=16)
        mpl.savefig(path + "graph.png")
        Pixmap = QtGui.QPixmap(path + "graph.png")
        self.ui.Graphic.setPixmap(Pixmap)
        mpl.cla()
        mpl.clf()
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())