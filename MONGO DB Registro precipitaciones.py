from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import ConnectionFailure

class Lluvias:
    def __init__(self, d=None,_id:int=0,precipitaciones:list=[]):
        if d is not None:
            self.__dict__ = d
        else:
            self._id = _id
            self.precipitaciones = precipitaciones
    
    def __str__(self):
        return f" Anyo :{self._id}"

def validar(mensaje:str, min:int, max:int)->int:
    while True:
        try:
            opcion = int(input( mensaje ))
            if opcion in range( min, max+1):
                return opcion
            else:
                print(f'Indica un valor entre {min} y {max}:')
        except Exception:
            print("Valor no valido")
            
def menu()->int:
    print("")
    print("MENU DE OPCIONES")
    print("=" * 35)
    print("1.- OBTENER PRECIPITACIONES")
    print("2.- ANALISIS ANUAL")
    print("3.- DESVIACION ANUAL")
    print("4.- HISTORICO MEDIA")
    print("5.- HISTORICO TOTAL")
    print("6.- CORTE ANUAL")
    print("7.- CORTE HISTORICO")
    print("8.- EXTREMOS ANUALL")
    print("9.- EXTREMOS HISTORICO")
    print("0.- SALIR")
    print("")
    return validar('Indica una opcion: ', 0, 10)


##def obtener_para_insertar( anyo):
##    obj = None
##    conexion = MongoClient("mongodb://127.0.0.1:27017")
##    try:
##        documento = conexion.lluvias.registro.find_one({"_id":anyo})
##        if documento is not None:
##            obj = Lluvias(documento)
##            return obj
##        else:
##            return None
##    except ConnectionFailure:
##        print("Servidor no encontrado")
##
##def insertar( objeto):
##    conexion = MongoClient("mongodb://127.0.0.1:27017")
##    try:
##        resultado = conexion.lluvias.registro.insert_one(objeto.__dict__)
##    except ConnectionFailure:
##        print("Servidor no encontrado")

def obtener( anyo,mes):
    obj = None
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documento = conexion.lluvias.registro.find_one({"_id":anyo})
        if documento is not None:
            obj = Lluvias(documento)
            return obj.precipitaciones[mes]
        else:
            return None
    except ConnectionFailure:
        print("Servidor no encontrado")

def analisis_anual(anyo):
    dic_registro = {}
    obj = None
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documento = conexion.lluvias.registro.find_one({"_id":anyo})
        if documento is not None:
            obj = Lluvias(documento)
            dic_registro["Regs"] = obj.precipitaciones
            dic_registro["Total"] = sum(obj.precipitaciones)
            dic_registro["Media"] = sum(obj.precipitaciones)/12
            return dic_registro
        else:
            return None
    except ConnectionFailure:
        print("Servidor no encontrado")
        
def desviacion_anual(anyo):
    lista = []
    obj = None
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documento = conexion.lluvias.registro.find_one({"_id":anyo})
        if documento is not None:
            obj = Lluvias(documento)
            media = sum(obj.precipitaciones)/12
            for precipitacion in obj.precipitaciones:
                lista.append(precipitacion - media)
            return lista
        else:
            return None
    except ConnectionFailure:
        print("Servidor no encontrado")

def historico_media():
    lista = []
    dic_registro = {}
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documentos = conexion.lluvias.registro.find()
        for documento in documentos:
            lista.append(Lluvias(documento))
        for elemento in lista:
            dic_registro[elemento._id] = sum(elemento.precipitaciones)/12
        return dic_registro
    except ConnectionFailure:
        print("Servidor no encontrado")

def historico_total():
    lista = []
    dic_registro = {}
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documentos = conexion.lluvias.registro.find()
        for documento in documentos:
            lista.append(Lluvias(documento))
        for elemento in lista:
            dic_registro[elemento._id] = sum(elemento.precipitaciones)
        return dic_registro
    except ConnectionFailure:
        print("Servidor no encontrado")

def corte_anual(anyo,cantidad):
    mes = 0
    dic_registro = {}
    dic_registro["Meses Humedos"] = []
    dic_registro["Meses Secos"] = []
    obj = None
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documento = conexion.lluvias.registro.find_one({"_id":anyo})
        if documento is not None:
            obj = Lluvias(documento)
            for lluvia in obj.precipitaciones:
                mes+=1
                if lluvia > cantidad :
                    dic_registro["Meses Humedos"].append(mes)
                else:
                    dic_registro["Meses Secos"].append(mes)           
            return dic_registro
        else:
            return None
    except ConnectionFailure:
        print("Servidor no encontrado")

