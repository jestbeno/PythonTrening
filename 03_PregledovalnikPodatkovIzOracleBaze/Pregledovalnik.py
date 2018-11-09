# ena prvih aplikacij, kjer sem uporabljal PyQt5 in Oracle
# funkcionalna ampak slaba praksa v vseh pogledih

from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets, uic
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout,  QMessageBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pandas as pd
from matplotlib.dates import DateFormatter
import re
from datetime import *
import numpy as np

############################## CONNECT TO ORACLE DATABASE ################################
import cx_Oracle

dsn_tns = cx_Oracle.makedsn('tajfun.arso.sigov.si', 1521, service_name='tajfun.arso.sigov.si')

# Files
UIFile = "Pregledovalnik4.ui"
StyleFile = "Pregledovalnik.qss"
UI_MainWindow, QtBaseClass = uic.loadUiType(UIFile)

class MainWindow(QMainWindow,UI_MainWindow ):
    def __init__(self, **meminfo):
        super().__init__()

        self.setupUi(self)

        self.nastaviDatumInCas()

        self.tidalDataFile = ""
        self.IzbranaPostaja = "Crnuce"
        self.SifraIzbranePostaje = 4982
        self.Postaje()
        self.__vodostaj = meminfo.get('vodostaj', )
        self.__datumCasKontrolneMeritve = meminfo.get('datumCasKontrolneMeritve', '')
        self.__temperatura = meminfo.get('temperatura','' )

        self.setStyleSheet(open(StyleFile, "r").read())
        self.setWindowTitle("Pregledovalnik")
        self.showMaximized()
        self.statusBar().addWidget(QLabel("Aplikacija je izdelana IZKLJUČNO ZA PRIPRAVLJENE PODATKE!!"))
        self.exitAction.triggered.connect(self.ZapriOkno)
        self.ActionOprogramu.triggered.connect(self.OpisPrograma)
        self.actionNavodilo_za_uporabo.triggered.connect(self.NavodiloZaUporabo)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.BTNKontrolneMeritve.clicked.connect(self.plotKontrolna)
        self.BTNKontrolneMeritve.setStatusTip('Klikni za vnos kontrolnih meritev iz baze!')
        self.BTNDataloger.setStatusTip('Klikni za izris grafa!')
        self.BTNDataloger.clicked.connect(self.plotDataloger)
        self.BTNIzhod.clicked.connect(self.ZapriOkno)

        container = self.graphicsView
        layout = QVBoxLayout(container)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

    @property
    def vodostaj(self):
        return self.__vodostaj
    @property
    def temperatura(self):
        return self.__temperatura
    @property
    def datumCasKontrolneMeritve(self):
        return self.__datumCasKontrolneMeritve
    @vodostaj.setter
    def vodostaj(self, vodostaj):
        self.__vodostaj = vodostaj
    @datumCasKontrolneMeritve.setter
    def datumCasKontrolneMeritve(self, datumCasKontrolneMeritve):
        self.__datumCasKontrolneMeritve = datumCasKontrolneMeritve
    @temperatura.setter
    def temperatura(self, temperatura):
        self.__temperatura = temperatura

    def plotKontrolna(self):
        con = cx_Oracle.Connection(user="nucic", password="BNucic", dsn=dsn_tns)
        IzborKolicine = 1
        if self.RadioButtonH.isChecked():
            IzborKolicine = 1
            self.figure.clf()
            plt.grid()
        elif self.RadioButtonT.isChecked():
            IzborKolicine = 3
            self.figure.clf()
            plt.grid()

        with con as conn:
            cursor = conn.cursor()
            OdCasovnoObdobje = self.DateEditZacetek.dateTime().toPyDateTime()
            DOCasovnoOBdobje = self.DateEditKonec.dateTime().toPyDateTime()
            HP_ID = self.SifraIzbranePostaje
            cursor.execute("select * from HIDR.KATHP_KONTROLNA_MERITEV where TP_MER_KOL = :1 and HP_ID = :2 AND KM_CAS BETWEEN :3 and :4",(IzborKolicine, HP_ID, OdCasovnoObdobje,DOCasovnoOBdobje,))
            cursor.arraysize = 256

            result = cursor.fetchall()
            vodostaj = []
            temperatura = []
            datumCas = []
            if IzborKolicine ==1:
                for row in result:
                    self.__vodostaj = row[4] / 100
                    vodostaj = np.append(vodostaj, self.__vodostaj)
                    self.__datumCasKontrolneMeritve= row[3]
                    datumCas =np.append(datumCas,self.__datumCasKontrolneMeritve)
                eltra = self.figure.add_subplot(111)
                eltra.scatter(datumCas, vodostaj, label='H Kontrolna', linewidth=1, color='b')
                eltra.set_ylabel('Vodostaj [m]')
                eltra.set_xlabel('Datum in ura')
                formatter = DateFormatter('%d.%m.%y %H:%M')

                plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
                plt.legend()
                self.canvas.draw()
            if IzborKolicine == 3:
                for row in result:
                    self.__temperatura = row[4]
                    temperatura = np.append(temperatura, self.__temperatura)
                    self.__datumCasKontrolneMeritve = row[3]
                    datumCas = np.append(datumCas, self.__datumCasKontrolneMeritve)
                eltra = self.figure.add_subplot(111)
                eltra.scatter(datumCas, temperatura, label='T Kontrolna', linewidth=1, color='r')
                eltra.set_ylabel('Temperatura [°C]')
                eltra.set_xlabel('Datum in ura')
                formatter = DateFormatter('%d.%m.%y %H:%M')
                plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
                plt.legend()
                self.canvas.draw()
        con.close()

    def plotDataloger(self):
        cas,Heltra = self.beriPodatkeDataloger()
        eltra = self.figure.add_subplot(111)
        eltra.plot(Heltra, cas, label='ELTRA', color='y')
        formatter = DateFormatter('%d.%m %H:%M')
        plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
        plt.legend()
        plt.grid()
        self.canvas.draw()
    def beriPodatkeDataloger(self):
        if self.RadioButtonH.isChecked():
            # self.figure.clf()
            plt.grid()
            self.tidalDataFile = ("3550_crnuceH.txt")
        elif self.RadioButtonT.isChecked():
            # self.figure.clf()
            plt.grid()
            self.tidalDataFile = ("3550_crnuceT.txt")
        f = open(self.tidalDataFile, 'r')
        tidal_df = pd.read_table(self.tidalDataFile, sep=';', names=["date", "time","elev"])
        Heltra = tidal_df.elev
        times = []
        for line in f:
            m = re.findall(r'([\w\.\w\:]+)', line)
            datevec = m[0] + " " + m[1]
            datumskiobjekt1 = datetime.strptime(datevec, "%d.%m.%Y %H:%M:%S")
            times = np.append(times, datumskiobjekt1)
            # print (datumskiobjekt1)
        return Heltra,times
    ''' ---------------------------------------------
    OBVESTILA IN NAVODILA..
    ----------------------------------------------'''
    def Obvestilo(self,tekst):
        QMessageBox.about(self,"Obvestilo", tekst)

    def nastaviDatumInCas(self):
        # self.DatumPrvegaObiska.setDateTime(QtCore.QDateTime.currentDateTime())
        ZacetniCas = QtCore.QDateTime(2017, 1, 1, 0, 0)
        self.DateEditZacetek.setDateTime(ZacetniCas)
        # print (self.DateEditZacetek.text())
        KoncniCas = QtCore.QDateTime(2018, 6, 30, 23,00)
        self.DateEditKonec.setDateTime(KoncniCas)

    def ZapriOkno(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Opozorilo')
        box.setText('Res želiš zaključiti z delom?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Da')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('Ne')
        box.exec_()
        if box.clickedButton() == buttonY:
            self.close()
        elif box.clickedButton() == buttonN:
            pass

    def OpisPrograma(self):
        QMessageBox.about(self,"Obvestilo", "Program za pomoč pri pregledovanju podatkov Datalogerjev in kontrolnih meritev.."
                                "\n"
                                "\n"
                                "Izdelal: Benjamin Nučič"
                                "\n"
                                "Program je izdelan izključno za PRIPRAVLJENE podatke iz programa HydRas!!")
    def NavodiloZaUporabo(self):
        QMessageBox.about(self,"Navodilo za uporabo:",
                                "1. Klikni na gumb: >>Vnos podatkov kontrolnih meritev<<, prenesle se bodo kontrolne meritve določenega obdobja iz baze.."
                                "\n"
                                "2. Klikni na gumb: >>Vnos podatkov Datalogerja<<,(izhodni podatki iz Hydras-a) nato klikneš >>Izriši graf<<" 
                                "\n"
                                "\n"
                                )


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
