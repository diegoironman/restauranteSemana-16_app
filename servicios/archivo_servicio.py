import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, carpeta_datos: Path) -> None:
        self.carpeta_datos = Path(carpeta_datos)

    def _leer_json(self, nombre_archivo: str) -> list:
        ruta = self.carpeta_datos / nombre_archivo

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            if isinstance(datos, list):
                return datos

            return []

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _guardar_json(self, nombre_archivo: str, datos: list) -> None:
        ruta = self.carpeta_datos / nombre_archivo

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    def cargar_productos(self) -> list:
        return self._leer_json("productos.json")

    def guardar_productos(self, productos: list) -> None:
        self._guardar_json(
            "productos.json",
            productos
        )

    def cargar_usuarios(self) -> list:
        return self._leer_json("usuarios.json")

    def guardar_usuarios(self, usuarios: list) -> None:
        self._guardar_json(
            "usuarios.json",
            usuarios
        )

    def cargar_ventas(self) -> list:
        return self._leer_json("ventas.json")

    def guardar_ventas(self, ventas: list) -> None:
        self._guardar_json(
            "ventas.json",
            ventas
        )