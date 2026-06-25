import re
from datetime import datetime


class GestorVentas:
    def __init__(self, ventas_cargadas=None):
        self.ventas = ventas_cargadas if ventas_cargadas is not None else []

    def vender_producto(self, inventario):
        if not inventario.productos:
            print("\nNo hay productos registrados para vender.")
            return False

        print("\n--- REGISTRO DE VENTA ---")
        vendedor = self._pedir_nombre_vendedor()
        productos_vendidos = []
        total = 0
        utilidad = 0

        while True:
            codigo = input("Código del producto: ").strip().upper()
            producto = next((p for p in inventario.productos if p["codigo"] == codigo), None)

            if producto is None:
                print("Error: producto no encontrado.")
                continue

            if producto["stock"] <= 0:
                print("Error: producto sin stock.")
                continue

            cantidad = self._pedir_cantidad(producto)
            subtotal = cantidad * producto["precio"]
            subutilidad = cantidad * (producto["precio"] - producto.get("precio_compra", 0))

            producto["stock"] -= cantidad
            productos_vendidos.append({
                "codigo": producto["codigo"],
                "nombre": producto["nombre"],
                "cantidad": cantidad,
                "subtotal": subtotal,
                "subutilidad": subutilidad
            })

            total += subtotal
            utilidad += subutilidad
            print(f"Agregado: {producto['nombre']} x{cantidad} = S/. {subtotal:.2f}")

            if not self._desea_agregar_otro_producto():
                break

        metodo_pago, codigo_pago = self._pedir_metodo_pago()

        venta = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "vendedor": vendedor,
            "pago": metodo_pago,
            "codigo_pago": codigo_pago,
            "productos_detalles": productos_vendidos,
            "codigo": productos_vendidos[0]["codigo"],
            "nombre": productos_vendidos[0]["nombre"] if len(productos_vendidos) == 1 else f"{productos_vendidos[0]['nombre']} y otros",
            "cantidad": sum(item["cantidad"] for item in productos_vendidos),
            "total": total,
            "utilidad": utilidad
        }

        self.ventas.append(venta)
        print(f"Venta registrada correctamente. Total: S/. {total:.2f}")
        return True

    def reporte_ventas(self, inventario):
        if not self.ventas:
            print("\nNo hay ventas registradas.")
            return

        total_general = 0
        utilidad_general = 0
        unidades_por_producto = {}

        print("\n--- REPORTE DE VENTAS ---")
        print(f"{'N°':<4} {'FECHA':<20} {'VENDEDOR':<18} {'PRODUCTO':<28} {'CANT.':<7} {'PAGO':<12} {'TOTAL':<10} {'UTILIDAD'}")
        print("-" * 120)

        for numero, venta in enumerate(self.ventas, start=1):
            total_general += venta.get("total", 0)
            utilidad_general += venta.get("utilidad", 0)

            print(
                f"{numero:<4} "
                f"{venta.get('fecha', 'N/A'):<20} "
                f"{venta.get('vendedor', 'N/A'):<18} "
                f"{venta.get('nombre', 'N/A'):<28} "
                f"{venta.get('cantidad', 0):<7} "
                f"{venta.get('pago', 'N/A'):<12} "
                f"S/. {venta.get('total', 0):<6.2f} "
                f"S/. {venta.get('utilidad', 0):.2f}"
            )

            for item in venta.get("productos_detalles", []):
                nombre = item["nombre"]
                unidades_por_producto[nombre] = unidades_por_producto.get(nombre, 0) + item["cantidad"]

        print("-" * 120)
        print(f"Total vendido: S/. {total_general:.2f}")
        print(f"Utilidad total: S/. {utilidad_general:.2f}")

        if unidades_por_producto:
            mas_vendido = max(unidades_por_producto, key=unidades_por_producto.get)
            print(f"Producto más vendido: {mas_vendido} ({unidades_por_producto[mas_vendido]} unidades)")

    def _pedir_nombre_vendedor(self):
        while True:
            nombre = input("Nombre del vendedor: ").strip()
            patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$"

            if len(nombre) < 3 or len(nombre) > 50:
                print("Error: el nombre debe tener entre 3 y 50 caracteres.")
            elif not re.fullmatch(patron, nombre):
                print("Error: el nombre solo puede contener letras y espacios.")
            else:
                return nombre

    def _pedir_cantidad(self, producto):
        while True:
            try:
                cantidad = int(input(f"Cantidad a vender de '{producto['nombre']}' (stock: {producto['stock']}): "))
                if 1 <= cantidad <= producto["stock"]:
                    return cantidad
                print("Error: cantidad inválida o mayor al stock disponible.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

    def _desea_agregar_otro_producto(self):
        while True:
            respuesta = input("¿Agregar otro producto a la venta? (s/n): ").strip().lower()
            if respuesta == "s":
                return True
            if respuesta == "n":
                return False
            print("Error: responda solo con 's' o 'n'.")

    def _pedir_metodo_pago(self):
        while True:
            print("\nMétodo de pago")
            print("1. Efectivo")
            print("2. Yape")
            print("3. Tarjeta")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                return "Efectivo", ""
            if opcion == "2":
                codigo = self._pedir_codigo_yape()
                return "Yape", codigo
            if opcion == "3":
                return "Tarjeta", ""

            print("Error: opción de pago inválida.")

    def _pedir_codigo_yape(self):
        while True:
            codigo = input("Código de seguridad Yape (3 números): ").strip()
            if codigo.isdigit() and len(codigo) == 3:
                return codigo
            print("Error: el código de Yape debe tener exactamente 3 números.")