def corte_historico(cantidad):
    lista = []
    dic_registro = {}
    dic_registro["Años Humedos"] = []
    dic_registro["Años Secos"] = []
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documentos = conexion.lluvias.registro.find()
        for documento in documentos:
            lista.append(Lluvias(documento))
        for anyo in lista:
            suma = sum(anyo.precipitaciones)
            if suma > cantidad :
                dic_registro["Años Humedos"].append(anyo._id)
            else:
                dic_registro["Años Secos"].append(anyo._id)
        return dic_registro                   
    except ConnectionFailure:
        print("Servidor no encontrado")    

def extremo_anual(anyo):
    mes_seco= 1
    mes_humedo = 1
    dic_registro = {}
    obj = None
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documento = conexion.lluvias.registro.find_one({"_id":anyo})
        if documento is not None:
            obj = Lluvias(documento)
            maximo=max(obj.precipitaciones)
            minimo = min(obj.precipitaciones)
            for lluvia in obj.precipitaciones:
                if lluvia == maximo:
                    dic_registro["Mes más Humedo"] = mes_humedo
                else:
                    mes_humedo += 1
            for lluvia in obj.precipitaciones:
                if lluvia == minimo:
                    dic_registro["Mes más Seco"] = mes_seco
                else:
                    mes_seco += 1                     
            return dic_registro
        else:
            return None
    except ConnectionFailure:
        print("Servidor no encontrado")    
    
def extremo_historico():
    lista = []
    dic_humedos = {}
    dic_secos = {}
    dic_final = {}
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        documentos = conexion.lluvias.registro.find()
        for documento in documentos:
            lista.append(Lluvias(documento))        
        for objeto in lista:
                dic_humedos[objeto._id] = max(objeto.precipitaciones)
                dic_secos[objeto._id] = min(objeto.precipitaciones)
        lluvia_max = max(dic_humedos.values())
        lluvia_min = min(dic_secos.values())
        for año, lluvia in dic_humedos.items():
            if lluvia == lluvia_max:
                dic_final["Anyo Más Humedo"] = año
        for año, lluvia in dic_secos.items():
            if lluvia == lluvia_min:
                dic_final["Anyo Más Seco"] = año
        return dic_final
        
    except ConnectionFailure:
        print("Servidor no encontrado")    


def main():

    while True:
        opcion = menu()
        
##        if opcion == 10:
##            documento = {}
##            documento["_id"] = int(input("Introduzca el anyo: "))
##            objeto =obtener_para_insertar(documento["_id"])
##            if objeto is not None:
##                print("Anyo ya registrado.")
##            else:
##                documento["precipitaciones"] = [22,42,56,34,84,94,12,54,94,98,66,88]
##                objeto = Lluvias(documento)
##                insertar(objeto)
##                print("Anyo y precipitacion agregados correctamente")                       

        if opcion == 1:
            año = validar("Indique el anyo: ",1980,2020)
            mes = validar("Indique el mes: ", 1, 12)
            precipitacion = obtener(año,mes-1)
            if precipitacion is not None:
                  print(f"Las precipitaciones del mes numero {mes} son de: {precipitacion}")
            else:
                print("Año no registrado.")
            
        elif opcion == 2:
            año = validar("Indique el anyo: ",1980,2020)
            dic_registro= analisis_anual(año)
            for clave, valor in dic_registro.items():
                print(clave, valor)

        elif opcion == 3:
            año = validar("Indique el anyo: ",1980,2020)            
            lista=desviacion_anual(año)
            print(f"La desviacion de cada mes respecto a la media anual es {lista}")

        elif opcion == 4:
            dic_registro = historico_media()
            for año, media in dic_registro.items():
                print(f"El año {año} la media anual de precipitaciones fue {media}")
                
        elif opcion == 5:
            dic_registro = historico_total()
            for año, suma in dic_registro.items():
                print(f"El año {año} la suma anual de precipitaciones fue {suma}")

        elif opcion == 6:
            año = validar("Indique el anyo: ",1980,2020)
            cantidad = int(input("Indique una cantidad: "))
            dic_registro = corte_anual(año,cantidad)
            for clave,valor in dic_registro.items():
                print(f" Los {clave} han sido {valor} ")

        elif opcion == 7:
            cantidad = int(input("Indique una cantidad: "))
            dic_registro = corte_historico(cantidad)
            for clave, valor in dic_registro.items():
                print(f" Los {clave} han sido {valor}")
            
        elif opcion == 8:
            año = validar("Indique el anyo: ",1980,2020)
            dic_registro = extremo_anual(año)
            for clave, valor in dic_registro.items():
                print(f" El año {año} el {clave} ha sido el {valor}")

        elif opcion == 9:
            dic_registro = extremo_historico()
            for clave, valor in dic_registro.items():
                print(f" El {clave} ha sido : {valor}")
                
        elif opcion == 0:
            print("Adios")
            print("Fin del programa")
            break
        

if __name__ == '__main__':
    main()
