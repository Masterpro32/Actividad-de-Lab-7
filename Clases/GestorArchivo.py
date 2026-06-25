import json
import os


class GestorArchivos:
    def __init__(self, nombre_archivo="libreria_datos.json"):
        carpeta_clases = os.path.dirname(os.path.abspath(__file__))
        carpeta_proyecto = os.path.dirname(carpeta_clases)
        self.archivo = os.path.join(carpeta_proyecto, nombre_archivo)

    def cargar_datos(self):
        if not os.path.exists(self.archivo):
            return [], []

        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            productos = datos.get("productos", [])
            ventas = datos.get("ventas", [])

            if isinstance(productos, list) and isinstance(ventas, list):
                return productos, ventas
            return [], []
        except (json.JSONDecodeError, OSError, TypeError):
            return [], []

    def guardar_datos(self, productos, ventas):
        datos = {
            "productos": productos,
            "ventas": ventas
        }

        try:
            with open(self.archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            print("Datos guardados correctamente.")
            return True
        except OSError:
            print("Error: no se pudieron guardar los datos.")
            return False
