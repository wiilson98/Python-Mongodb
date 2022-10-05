from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import ConnectionFailure
from datetime import datetime

class Cliente:
    def __init__(self,d =None, dni:str="0", nombre:str="0", cuentas:list=[]):
        if d is not None:
            self.__dict__ = d
        else:            
            self._id = dni
            self.nombre = nombre
            self.cuentas = cuentas

    def __str__(self):
        return f"Dni: {self._id} Nombre: {self.nombre}"

class Cuenta:   
    def __init__(self, d=None, ncuenta:str = "0", saldo:float = 0, interes:float = 0, bonificacion:float = 0):
        if d is not None:
            self.__dict__ = d
        else:
            self._id = ncuenta
            self.saldo = saldo
            self.interes = interes
            if bonificacion > 0:
                self.bonificacion = bonificacion
            self.fecha = datetime.datetime.now()
    def ingresar(self, cantidad):
        self.saldo += cantidad
    def retirar(self, cantidad):
        self.saldo -= cantidad
    def beneficio(self):
        return self.saldo * self.interes
    def __str__(self):
        return "Ncuenta: {} saldo: {} interes: {}".format(self._id, self.saldo, self.interes)

def actualizar( objeto,opc):
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        if opc == 1:
            resultado = conexion.banco.cuentas.replace_one({"_id":objeto._id}, objeto.__dict__ )
            return resultado.modified_count > 0
        else:
            resultado = conexion.banco.clientes.replace_one({"_id":objeto._id}, objeto.__dict__ )
            return resultado.modified_count > 0            
    except ConnectionFailure:
        print("Servidor no encontrado")

def eliminar( cuenta ):
    conexion = MongoClient("mongodb://127.0.0.1:27017")    
    try:
        resultado = conexion.banco.cuentas.delete_one({"_id":cuenta._id})
    except ConnectionFailure:
        print("Servidor no encontrado")
    return resultado.deleted_count > 0

def insertar( objeto,opcion):
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        if opcion == 1:
            resultado = conexion.banco.cuentas.insert_one(objeto.__dict__)
        else:
            resultado = conexion.banco.clientes.insert_one(objeto.__dict__)
    except ConnectionFailure:
        print("Servidor no encontrado")
    return resultado.inserted_id

def listar(opcion):
    lista = []
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        if opcion == 1:
            documentos = conexion.banco.cuentas.find()
            # Obtencion de documentos
            for documento in documentos:
            # Instanciacion de cada cuenta y añadido a la lista de cuentas
                lista.append(Cuenta(documento))
            return lista
        else:
            documentos = conexion.banco.clientes.find()
            for documento in documentos:
                lista.append(Cliente(documento))
            return lista
    except ConnectionFailure:
        print("Servidor no encontrado")
    # Recorrido de lista de objetos cuenta resultantes

def obtener( n_ide,opc):
    obj = None
    conexion = MongoClient("mongodb://127.0.0.1:27017")
    try:
        if opc ==1:
            documento = conexion.banco.cuentas.find_one({"_id":n_ide})
            if documento is not None:
                obj = Cuenta(documento)
                return obj
        else:
            documento = conexion.banco.clientes.find_one({"_id":n_ide})
            if documento is not None:
                obj= Cliente(documento)
                return obj
    except ConnectionFailure:
        print("Servidor no encontrado")
# "recibe un dni y retorna la suma de saldos del cliente"       
def suma_saldos(dni):
    suma = 0
    opc = 2
    cliente = obtener(dni,opc)
    for cuenta in cliente.cuentas:
        opc = 1
        obj = obtener(cuenta,opc)
        suma += obj.saldo
    return suma

#" recibe un dni y retorna una lista con los objetis cuentas del dni indicado"    
def obtener_cuentas(dni):
    lista_cuentas = []
    opc = 2
    cliente = obtener(dni,opc)
    for cuenta in cliente.cuentas:
        opc = 1
        obj = obtener(cuenta,opc)
        lista_cuentas.append(obj)
    return lista_cuentas

#"recibe un ncuenta y retorna el objeto del cliente"
def obtener_cliente(ncuenta):
    opc = 1
    cuenta = obtener(ncuenta,opc)
    opc = 2
    lista_clientes = listar(opc)
    for cliente in lista_clientes:
        if cuenta._id in cliente.cuentas:
            return cliente
                
def menu():
    while True:
        print("")
        print("OPCIONES")
        print("1.- LISTA CLIENTES")
        print("2.- LISTA CUENTAS")
        print("3.- MOSTRAR CUENTA")
        print("4.- INGRESAR")
        print("5.- RETIRAR")
        print("6.- BENEFICIO")
        print("7.- ALTA CLIENTE")
        print("8.- ALTA CUENTA")
        print("9.- ELIMINAR CUENTA")
        print("")
        try:
            opcion = int(input("Indica una opcion: "))
            print("")
            if 0 <= opcion <= 9:                                       
                return opcion
            else:
                print("Opcion incorrecta.")
        except ValueError:
            print("Valor no valido.")

