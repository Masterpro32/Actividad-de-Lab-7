# Importa json para leer y escribir datos en formato JSON.
import json
# Importa os para trabajar con rutas de archivos y carpetas del sistema.
import os
# Importa re para validar textos mediante expresiones regulares.
import re
# Importa datetime para registrar la fecha y hora exacta de cada venta.
from datetime import datetime

# Define la clase encargada de gestionar ventas, pagos y reportes.
class GestorVentas:
    # Constructor que recibe el historial de ventas cargado, si existe.
    def __init__(self, ventas_cargadas=None):
        # Inicializa la lista de ventas con datos cargados o con una lista vacía.
        self.ventas = ventas_cargadas if ventas_cargadas is not None else []

    # Define un método reutilizable para validar el nombre del vendedor.
    def validar_nombre_vendedor(self, mensaje):
        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Solicita el nombre del vendedor y elimina espacios al inicio y al final.
            nombre = input(mensaje).strip()
            # Valida que el nombre del vendedor no esté vacío ni sea una palabra inválida.
            if nombre == "" or nombre.lower() in ['nan', 'inf', '-inf', 'infinity', 'null', 'undefined']:
                # Muestra un error cuando el nombre del vendedor no es aceptado.
                print("Error: Nombre de vendedor no válido.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Verifica que el nombre del vendedor tenga entre 3 y 50 caracteres.
            if len(nombre) < 3 or len(nombre) > 50:
                # Informa el rango permitido para el nombre del vendedor.
                print("Error: El nombre del vendedor debe tener entre 3 y 50 caracteres.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Define una expresión regular que permite solo letras, tildes, ñ, ü y espacios.
            patron_nombre = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$"
            # Comprueba si el nombre completo cumple con el patrón permitido.
            if not re.fullmatch(patron_nombre, nombre):
                # Informa que el nombre no puede tener números ni símbolos.
                print("Error : El nombre del vendedor solo puede contener letras y espacios. No se permiten números ni símbolos.")
                # Regresa al inicio del bucle para volver a pedir una entrada válida.
                continue
            # Devuelve el nombre del vendedor ya validado.
            return nombre

    # Define el método principal para registrar una venta con uno o varios productos.
    def vender_producto(self, inventario):
        # Inicia un bloque para intentar ejecutar código que podría generar errores.
        try:
            # Muestra el encabezado del proceso de venta multiproducto.
            print("\n--- REGISTRAR VENTA MULTIPRODUCTO ---")
            # Verifica si existen productos disponibles en el inventario.
            if not inventario.productos:
                # Informa que no se puede vender porque no hay productos registrados.
                print("No hay productos registrados.")
                # Sale del método actual sin continuar ejecutando más instrucciones.
                return

            # Solicita y valida el nombre del vendedor antes de registrar la venta.
            vendedor = self.validar_nombre_vendedor("Nombre del vendedor: ")
            # Crea una lista para guardar los productos agregados a la boleta actual.
            items_venta = []
            # Inicializa el total que pagará el cliente en esta venta.
            total_boleta = 0
            # Inicializa la utilidad o ganancia total de esta venta.
            utilidad_boleta = 0

            # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
            while True:
                # Solicita el código del producto, elimina espacios y lo convierte a mayúsculas.
                codigo = input("\nIngrese el código del producto: ").strip().upper()
                # Valida que el código ingresado no sea vacío ni un valor inválido.
                if codigo in ['NAN', 'INF', '-INF', 'INFINITY', '']:
                    # Informa que el código ingresado no es aceptado.
                    print("Error: Código no válido.")
                    # Regresa al inicio del bucle para volver a pedir una entrada válida.
                    continue

                # Busca en el inventario el primer producto que coincida con el código ingresado.
                producto = next((p for p in inventario.productos if p['codigo'] == codigo), None)
                # Verifica si no se encontró ningún producto con ese código.
                if not producto:
                    # Informa que el código no corresponde a ningún producto registrado.
                    print("Error: Producto no encontrado.")
                # Evalúa una condición alternativa si las condiciones anteriores no se cumplieron.
                elif producto['stock'] <= 0:
                    # Informa que el producto existe, pero no puede venderse por falta de stock.
                    print(f"Error: El producto {producto['nombre']} no tiene stock disponible.")
                # Maneja cualquier opción que no coincida con las opciones permitidas.
                else:
                    # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
                    while True:
                        # Solicita la cantidad a vender mostrando el stock disponible.
                        entrada_cant = input(f"Cantidad a vender de '{producto['nombre']}' (Stock: {producto['stock']}): ").strip()
                        # Valida que la cantidad ingresada no esté vacía ni sea un valor inválido.
                        if entrada_cant.lower() in ['inf', '-inf', 'nan', 'infinity', '']:
                            # Muestra información en pantalla para guiar al usuario durante el proceso.
                            print("Error: Entrada no válida.")
                            # Regresa al inicio del bucle para volver a pedir una entrada válida.
                            continue
                        # Inicia un bloque para intentar ejecutar código que podría generar errores.
                        try:
                            # Convierte la cantidad ingresada a número entero.
                            cantidad = int(entrada_cant)
                            # Valida que la cantidad sea mayor que cero y no supere el stock disponible.
                            if 0 < cantidad <= producto['stock']:
                                # Rompe el bucle principal y finaliza la ejecución de la función actual.
                                break
                            # Informa que la cantidad no es válida para la venta.
                            print("Error: Cantidad inválida o supera el stock.")
                        # Captura el error cuando la entrada numérica no tiene el formato esperado.
                        except ValueError:
                            # Solicita que la cantidad sea un número entero válido.
                            print("Error: Ingrese un número entero válido.")

                    # Obtiene el precio de venta del producto seleccionado.
                    precio_v = producto['precio']
                    # Obtiene el precio de compra; si no existe, usa 0 como valor predeterminado.
                    precio_c = producto.get('precio_compra', 0)
                    # Calcula el subtotal multiplicando cantidad por precio de venta.
                    subtotal = quantity = cantidad * precio_v
                    # Calcula la ganancia del producto vendido.
                    subutilidad = (precio_v - precio_c) * cantidad

                    # Descuenta del inventario la cantidad vendida.
                    producto['stock'] -= cantidad

                    # Agrega el producto vendido a la lista de detalles de la boleta.
                    items_venta.append({
                        # Línea necesaria para completar el funcionamiento del sistema.
                        "codigo": producto['codigo'],
                        # Línea necesaria para completar el funcionamiento del sistema.
                        "nombre": producto['nombre'],
                        # Guarda la cantidad vendida del producto.
                        "cantidad": cantidad,
                        # Guarda el subtotal correspondiente a este producto.
                        "subtotal": subtotal,
                        # Guarda la utilidad generada por este producto.
                        "subutilidad": subutilidad
                    # Línea necesaria para completar el funcionamiento del sistema.
                    })

                    # Suma el subtotal del producto al total general de la boleta.
                    total_boleta += subtotal
                    # Suma la utilidad del producto a la utilidad total de la venta.
                    utilidad_boleta += subutilidad
                    # Confirma que el producto fue agregado a la venta actual.
                    print(f"-> Agregado: {producto['nombre']} x{cantidad} (S/. {subtotal:.2f})")

                # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
                while True:
                    # Pregunta si se agregará otro producto a la misma boleta.
                    continuar = input("\n¿Deseas agregar otro producto a esta misma venta? (s/n): ").strip().lower()
                    # Valida que la respuesta sea solamente sí o no.
                    if continuar in ['s', 'n']:
                        # Rompe el bucle principal y finaliza la ejecución de la función actual.
                        break
                    # Informa que solo se aceptan las opciones s o n.
                    print("Error: Opción inválida. Ingrese únicamente 's' para Sí o 'n' para No.")
                # Evalúa una condición para decidir si se ejecuta este bloque de código.
                if continuar == 'n':
                    # Rompe el bucle principal y finaliza la ejecución de la función actual.
                    break

            # Verifica que la venta tenga al menos un producto agregado.
            if items_venta:
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print(f"\n=========================================")
                # Muestra el total final que debe pagar el cliente.
                print(f" TOTAL A PAGAR POR EL CLIENTE: S/. {total_boleta:.2f}")
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print(f"=========================================")
                
                # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
                while True:
                    # Muestra las opciones disponibles de método de pago.
                    print("\nMétodo de pago: 1. Efectivo | 2. Yape | 3. Tarjeta")
                    # Solicita al usuario seleccionar un método de pago.
                    op_pago = input("Seleccione una opción (1-3): ").strip()
                    # Valida que la opción de pago sea una de las permitidas.
                    if op_pago in ['1', '2', '3']:
                        # Rompe el bucle principal y finaliza la ejecución de la función actual.
                        break
                    # Informa que el método de pago ingresado no es válido.
                    print("Error: Opción inválida. Debe seleccionar 1, 2 o 3.")

                # Establece efectivo como método de pago predeterminado.
                metodo_pago = "Efectivo"
                # Inicializa el código de pago vacío porque solo aplica para algunos métodos.
                cod_pago = ""
                
                # Comprueba si el pago será por Yape.
                if op_pago == "2":
                    # Asigna Yape como método de pago.
                    metodo_pago = "Yape"
                    # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
                    while True:
                        # Solicita el código de seguridad de Yape.
                        cod_pago = input("Ingrese código de seguridad Yape (Exactamente 3 números): ").strip()
                        # Valida que el código de Yape tenga exactamente tres dígitos.
                        if cod_pago.isdigit() and len(cod_pago) == 3:
                            # Rompe el bucle principal y finaliza la ejecución de la función actual.
                            break
                        # Indica el formato correcto para el código de Yape.
                        print("Error: El código de Yape debe tener exactamente 3 dígitos numéricos (Ejemplo: 457).")
                # Comprueba si el pago será con tarjeta.
                elif op_pago == "3":
                    # Asigna tarjeta como método de pago.
                    metodo_pago = "Tarjeta"
                    # Inicializa el código de pago vacío porque solo aplica para algunos métodos.
                    cod_pago = ""

                # Crea un diccionario con toda la información de la venta realizada.
                nueva_venta = {
                    # Guarda la fecha y hora actual con formato día/mes/año hora:minuto:segundo.
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    # Guarda el nombre del vendedor que atendió la venta.
                    "vendedor": vendedor,
                    # Guarda el método de pago usado por el cliente.
                    "pago": metodo_pago,
                    # Guarda el código de pago si corresponde.
                    "codigo_pago": cod_pago,
                    # Guarda la lista detallada de productos vendidos en la boleta.
                    "productos_detalles": items_venta, 
                    # Guarda el total final de la boleta.
                    "total": total_boleta,
                    # Guarda la utilidad total obtenida en la venta.
                    "utilidad": utilidad_boleta
                # Línea necesaria para completar el funcionamiento del sistema.
                }
                
                # Guarda el código del primer producto para mantener compatibilidad con reportes antiguos.
                nueva_venta["codigo"] = items_venta[0]["codigo"]
                # Guarda el nombre del producto o un resumen cuando hay varios productos.
                nueva_venta["nombre"] = items_venta[0]["nombre"] if len(items_venta) == 1 else f"{items_venta[0]['nombre']} y otros..."
                # Calcula el total de unidades vendidas en la boleta.
                nueva_venta["cantidad"] = sum(item["cantidad"] for item in items_venta)

                # Agrega la venta completa al historial de ventas.
                self.ventas.append(nueva_venta)
                
                # Inicia un bloque para intentar ejecutar código que podría generar errores.
                try:
                    # Obtiene la carpeta donde está ubicado el archivo de clases.
                    ruta_clases = os.path.dirname(os.path.abspath(__file__))
                    # Obtiene la carpeta principal del proyecto, ubicada encima de la carpeta de clases.
                    ruta_libreria = os.path.dirname(ruta_clases)
                    # Construye la ruta completa donde se guardará el archivo JSON.
                    ruta_json = os.path.join(ruta_libreria, "libreria_datos.json")

                    # Abre el archivo JSON en modo escritura para guardar automáticamente la venta.
                    with open(ruta_json, "w", encoding="utf-8") as f:
                        # Prepara el diccionario que se guardará en el JSON.
                        datos_a_guardar = {
                            # Incluye el inventario actualizado con el stock descontado.
                            "productos": inventario.productos,
                            # Incluye el historial de ventas actualizado.
                            "ventas": self.ventas
                        # Línea necesaria para completar el funcionamiento del sistema.
                        }
                        # Escribe los datos actualizados en formato JSON legible.
                        json.dump(datos_a_guardar, f, ensure_ascii=False, indent=4)
                # Captura cualquier error que ocurra durante el autoguardado.
                except Exception as e:
                    # Muestra el detalle del error si el autoguardado falla.
                    print(f"\nError crítico al auto-guardar el archivo: {e}")

                # Confirma que la venta se registró y muestra el total.
                print(f"¡Venta registrada con éxito! Total Boleta: S/. {total_boleta:.2f}")
            # Maneja cualquier opción que no coincida con las opciones permitidas.
            else:
                # Informa que no se registró venta porque no se añadió ningún producto.
                print("\nVenta cancelada (No se agregaron productos).")

        # Captura la interrupción manual del usuario con Ctrl + C.
        except KeyboardInterrupt:
            # Informa que la venta fue cancelada por interrupción.
            print("\n\n[PROCESO INTERRUMPIDO] Se presionó Ctrl + C. La venta actual fue cancelada y el stock no se afectará.")
            # Verifica si ya se habían agregado productos antes de la interrupción.
            if 'items_venta' in locals() and items_venta:
                # Recorre los productos agregados para revertir el descuento de stock.
                for item in items_venta:
                    # Busca el producto afectado dentro del inventario.
                    prod = next((p for p in inventario.productos if p['codigo'] == item['codigo']), None)
                    # Comprueba que el producto exista antes de restaurar stock.
                    if prod:
                        # Devuelve al inventario la cantidad que se había descontado.
                        prod['stock'] += item['cantidad']
                # Confirma que el stock fue restaurado correctamente.
                print("-> El stock retenido ha sido devuelto al inventario con éxito.")

    # Define el método que muestra diferentes reportes de ventas.
    def reporte_ventas(self, inventario):
        # Verifica si todavía no existen ventas registradas.
        if not self.ventas:
            # Informa que no hay información suficiente para reportar ventas.
            print("\nNo hay ventas registradas.")
            # Sale del método actual sin continuar ejecutando más instrucciones.
            return

        # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
        while True:
            # Muestra el encabezado del menú de reportes.
            print("\n--- REPORTES DE VENTAS ---")
            # Muestra la opción para listar todas las ventas.
            print("1. Ver todas las ventas")
            # Muestra la opción para filtrar ventas por categoría.
            print("2. Filtrar por categoría")
            # Muestra la opción para calcular el producto con más unidades vendidas.
            print("3. Ver producto más vendido")
            # Muestra la opción para revisar una venta puntual con detalle.
            print("4. Ver detalle de una venta específica")
            # Solicita al usuario elegir el tipo de reporte.
            op = input("Seleccione una opción (1-4): ").strip()
            # Valida que la opción del reporte esté dentro del rango permitido.
            if op in ['1', '2', '3', '4']:
                # Rompe el bucle principal y finaliza la ejecución de la función actual.
                break
            # Informa que debe elegirse un número entre 1 y 4.
            print("Error: Opción inválida. Seleccione un número entre 1 y 4.")

        # Inicialmente usa todas las ventas para el reporte.
        lista = self.ventas
        
        # Comprueba si el usuario desea filtrar por categoría.
        if op == "2":
            # Define la lista de categorías disponibles para filtrar ventas.
            cats = ["Cuadernos", "Papelería", "Arte y Manualidades", "Herramientas de Oficina", "Escritura", "Varios"]
            # Muestra el encabezado de categorías disponibles.
            print("\nCategorías disponibles:")
            # Recorre las categorías asignándoles un número desde 1.
            for i, cat in enumerate(cats, 1):
                # Muestra cada categoría junto con su número de selección.
                print(f"{i}. {cat}")
            
            # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
            while True:
                # Solicita el número de la categoría que se desea filtrar.
                sel = input("\nIngrese el número de la categoría: ").strip()
                # Valida que la selección no esté vacía ni sea un valor inválido.
                if sel.lower() in ['inf', '-inf', 'nan', 'infinity', '']:
                    # Muestra información en pantalla para guiar al usuario durante el proceso.
                    print("Error: Entrada inválida.")
                    # Regresa al inicio del bucle para volver a pedir una entrada válida.
                    continue
                # Verifica que la selección sea un número dentro del rango de categorías.
                if sel.isdigit() and 0 < int(sel) <= len(cats):
                    # Rompe el bucle principal y finaliza la ejecución de la función actual.
                    break
                # Informa el rango correcto para seleccionar una categoría.
                print(f"Error: Debe ingresar un número entre 1 y {len(cats)}.")

            # Convierte la categoría elegida a minúsculas para comparar fácilmente.
            cat_elegida = cats[int(sel)-1].lower()
            # Obtiene los códigos de productos que pertenecen a la categoría elegida.
            cods = [p['codigo'] for p in inventario.productos if p.get('categoria', '').lower() == cat_elegida]
            
            # Reinicia la lista para guardar solo las ventas que coincidan con el filtro.
            lista = []
            # Recorre cada venta registrada en el historial.
            for v in self.ventas:
                # Inicializa una bandera para saber si la venta contiene productos de la categoría.
                incluye_producto = False
                # Comprueba si la venta tiene formato multiproducto con detalle.
                if "productos_detalles" in v:
                    # Recorre los productos de una venta con varios productos.
                    for item in v["productos_detalles"]:
                        # Evalúa una condición para decidir si se ejecuta este bloque de código.
                        if item.get('codigo') in cods:
                            # Marca que la venta sí incluye al menos un producto de la categoría elegida.
                            incluye_producto = True
                            # Rompe el bucle principal y finaliza la ejecución de la función actual.
                            break
                # Maneja cualquier opción que no coincida con las opciones permitidas.
                else:
                    # Evalúa una condición para decidir si se ejecuta este bloque de código.
                    if v.get('codigo') in cods:
                        # Marca que la venta sí incluye al menos un producto de la categoría elegida.
                        incluye_producto = True
                # Comprueba si la venta debe agregarse al resultado filtrado.
                if incluye_producto:
                    # Agrega la venta al listado filtrado por categoría.
                    lista.append(v)
            
        # Comprueba si el usuario desea ver el producto más vendido.
        elif op == "3":
            # Crea un diccionario para acumular unidades vendidas por producto.
            conteo_unidades = {}
            # Recorre cada venta registrada en el historial.
            for v in self.ventas:
                # Comprueba si la venta tiene formato multiproducto con detalle.
                if "productos_detalles" in v:
                    # Recorre los productos de una venta con varios productos.
                    for item in v["productos_detalles"]:
                        # Obtiene el nombre del producto o usa Desconocido si falta el dato.
                        n = item.get('nombre', 'Desconocido')
                        # Suma la cantidad vendida al conteo total de ese producto.
                        conteo_unidades[n] = conteo_unidades.get(n, 0) + item.get('cantidad', 0)
                # Maneja cualquier opción que no coincida con las opciones permitidas.
                else:
                    # Obtiene el nombre del producto en ventas simples o antiguas.
                    nombre = v.get('nombre', 'Desconocido')
                    # Obtiene la cantidad vendida en una venta simple o antigua.
                    cant = v.get('cantidad', 0)
                    # Acumula las unidades vendidas para productos de ventas antiguas.
                    conteo_unidades[nombre] = conteo_unidades.get(nombre, 0) + cant
            
            # Verifica que existan datos suficientes para calcular el producto más vendido.
            if conteo_unidades:
                # Encuentra el producto con la mayor cantidad de unidades vendidas.
                producto_estrella = max(conteo_unidades, key=conteo_unidades.get)
                # Obtiene el total de unidades vendidas del producto más vendido.
                unidades_totales = conteo_unidades[producto_estrella]
                
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("\n==================================================")
                # Muestra el título del reporte de producto más vendido.
                print(f"PRODUCTO MÁS VENDIDO")
                # Muestra el nombre del producto más vendido.
                print(f"Producto: {producto_estrella}")
                # Muestra cuántas unidades se vendieron de ese producto.
                print(f"Total de unidades despachadas: {unidades_totales} uds.")
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print("==================================================")
            # Maneja cualquier opción que no coincida con las opciones permitidas.
            else:
                # Informa que no se puede calcular el producto más vendido.
                print("\nNo hay registros suficientes para calcular el más vendido.")
            # Sale del método actual sin continuar ejecutando más instrucciones.
            return

        # Comprueba si el usuario desea ver el detalle de una venta específica.
        elif op == "4":
            # Inicia un bucle para mantener el programa activo hasta que el usuario decida salir.
            while True:
                # Solicita el número de venta que se desea revisar en detalle.
                num_ingresado = input(f"\nIngrese el número de la venta que desea detallar (1-{len(self.ventas)}): ").strip()
                # Valida que el número ingresado esté dentro del rango de ventas existentes.
                if num_ingresado.isdigit() and 0 < int(num_ingresado) <= len(self.ventas):
                    # Rompe el bucle principal y finaliza la ejecución de la función actual.
                    break
                # Informa el rango válido de ventas que se pueden consultar.
                print(f"Error: Ingrese un número válido en el rango de 1 a {len(self.ventas)}.")
            
            # Obtiene la venta seleccionada restando 1 porque las listas empiezan desde cero.
            venta_sel = self.ventas[int(num_ingresado) - 1]
            
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("\n=======================================================================")
            # Muestra el título del detalle de la venta elegida.
            print(f"DETALLE DE LA VENTA N° {num_ingresado}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("=======================================================================")
            # Muestra la fecha y hora de la venta seleccionada.
            print(f"Fecha/Hora:  {venta_sel.get('fecha', 'N/A')}")
            # Muestra el vendedor de la venta seleccionada.
            print(f"Vendedor:    {venta_sel.get('vendedor', 'N/A')}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print(f"Método Pago: {venta_sel.get('pago', 'Efectivo')} {f'({venta_sel.get('codigo_pago')})' if venta_sel.get('codigo_pago') else ''}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("------------------------------------------------------------------------")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print(f"{'COD.':<6} | {'PRODUCTO':<30} | {'STOCK':<10} | {'CANT.':<5} | {'SUBTOTAL':<9}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("------------------------------------------------------------------------")
            # Obtiene los productos detallados o adapta ventas antiguas a una lista.
            lista_items = venta_sel.get("productos_detalles", [venta_sel])
            
            # Recorre una colección de datos elemento por elemento.
            for item in lista_items:
                # Obtiene el código del producto vendido en el detalle.
                cod = item.get('codigo')
                # Obtiene la cantidad vendida del producto en el detalle.
                cant = item.get('cantidad', 0)
            
                # Asigna o actualiza un valor que será usado más adelante en el programa.
                prod = next((p for p in inventario.productos if p['codigo'] == cod), None)
                # Obtiene el stock actual del producto; si no existe, usa cero.
                stock_actual = prod.get('stock', 0) if prod else 0
                # Reconstruye el stock antes de la venta sumando lo vendido al stock actual.
                stock_inicial = stock_actual + cant
                # Forma un texto que muestra el cambio de stock antes y después de la venta.
                str_stock = f"{stock_inicial}->{stock_actual}"
                
                # Muestra información en pantalla para guiar al usuario durante el proceso.
                print(f"{cod:<6} | {item.get('nombre', 'Desconocido'):<30} | {str_stock:<10} | {cant:<5} | S/. {item.get('subtotal', 0):<5.2f}")
                
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("-------------------------------------------------------------------------")
            # Muestra el total pagado en la venta detallada.
            print(f"TOTAL COMPRA:                                                  S/. {venta_sel.get('total', 0):.2f}")
            # Muestra la ganancia generada por la venta detallada.
            print(f"UTILIDAD:                                                      S/. {venta_sel.get('utilidad', 0):.2f}")
            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print("========================================================================")
            # Sale del método actual sin continuar ejecutando más instrucciones.
            return

        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print(f"\n{'N° VENTA':<9} | {'FECHA':<20} | {'COD.':<6} | {'PRODUCTO':<25} | {'CATEGORÍA':<18} | {'STOCK':<11} | {'CANT.':<5} | {'PAGO':<15} | {'TOTAL':<9} | {'UTILIDAD':<9}")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("-" * 163)
        
        # Inicializa el acumulador de utilidad total del reporte.
        ut_total = 0
        # Inicializa el acumulador de unidades vendidas del reporte.
        un_total = 0
        
        # Recorre las ventas del reporte asignándoles un número visible desde 1.
        for num_v, v in enumerate(lista, 1):
            # Obtiene la cantidad vendida en una venta simple o antigua.
            cant = v.get('cantidad', 0)
            # Suma las unidades de la venta al total general.
            un_total += cant
            
            # Obtiene la utilidad guardada en la venta; si no existe, usa cero.
            ut = v.get('utilidad', 0)
            # Busca el producto relacionado con la venta para completar datos del reporte.
            prod = next((p for p in inventario.productos if p['codigo'] == v['codigo']), None)
            # Si no hay utilidad guardada, intenta calcularla usando los datos del producto.
            if ut == 0 and prod:
                # Obtiene el precio de compra para calcular utilidad.
                precio_c = prod.get('precio_compra', 0)
                # Obtiene el precio de venta para calcular utilidad.
                precio_v = prod.get('precio', 0)
                # Si falta el precio de venta, intenta calcularlo dividiendo total entre cantidad.
                if precio_v == 0 and cant > 0:
                    # Calcula un precio de venta aproximado usando el total de la venta.
                    precio_v = v.get('total', 0) / cant
                # Calcula la utilidad multiplicando margen por cantidad vendida.
                ut = (precio_v - precio_c) * cant
                # Evita que la utilidad calculada quede negativa.
                ut = max(0, ut)
            # Acumula la utilidad de la venta en la utilidad total.
            ut_total += ut
            
            # Obtiene el stock actual del producto; si no existe, usa cero.
            stock_actual = prod.get('stock', 0) if prod else 0
            # Reconstruye el stock antes de la venta sumando lo vendido al stock actual.
            stock_inicial = stock_actual + cant
            # Forma un texto que muestra el cambio de stock antes y después de la venta.
            str_stock = f"{stock_inicial}->{stock_actual}"
            
            # Obtiene el método de pago de la venta o usa Efectivo por defecto.
            metodo = v.get('pago', 'Efectivo')
            # Obtiene el código de pago, considerando nombres de campo antiguos si existen.
            cod_pago = v.get('codigo_pago', v.get('Cod', ''))
            # Forma el texto del pago incluyendo código cuando corresponde.
            pago_formateado = f"{metodo} ({cod_pago})" if cod_pago and str(cod_pago).lower() != 'nan' and str(cod_pago).strip() else metodo

            # Obtiene el nombre del producto en ventas simples o antiguas.
            nombre = v.get('nombre', 'Desconocido')
            # Verifica si el nombre del producto es demasiado largo para la tabla.
            if len(nombre) > 23:
                # Recorta el nombre para mantener ordenada la tabla del reporte.
                nombre = nombre[:20] + "..."
                
            # Obtiene la categoría del producto o usa un texto predeterminado.
            categoria = prod.get('categoria', 'Sin Categoría') if prod else 'Sin Categoría'
            # Verifica si el texto de categoría es demasiado largo para la tabla.
            if len(categoria) > 16:
                # Recorta la categoría para que encaje en la tabla.
                categoria = categoria[:14] + ".."
                
            # Verifica si el texto del método de pago es demasiado largo.
            if len(pago_formateado) > 14:
                # Recorta el texto del pago para mantener alineado el reporte.
                pago_formateado = pago_formateado[:12] + ".."

            # Crea una etiqueta legible para identificar cada venta en la tabla.
            texto_venta = f"Venta {num_v}"

            # Muestra información en pantalla para guiar al usuario durante el proceso.
            print(f"{texto_venta:<9} | {v.get('fecha', 'N/A'):<20} | {v.get('codigo', 'N/A'):<6} | {nombre:<25} | {categoria:<18} | {str_stock:<11} | {cant:<5} | {pago_formateado:<15} | S/. {v.get('total', 0):<5.2f} | S/. {ut:<5.2f}")
        
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("-" * 163)
        # Muestra el total de unidades vendidas en el reporte.
        print(f"TOTAL UNIDADES VENDIDAS: {un_total}")
        # Muestra la utilidad total acumulada en el reporte.
        print(f"GANANCIA TOTAL (UTILIDAD): S/. {ut_total:.2f}")
        # Muestra información en pantalla para guiar al usuario durante el proceso.
        print("=" * 163)
