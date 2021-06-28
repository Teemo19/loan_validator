import requests
import re
from datetime import datetime as dt

parameters = {'paterno': 'MALDONADO','materno':'MENDOZA','nombre':'CELSO ALEJANDRO','dia':'19','mes':'12','anio':'1994','sexo':'H','entidad':'CM'}
#parameters = {'paterno': 'Romero','materno':'Sanchez','nombre':'Xochitl','dia':'10','mes':'07','anio':'1995','sexo':'M','entidad':'JC'}

class CURP:
    def __init__(self,parameters):
            # DEFINIMOS FUNCION PARA QUITAR ACENTOS
            a,b = 'áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU'
            trans = str.maketrans(a,b)
            self.pstCURP   = ""
            self.pstNombre = parameters['nombre'].upper().translate(trans) #QUITAMOS ACENTOS
            self.pstPaterno = parameters['paterno'].upper().translate(trans)#     ||
            self.pstMaterno = parameters['materno'].upper().translate(trans)#     ||
            self.dfecha = ''.join([parameters['anio'][2:],parameters['mes'],parameters['dia']])
            self.pstSexo = parameters['sexo'].upper()
            self.pnuCveEntidad = parameters['entidad'].upper()
            if(len(self.pstNombre.split(' '))>1):
                blacklist=["JOSE","MARIA","MA.","MA"]
                nombres = self.pstNombre.split(' ')
                if(nombres[0] in blacklist and nombres[1] not in blacklist):
                    del nombres[0]
                    self.pstNombre = nombres[0]
            self.add_dataToCurp(self.pstPaterno[:2])
            self.add_dataToCurp(self.pstMaterno[:1])
            self.add_dataToCurp(self.pstNombre[:1])
            self.add_dataToCurp(self.dfecha)
            self.add_dataToCurp(self.pstSexo)
            self.add_dataToCurp(self.pnuCveEntidad)
            self.add_dataToCurp(self.find_firstConsonant(self.pstPaterno))
            self.add_dataToCurp(self.find_firstConsonant(self.pstMaterno))
            self.add_dataToCurp(self.find_firstConsonant(self.pstNombre))
            self.contador = 18
            self.contador1 = 0
            self.valor = 0
            self.sumatoria = 0
            self.calculate_last_digits()

    def add_dataToCurp(self,text):
        self.pstCURP+=text.upper()
        
    def find_firstConsonant(self,text):
        vocals =['A','E','I','O','U','a','e','i','o','u']
        counter = 0
        for letter in text:
            if(letter not in vocals):
                counter+=1
            if(counter == 2):
                return letter

    def calculate_last_digits(self):
        #range of condicional letters
        condiciones = list()
        anio = self.dfecha[:2]
        condiciones.extend([str(i) for i in range(10)])
        condiciones.extend([chr(i) for i in range(65,79)])
        condiciones.extend(['Ñ'])
        condiciones.extend([chr(i) for i in range(79,91)])
        if (int(anio) > int(dt.now().strftime("%y"))):
            pstDigSig = '0'
        elif (int(anio) <= int(dt.now().strftime("%y"))):
            pstDigSig = 'A'
        self.add_dataToCurp(pstDigSig)
        while(True):
            if(self.contador1 > 16):
                break
            for i in range(37):
                pstCom = self.pstCURP[self.contador1]
                if(pstCom == condiciones[i]):
                    self.valor = i * self.contador
                    break
            self.contador  -= 1 
            self.contador1 += 1
            self.sumatoria += self.valor
        numVer  = str(abs((self.sumatoria % 10) - 10))
        if(numVer == '10'):
            numVer = '0'
        self.add_dataToCurp(numVer)

class RFC:
    def __init__(self,parameters):
        # DEFINIMOS FUNCION PARA QUITAR ACENTOS
        a,b = 'áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU'
        trans = str.maketrans(a,b)
        self.pstRFC   = ""
        self.pstNombre = parameters['nombre'].upper().translate(trans) #QUITAMOS ACENTOS
        self.pstPaterno = parameters['paterno'].upper().translate(trans)#     ||
        self.pstMaterno = parameters['materno'].upper().translate(trans)#     ||
        self.dfecha = ''.join([parameters['anio'][2:],parameters['mes'],parameters['dia']])
        self.pstSexo = parameters['sexo'].upper()
        self.pnuCveEntidad = parameters['entidad'].upper()    
        # delete names jose & maria 
        if(len(self.pstNombre.split(' '))>1):
            blacklist=["JOSE","MARIA","MA.","MA"]
            nombres = self.pstNombre.split(' ')
            if(nombres[0] in blacklist and nombres[1] not in blacklist):
                del nombres[0]
                self.pstNombre = nombres[0]
        self.add_dataToRFC(self.pstPaterno[:2])
        self.add_dataToRFC(self.pstMaterno[:1])
        self.add_dataToRFC(self.pstNombre[:1])
        self.add_dataToRFC(self.dfecha)

    def add_dataToRFC(self,text):
        self.pstRFC+=text.upper()
