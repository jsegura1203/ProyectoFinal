import serial as connector
import sys

from PyQt5 import uic, QtWidgets

import KNN
import discretizador_proy

qtCreatorFile = "proyecto.ui"  # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_conectar.clicked.connect(self.conectar)
        self.btn_iniciar.clicked.connect(self.iniciar)
        self.btn_resultados.clicked.connect(self.resultados)
        self.arduino = None
        self.nombre="plantas"
        self.cargar()
        self.fila=0
        self.datos=[]
        self.respuestas=""
        self.lista=[]

    # Área de los Slots
    def cargar(self):
        discretizador_proy.discretizador("plantas")

    def resultados(self):
        self.lista[0] = self.txt_atributo1.text()
        self.lista[1] = self.txt_atributo2.text()
        self.lista[2] = self.txt_atributo3.text()
        self.lista[3] = self.txt_atributo4.text()
        self.lista=list(map(float, self.lista))
        valor=KNN.metodo(self.lista[0:len(self.lista)-1], self.nombre+"_generado.csv")
        self.respuestas=valor
        valor=float(self.respuestas[0])
        if(valor==1):
            cadena="Riego abundante\n"
        else:
            if(valor==2):
                cadena="Riego medio\n"
            else:
                cadena="No regar\n"
        self.arduino.write(cadena.encode())

    def conectar(self):
        try:
            if self.arduino == None:
                com = "COM"+ self.txt_com.text()
                self.arduino =  connector.Serial(com, baudrate=9600, timeout=1)  #Establece la conexion por primera vez
                print("Conexión Inicializada")
                self.btn_conectar.setText("DESCONECTAR")
                self.txt_com.setEnabled(False)
            elif self.arduino.isOpen(): ##otra opción: checar que el texto del boton sea desconectar
                self.btn_conectar.setText("RECONECTAR")
                self.arduino.close()
                print("Conexion Cerrada")
            else:
                self.btn_conectar.setText("DESCONECTAR")
                self.arduino.open()
                print("Conexion Reconectada")
        except Exception as e:
            print(str(e))

    def iniciar(self):
        flag=True
        if self.arduino != None:
            if self.arduino.isOpen():  ##otra opción: checar que el texto del boton sea desconectar
                try:
                    while(flag):
                        self.lista=self.leer()
                        if(self.lista!=None):
                            print(self.lista)
                            if(len(self.lista)==5):
                                if(self.lista[4]=="1"):
                                    flag=False
                    if(flag==False):
                        self.txt_atributo1.setText(self.lista[0]+"")
                        self.txt_atributo2.setText(self.lista[1]+"")
                        self.txt_atributo3.setText(self.lista[2]+"")
                        self.txt_atributo4.setText(self.lista[3]+"")

                except Exception as e:
                    print(str(e))
            else:
                print("La conexión esta cerrada actualmente")
        else:
            print("Aun no se ha realizado la conexion con Arduino")

    def leer(self):
        cadena = self.arduino.readline().decode().strip("\r\n")
        if(cadena!=""):
            if(cadena[0]=="I" and cadena[len(cadena)-1]=="T"):
                cadena=cadena[1:len(cadena)-1]
                lista=cadena.split(";")
                return lista


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

