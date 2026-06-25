
import re


class GestorInventario:
    CATEGORIAS = {
        "C": "Cuadernos",
        "P": "Papelería",
        "A": "Arte y Manualidades",
        "H": "Herramientas de Oficina",
        "E": "Escritura",
        "Ñ": "Varios"
    }

    VALORES_INVALIDOS = {"", "nan", "inf", "-inf", "infinity", "null", "undefined", "none"}

    def _init_(self, productos_cargados=None):
        self.productos = productos_cargados if productos_cargados is not None else []

    def registrar_producto(self):
        print("\n--- REGISTRO DE PRODUCTO ---")

        nombre = self._pedir_nombre_producto()
        codigo, categoria = self._pedir_codigo_producto()
        precio = self._pedir_precio("Precio de venta (S/.): ")
        precio_compra = self._pedir_precio_compra(precio)
        stock = self._pedir_entero("Stock inicial: ", minimo=0)
        stock_minimo = self._pedir_entero("Stock mínimo de alerta: ", minimo=1)

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria": categoria,
            "precio": precio,
            "precio_compra": precio_compra,
            "stock": stock,
            "stock_minimo": stock_minimo
        }

        self.productos.append(producto)
        print(f"Producto registrado correctamente: {nombre} ({codigo}).")

    def mostrar_productos(self):
        if not self.productos:
            print("\nEl inventario está vacío.")
            return

        print("\n--- INVENTARIO DE PRODUCTOS ---")
        print(f"{'CÓDIGO':<8} {'NOMBRE':<30} {'CATEGORÍA':<24} {'PRECIO':<10} {'STOCK':<8} {'ESTADO'}")
        print("-" * 95)

        for producto in sorted(self.productos, key=lambda p: p["codigo"]):
            stock = producto["stock"]
            stock_minimo = producto.get("stock_minimo", 1)

            if stock == 0:
                estado = "SIN STOCK"
            elif stock <= stock_minimo:
                estado = "BAJO STOCK"
            else:
                estado = "OK"

            print(
                f"{producto['codigo']:<8} "
                f"{producto['nombre']:<30} "
                f"{producto.get('categoria', 'Sin categoría'):<24} "
                f"S/. {producto['precio']:<6.2f} "
                f"{stock:<8} "
                f"{estado}"
            )

    def buscar_producto(self):
        if not self.productos:
            print("\nNo hay productos registrados.")
            return

        texto = input("\nIngrese el nombre del producto a buscar: ").strip().lower()
        if texto in self.VALORES_INVALIDOS:
            print("Error: búsqueda inválida.")
            return

        encontrados = [p for p in self.productos if texto in p["nombre"].lower()]

        if not encontrados:
            print("No se encontraron productos.")
            return

        print("\n--- RESULTADOS DE BÚSQUEDA ---")
        for producto in encontrados:
            print(f"Código: {producto['codigo']}")
            print(f"Nombre: {producto['nombre']}")
            print(f"Categoría: {producto.get('categoria', 'Sin categoría')}")
            print(f"Precio: S/. {producto['precio']:.2f}")
            print(f"Stock: {producto['stock']}")
            print("-" * 35)
            def _pedir_nombre_producto(self):
        while True:
            nombre = input("Nombre del producto: ").strip()
            nombre_minuscula = nombre.lower()

            if nombre_minuscula in self.VALORES_INVALIDOS:
                print("Error: el nombre no puede estar vacío.")
            elif len(nombre) < 3 or len(nombre) > 60:
                print("Error: el nombre debe tener entre 3 y 60 caracteres.")
            elif nombre.isdigit():
                print("Error: el nombre no puede ser solo números.")
            elif all(not caracter.isalnum() and not caracter.isspace() for caracter in nombre):
                print("Error: el nombre no puede contener solo símbolos.")
            elif any(p["nombre"].lower() == nombre_minuscula for p in self.productos):
                print("Error: ya existe un producto con ese nombre.")
            else:
                return nombre

    def _pedir_codigo_producto(self):
        while True:
            print("\nPrefijos permitidos:")
            for letra, categoria in self.CATEGORIAS.items():
                print(f"{letra} -> {categoria}")

            codigo = input("Código del producto (Ejemplo: C001): ").strip().upper()

            if codigo.lower() in self.VALORES_INVALIDOS:
                print("Error: el código no puede estar vacío.")
            elif len(codigo) != 4:
                print("Error: el código debe tener 4 caracteres.")
            elif codigo[0] not in self.CATEGORIAS:
                print("Error: prefijo de categoría inválido.")
            elif not codigo[1:].isdigit():
                print("Error: después del prefijo deben ir 3 números.")
            elif any(p["codigo"] == codigo for p in self.productos):
                print("Error: ya existe un producto con ese código.")
            else:
                return codigo, self.CATEGORIAS[codigo[0]]

    def _pedir_precio(self, mensaje):
        while True:
            entrada = input(mensaje).strip()

            if entrada.lower() in self.VALORES_INVALIDOS:
                print("Error: entrada inválida.")
            elif not re.fullmatch(r"\d+(\.\d{1,2})?", entrada):
                print("Error: ingrese un número positivo con máximo 2 decimales.")
            else:
                precio = float(entrada)
                if precio > 0:
                    return precio
                print("Error: el precio debe ser mayor a 0.")

    def _pedir_precio_compra(self, precio_venta):
        while True:
            precio_compra = self._pedir_precio("Precio de compra (S/.): ")
            if precio_compra < precio_venta:
                return precio_compra
            print("Error: el precio de compra debe ser menor al precio de venta.")

    def _pedir_entero(self, mensaje, minimo):
        while True:
            entrada = input(mensaje).strip()

            try:
                numero = int(entrada)
                if numero >= minimo:
                    return numero
                print(f"Error: el valor mínimo permitido es {minimo}.")
            except ValueError:
                print("Error: ingrese un número entero válido.")