def main():
    
    while True:
        try:
            
            opcion = menu()
            
            if opcion == 1:
                
                opc = 2
                clientes = listar(opc)
                if len(clientes) > 0:
                    print("LISTA DE CLIENTES: ")
                    for cliente in clientes:
                        print(cliente)
                else:
                    print("No hay clientes registrados.")

            if opcion == 2:
                
                dni = input("Introduzca el dni: ")
                opc = 2
                cliente = obtener(dni,opc)
                if cliente is not None:
                    if len(cliente.cuentas) > 0:
                        cuentas = obtener_cuentas(dni)
                        print("Cuentas: ")
                        for cuenta in cuentas:
                            print(cuenta)
                        print(f"El sumatorio de capital de todas las cuentas es de:{suma_saldos(dni)} $")
                    else:
                        print("El cliente no tiene cuentas registradas")
                else:
                    print("Error.Cliente inexistente.")

            if opcion == 3:
                
                opc = 1
                ncuenta = input("Introduzca el numero de cuenta: ")
                cuenta = obtener(ncuenta,opc)
                if cuenta is not None:
                    cliente = obtener_cliente(cuenta._id)
                    print(cliente)
                    print(cuenta)                    
                else:
                    print("Error.Cuenta inexistente.")

            if opcion == 4:
                
                opc = 1
                ncuenta = input("Introduzca el numero de cuenta: ")
                cuenta = obtener(ncuenta,opc)
                if cuenta is not None:
                    cantidad = float(input("Introduzca la cantidad a INGRESAR: "))
                    if cantidad > 0:
                        cuenta.ingresar(cantidad)
                        actualizar(cuenta,opc)
                        print("Ingreso realizado correctamente.")
                        print(f"Nuevo saldo {cuenta.saldo}$")
                    else:
                        print("Error.La cantidad no puede ser negativa.")
                else:
                    print("Error.Cuenta inexistente.")
                    
            if opcion == 5:
                
                opc = 1
                ncuenta = input("Introduzca el numero de cuenta: ")
                cuenta = obtener(ncuenta,opc)
                if cuenta is not None:
                    cantidad = float(input("Introduzca la cantidad a RETIRAR: "))
                    if cantidad > 0:
                        if cantidad < cuenta.saldo:
                            cuenta.retirar(cantidad)
                            actualizar(cuenta,opc)
                            print("Retiro realizado correctamente.")
                            print(f"Nuevo saldo {cuenta.saldo}$")
                        else:
                            print("Error.Retiro superior al saldo disponible.")
                    else:
                        print("Error. El retiro no puede ser negativo.")
                else:
                    print("Error.Cuenta inexistente.")            

            if opcion == 6:
                
                opc = 1
                ncuenta = input("Introduzca el numero de cuenta: ")
                cuenta = obtener(ncuenta,opc)
                if cuenta is not None:
                    beneficio = cuenta.beneficio()
                    if cuenta.bonificacion is not None:
                        beneficio += cuenta.bonificacion
                        print(f"El beneficio de de la cuenta {cuenta._id} es de {beneficio}$")
                    else:
                        print(f"El beneficio de de la cuenta {cuenta._id} es de {beneficio}$")                        
                else:
                    print("Error.Cuenta inexistente.")
                
            elif opcion == 7:
                
                opc = 2
                documento = dict()
                documento["_id"] = input("Introduzca el dni del cliente: ")
                cliente = obtener(documento["_id"],opc)
                if cliente is None :
                    documento["nombre"] = input("Introduzca el nombre: ")
                    documento["cuentas"] = []
                    cliente = Cliente(documento)
                    resultado = insertar(cliente,opc)
                    print(f" El numero de dni: {resultado} se ha registrado correctamente.")
                else:
                    print("Error.Cliente ya existente.")
                    
            elif opcion == 8:
                
                opc = 2
                documento = dict()
                dni = input("Introduzca el dni: ")
                cliente = obtener(dni,opc)
                if cliente is not None:
                    opc = 1
                    documento["_id"] = input("Introduzca el numero de cuenta: ")
                    cuenta = obtener(documento["_id"],opc)
                    if cuenta is None:
                        opc = 2
                        cliente.cuentas.append(documento["_id"])
                        actualizar(cliente,opc)
                        documento["saldo"] = float(input("Introduzca el saldo: "))
                        documento["interes"] = float(input("Introduzca el interes: "))
                        pregunta = input("Desea que sea bonificada?(si/no): ").lower()
                        opc = 1
                        if pregunta == "si":
                            documento["bonificacion"] = float(input("Introduzca la bonificacion: "))
                            documento["fecha"] = datetime.now()
                            cuenta = Cuenta(documento)
                            resultado = insertar(cuenta,opc)
                            print(f"El numero de cuenta {resultado} se ha registerado correctamente.")
                        else:
                            documento["bonificacion"] = None
                            documento["fecha"] = datetime.now()
                            cuenta = Cuenta(documento)
                            resultado = insertar(cuenta,opc)
                            print(f"El numero de cuenta {resultado} se ha registerado correctamente.")                             
                    else:
                        print("Error.Cuenta ya existente.")
                else:
                    print("Error.Cliente inexistente.")

            elif opcion == 9:
                
                opc = 2
                dni= input("Introduzca el dni: ")
                cliente = obtener(dni,opc)
                if cliente is not None:
                    print("NCUENTAS DEL CLIENTE:")
                    for cuenta in cliente.cuentas:
                        print(cuenta)
                    ncuenta = input("Elija el numero de cuenta a ELIMINAR: ")
                    opc = 1
                    cuenta = obtener(ncuenta,opc)                    
                    if cuenta is not None:
                        eliminar(cuenta)
                        for cuenta in cliente.cuentas:
                            if cuenta == ncuenta:
                                cliente.cuentas.remove(cuenta)
                        opc =  2
                        actualizar(cliente,opc)
                        print("CUENTA ELIMINADA CORRECTAMENTE")
                    else:
                        print("Error.Cuenta inexistente.")                        
                else:
                    print("Error.Cliente inexisttente.")
            else:
                print("Adios")
                
        except Exception as ex:
            print(ex)

main()
