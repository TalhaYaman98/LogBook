import sys
import pandas as pd
import csv, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from Interface import Ui_MainWindow
from datetime import datetime

class defter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("resim.jpg"))  # Set the window icon
        self.setToolTip("Devam Et")  # Set the tooltip text
        self.msg = QMessageBox()  # Initialize a message box
        self.simdi = datetime.now()  # Get the current date and time

        # Connect buttons to their respective methods
        self.ui.pushButton.clicked.connect(self.kayit)
        self.ui.pushButton_2.clicked.connect(self.goster)
        self.ui.pushButton_3.clicked.connect(self.istatis)
        self.ui.pushButton_4.clicked.connect(self.sil)

        # Populate list widgets with existing CSV files from the directory
        result = os.listdir("C:/Users/Talha/Documents/OdaVerileri")
        for dosya in result:      
            if dosya.endswith(".csv"):
                self.ui.listWidget.addItem(str(dosya))
                self.ui.listWidget_2.addItem(str(dosya))
                self.ui.listWidget_3.addItem(str(dosya))
        self.ui.listWidget.setCurrentRow(0)
        self.ui.listWidget_2.setCurrentRow(0)
        self.ui.listWidget_3.setCurrentRow(0)

    def kayit(self):
        # Get data from the line edit and split it into a list
        veriler = self.ui.lineEdit.text()
        verilerliste = veriler.split()
        if len(verilerliste) != 7:
            # Show an error message if there are not exactly 7 items
            print(len(verilerliste))
            self.msg.setText("KAYIT BAŞARISIZ")  # Registration failed
            self.msg.setWindowTitle("hata")  # Error
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.show()
        else:
            pass

        Taslak = ["Oda", "İşlem", "Hava", "Isı", "Nem", "Kasa", "Gün", "Tarih"]
        verilerliste.append(str(self.simdi.date()))  # Append current date to the data

        dosyalistesi = []
        dosyalar = os.listdir("C:/Users/Talha/Documents/OdaVerileri")
        for dosya in dosyalar:      
            if dosya.endswith(".csv"):
                dosyalistesi.append(str(dosya))
        
        oda = ""
        for j in dosyalistesi:
            if j == F"{verilerliste[0]}.csv":
                oda = j
                break
            else:
                pass

        if oda == F"{verilerliste[0]}.csv":
            # If a file for the room already exists, append data to it
            with open(f"C:/Users/Talha/Documents/OdaVerileri/{oda}", "a", encoding="utf-8") as defter:
                yazici = csv.writer(defter)
                yazici.writerow("")
                yazici.writerow(verilerliste)
                print("kayıt etti")  # Registered
                print(verilerliste)

                self.msg.setText("KAYIT EDİLDİ")  # Data recorded
                self.msg.setWindowTitle("BAŞARILI")  # Successful
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.show()

        if oda == "":
            oda = f"oda{len(dosyalistesi)+1}"
            print(oda)
            if oda == F"{verilerliste[0]}":
                # If no existing file is found, create a new one and write the data
                with open(f"C:/Users/Talha/Documents/OdaVerileri/{oda}.csv", "w", encoding="utf-8") as deft:
                    yazi = csv.writer(deft)
                    yazi.writerow(Taslak)
                    yazi.writerow("")
                    yazi.writerow(verilerliste)
                    print("kayıt etti")  # Registered
                    print(verilerliste)
                    
                    # Update list widgets with the new file list
                    result = os.listdir("C:/Users/Talha/Documents/OdaVerileri")
                    self.ui.listWidget_2.clear()
                    self.ui.listWidget.clear()
                    self.ui.listWidget_3.clear()
                    for dosya in result:      
                        if dosya.endswith(".csv"):
                            self.ui.listWidget_2.addItem(str(dosya))
                            self.ui.listWidget.addItem(str(dosya))
                            self.ui.listWidget_3.addItem(str(dosya))
                    self.ui.listWidget_2.setCurrentRow(0)
                    self.ui.listWidget.setCurrentRow(0)
                    self.ui.listWidget_3.setCurrentRow(0)

                    self.msg.setText("YENİ DOSYA AÇILDI")  # New file created
                    self.msg.setWindowTitle("BAŞARILI")  # Successful
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setStandardButtons(QMessageBox.Ok)
                    self.msg.show()
            else:
                pass

        self.ui.lineEdit.clear()  # Clear the input field

    def goster(self):
        # Show the contents of the selected CSV file in the text edit widget
        index = self.ui.listWidget_2.currentRow()
        item = self.ui.listWidget_2.item(index)
        adres = f"C:/Users/Talha/Documents/OdaVerileri/{str(item.text())}"

        df = pd.read_csv(f"C:/Users/Talha/Documents/OdaVerileri/{str(item.text())}")
        sayac = 0
        for i in df["Gün"]:
            sayac += 1

        result = df.head(sayac)
        veri = str(result)

        self.ui.textEdit.setText(veri.replace(" ", "  "))  # Display data in text edit widget

    def sil(self):
        # Delete the selected CSV file
        index = self.ui.listWidget_2.currentRow()
        item = self.ui.listWidget_2.item(index)
        if item is None:
            return
        q = QMessageBox.question(self, "OdaSilme", "Emin misin?: " + item.text(), QMessageBox.Yes | QMessageBox.No)
        if q == QMessageBox.Yes:
            item = self.ui.listWidget_2.takeItem(index)
            os.remove(f"C:/Users/Talha/Documents/OdaVerileri/{str(item.text())}")
            del item

        # Update list widgets after deletion
        result = os.listdir("C:/Users/Talha/Documents/OdaVerileri")
        self.ui.listWidget.clear()
        self.ui.listWidget_3.clear()
        for dosya in result:      
            if dosya.endswith(".csv"):
                self.ui.listWidget.addItem(str(dosya))
                self.ui.listWidget_3.addItem(str(dosya))
                self.ui.listWidget.setCurrentRow(0)
                self.ui.listWidget_3.setCurrentRow(0)

    def istatis(self):
        # Placeholder method for future statistics functionality
        pass

deft = QApplication(sys.argv)
penc = defter()
penc.show()
deft.exec_()
