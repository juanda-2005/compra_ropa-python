import json

# Clase base Producto
class Producto:
    def __init__(self, nombre, precio, stock):
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    def mostrar_info(self):
        return f"{self._nombre} - Precio: {self._precio} Gs, Stock: {self._stock}"

    def actualizar_stock(self, cantidad):
        if cantidad <= self._stock:
            self._stock -= cantidad
            return True
        else:
            print("No hay suficiente stock disponible.")
            return False

    def obtener_precio(self):
        return self._precio

    def obtener_nombre(self):
        return self._nombre

    def obtener_stock(self):
        return self._stock

# Clase Ropa que hereda de Producto
class Ropa(Producto):
    def __init__(self, nombre, precio, stock, talla):
        super().__init__(nombre, precio, stock)
        self._talla = talla

    def mostrar_info(self):
        return f"{self._nombre} - Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}"

# Clases específicas que heredan de Ropa
class Camisa(Ropa):
    def __init__(self, nombre, precio, stock, talla, tipo):
        super().__init__(nombre, precio, stock, talla)
        self._tipo = tipo

    def mostrar_info(self):
        return f"Camisa: {self._nombre}, Tipo: {self._tipo}, Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}"

class Pantalon(Ropa):
    def __init__(self, nombre, precio, stock, talla, corte):
        super().__init__(nombre, precio, stock, talla)
        self._corte = corte

    def mostrar_info(self):
        return f"Pantalon: {self._nombre}, Corte: {self._corte}, Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}"

class Zapato(Ropa):
    def __init__(self, nombre, precio, stock, talla, material):
        super().__init__(nombre, precio, stock, talla)
        self._material = material

    def mostrar_info(self):
        return f"Zapato: {self._nombre}, Material: {self._material}, Talla: {self._talla}, Precio: {self._precio} Gs, Stock: {self._stock}"

# Clase Tienda que maneja el inventario
class Tienda:
    def __init__(self):
        self.inventario = []
        self.cargar_inventario()

    def agregar_producto(self, producto):
        self.inventario.append(producto)

    def mostrar_productos(self):
        for producto in self.inventario:
            print(producto.mostrar_info())

    def buscar_producto(self, nombre):
        for producto in self.inventario:
            if producto.obtener_nombre() == nombre:
                return producto
        return None

    def cargar_inventario(self):
        try:
            with open("stock.txt", "r") as file:
                data = json.load(file)
                for item in data:
                    if item['tipo'] == "Camisa":
                        producto = Camisa(item['nombre'], item['precio'], item['stock'], item['talla'], item['tipo_especifico'])
                    elif item['tipo'] == "Pantalon":
                        producto = Pantalon(item['nombre'], item['precio'], item['stock'], item['talla'], item['tipo_especifico'])
                    elif item['tipo'] == "Zapato":
                        producto = Zapato(item['nombre'], item['precio'], item['stock'], item['talla'], item['tipo_especifico'])
                    self.inventario.append(producto)
            print("Inventario cargado exitosamente.")
        except FileNotFoundError:
            print("Archivo de stock no encontrado, iniciando con inventario vacío.")

    def guardar_inventario(self):
        data = []
        for producto in self.inventario:
            data.append({
                "tipo": producto.__class__.__name__,
                "nombre": producto.obtener_nombre(),
                "precio": producto.obtener_precio(),
                "stock": producto.obtener_stock(),
                "talla": producto._talla,
                "tipo_especifico": getattr(producto, "_tipo", getattr(producto, "_corte", getattr(producto, "_material", None)))
            })
        with open("stock.txt", "w") as file:
            json.dump(data, file)

# Clase Carrito que almacena los productos seleccionados
class Carrito:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto, cantidad):
        if producto.actualizar_stock(cantidad):
            self.productos.append((producto, cantidad))
            print(f"Producto '{producto.obtener_nombre()}' agregado al carrito.")

    def calcular_total(self):
        total = sum(producto.obtener_precio() * cantidad for producto, cantidad in self.productos)
        return total

    def mostrar_carrito(self):
        print("Resumen del carrito:")
        for producto, cantidad in self.productos:
            print(f"{producto.mostrar_info()} - Cantidad: {cantidad}")
        print(f"Total a pagar: {self.calcular_total()} Gs")

# Función principal del programa
def main():
    tienda = Tienda()
    carrito = Carrito()

    while True:
        print("\n--- Menú de la Tienda ---")
        print("1: Agregar producto")
        print("2: Ver productos")
        print("3: Comprar producto")
        print("4: Finalizar compra")
        print("5: Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            tipo = input("Introduce el tipo de producto (camisa, pantalon, zapato): ").strip().lower()
            nombre = input("Nombre del producto: ")
            precio = int(input("Precio del producto en guaraníes: "))
            stock = int(input("Cantidad en stock: "))
            talla = input("Talla del producto: ")

            if tipo == "camisa":
                tipo_especifico = input("Tipo de camisa (formal, casual, etc.): ")
                producto = Camisa(nombre, precio, stock, talla, tipo_especifico)
            elif tipo == "pantalon":
                tipo_especifico = input("Corte de pantalon (regular, slim, etc.): ")
                producto = Pantalon(nombre, precio, stock, talla, tipo_especifico)
            elif tipo == "zapato":
                tipo_especifico = input("Material del zapato (cuero, tela, etc.): ")
                producto = Zapato(nombre, precio, stock, talla, tipo_especifico)
            else:
                print("Tipo de producto no válido.")
                continue

            tienda.agregar_producto(producto)

        elif opcion == "2":
            tienda.mostrar_productos()

        elif opcion == "3":
            nombre = input("Introduce el nombre del producto a comprar: ")
            producto = tienda.buscar_producto(nombre)
            if producto:
                cantidad = int(input("Introduce la cantidad a comprar: "))
                carrito.agregar_producto(producto, cantidad)
            else:
                print("Producto no encontrado.")

        elif opcion == "4":
            carrito.mostrar_carrito()

        elif opcion == "5":
            tienda.guardar_inventario()
            print("Gracias por visitar la tienda. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()