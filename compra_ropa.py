from abc import ABC, abstractmethod
import os

class Producto(ABC):
    def __init__(self, nombre, precio, stock, talla):
        self._nombre = nombre
        self._precio = precio
        self._stock = stock
        self._talla = talla

    @abstractmethod
    def mostrar_detalle(self):
        pass

    def comprar(self, cantidad):
        if cantidad <= self._stock:
            self._stock -= cantidad
            return self._precio * cantidad
        else:
            print("No hay suficiente stock.")
            return 0

    def get_nombre(self):
        return self._nombre

    def get_stock(self):
        return self._stock

    def set_stock(self, stock):
        self._stock = stock

class Camisa(Producto):
    def mostrar_detalle(self):
        print(f"Camisa: {self._nombre}, Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}")

class Pantalon(Producto):
    def mostrar_detalle(self):
        print(f"Pantalón: {self._nombre}, Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}")

class Zapato(Producto):
    def mostrar_detalle(self):
        print(f"Zapato: {self._nombre}, Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}")

class Tienda:
    def __init__(self, nombre):
        self.nombre = nombre
        self.productos = []
        self.cargar_productos() 

    def agregar_producto(self, producto):
        self.productos.append(producto)
        print(f"Producto '{producto.get_nombre()}' agregado a la tienda.")
        self.guardar_productos() 

    def mostrar_productos(self):
        if self.productos:
            print("\nProductos disponibles:")
            for producto in self.productos:
                producto.mostrar_detalle()
        else:
            print("\nNo hay productos disponibles en la tienda.")

    def procesar_compra(self, nombre_producto, cantidad):
        for producto in self.productos:
            if producto.get_nombre().lower() == nombre_producto.lower():
                total = producto.comprar(cantidad)
                if total > 0:
                    print(f"Compra realizada. Total a pagar: {total:,} Gs")
                    self.guardar_productos() 
                return
        print("Producto no encontrado.")

    def guardar_productos(self):
        with open("stock.txt", "w") as file:
            for producto in self.productos:
                file.write(f"{type(producto).__name__},{producto.get_nombre()},{producto._precio},{producto.get_stock()},{producto._talla}\n")

    def cargar_productos(self):
        if os.path.exists("stock.txt"):
            with open("stock.txt", "r") as file:
                for line in file:
                    if line.strip(): 
                        try:
                            tipo, nombre, precio, stock, talla = line.strip().split(",")
                            precio = int(precio)
                            stock = int(stock)

                            if tipo == "Camisa":
                                producto = Camisa(nombre, precio, stock, talla)
                            elif tipo == "Pantalon":
                                producto = Pantalon(nombre, precio, stock, talla)
                            elif tipo == "Zapato":
                                producto = Zapato(nombre, precio, stock, talla)
                            else:
                                continue
                            
                            self.productos.append(producto)
                        except ValueError as e:
                            print(f"Error al cargar un producto: {e}")
            print("Inventario cargado exitosamente.")
        else:
            print("Archivo de stock no encontrado, iniciando con inventario vacío.")

def menu():
    tienda = Tienda("Ropa Moderna")
    
    while True:
        print("\n--- Menú de la Tienda ---")
        print("1: Agregar producto")
        print("2: Ver productos")
        print("3: Comprar producto")
        print("4: Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            tipo = input("Introduce el tipo de producto (camisa, pantalon, zapato): ").strip().lower()
            nombre = input("Nombre del producto: ")
            precio = int(input("Precio del producto en guaraníes: "))
            stock = int(input("Cantidad en stock: "))
            talla = input("Talla del producto: ")

            if tipo == "camisa":
                tienda.agregar_producto(Camisa(nombre, precio, stock, talla))
            elif tipo == "pantalon":
                tienda.agregar_producto(Pantalon(nombre, precio, stock, talla))
            elif tipo == "zapato":
                tienda.agregar_producto(Zapato(nombre, precio, stock, talla))
            else:
                print("Tipo de producto no válido.")
        
        elif opcion == '2':
            tienda.mostrar_productos()

        elif opcion == '3':
            nombre_producto = input("Introduce el nombre del producto a comprar: ")
            cantidad = int(input("Introduce la cantidad a comprar: "))
            tienda.procesar_compra(nombre_producto, cantidad)
        
        elif opcion == '4':
            print("Gracias por visitar la tienda. ¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")
menu()
