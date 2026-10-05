from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.productos = []
        self.usuarios = []
        self.ventas = []

        self._cargar_datos()

    # =========================================================
    # CARGA DE DATOS
    # =========================================================

    def _cargar_datos(self) -> None:
        datos_productos = self.archivo_servicio.cargar_productos()
        datos_usuarios = self.archivo_servicio.cargar_usuarios()
        datos_ventas = self.archivo_servicio.cargar_ventas()

        self.productos = [
            Producto(
                item["codigo"],
                item["nombre"],
                item["categoria"],
                float(item["precio"]),
                int(item["stock"])
            )
            for item in datos_productos
        ]

        self.usuarios = [
            Usuario(
                item["identificador"],
                item["nombre"],
                item["usuario"],
                item["contrasena"],
                item["rol"]
            )
            for item in datos_usuarios
        ]

        self.ventas = [
            Venta(
                item["identificador"],
                item["usuario_id"],
                item["producto_codigo"],
                item["fecha"]
            )
            for item in datos_ventas
        ]

    # =========================================================
    # PERSISTENCIA
    # =========================================================

    def _guardar_productos(self) -> None:
        productos_json = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "precio": producto.precio,
                "stock": producto.stock
            }
            for producto in self.productos
        ]

        self.archivo_servicio.guardar_productos(productos_json)

    def _guardar_usuarios(self) -> None:
        usuarios_json = [
            usuario.convertir_a_diccionario()
            for usuario in self.usuarios
        ]

        self.archivo_servicio.guardar_usuarios(usuarios_json)

    def _guardar_ventas(self) -> None:
        ventas_json = [
            venta.convertir_a_diccionario()
            for venta in self.ventas
        ]

        self.archivo_servicio.guardar_ventas(ventas_json)

    # =========================================================
    # VALIDACIONES DE PRODUCTOS
    # =========================================================

    def _validar_datos_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: str,
        stock: str
    ) -> tuple[bool, str, float | None, int | None]:

        if not codigo or not nombre or not categoria:
            return (
                False,
                "Código, nombre y categoría son obligatorios.",
                None,
                None
            )

        try:
            precio_numero = float(precio)
            stock_numero = int(stock)
        except ValueError:
            return (
                False,
                "El precio debe ser numérico y el stock un número entero.",
                None,
                None
            )

        if precio_numero < 0:
            return False, "El precio no puede ser negativo.", None, None

        if stock_numero < 0:
            return False, "El stock no puede ser negativo.", None, None

        return True, "", precio_numero, stock_numero

    # =========================================================
    # VALIDACIONES DE USUARIOS
    # =========================================================

    def _validar_datos_usuario(
        self,
        identificador: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str
    ) -> tuple[bool, str]:

        if not identificador.strip():
            return False, "El identificador es obligatorio."

        if not nombre.strip():
            return False, "El nombre es obligatorio."

        if not usuario.strip():
            return False, "El nombre de usuario es obligatorio."

        if not contrasena.strip():
            return False, "La contraseña es obligatoria."

        if rol not in ("Empleado", "Cliente"):
            return (
                False,
                "Desde esta sección solo se pueden gestionar "
                "usuarios con rol Empleado o Cliente."
            )

        return True, ""

    # =========================================================
    # LOGIN
    # =========================================================

    def validar_acceso(self, usuario: str, contrasena: str):
        usuario = usuario.strip()
        contrasena = contrasena.strip()

        for persona in self.usuarios:
            if (
                persona.usuario == usuario
                and persona.contrasena == contrasena
            ):
                return persona

        return None

    def es_administrador(self, usuario: Usuario) -> bool:
        return usuario.rol == "Administrador"

    # =========================================================
    # LISTADOS
    # =========================================================

    def listar_productos(self) -> list[Producto]:
        return self.productos.copy()

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios.copy()

    def listar_ventas(self) -> list[Venta]:
        return self.ventas.copy()

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    # =========================================================
    # BÚSQUEDAS
    # =========================================================

    def buscar_producto(self, codigo: str):
        codigo = codigo.strip().upper()

        for producto in self.productos:
            if producto.codigo.upper() == codigo:
                return producto

        return None

    def buscar_usuario(self, usuario_id: str):
        """
        Busca por nombre de usuario.

        Se conserva este método porque la sección de Ventas
        de la Semana 15 ya trabaja con usuario.usuario.
        """
        usuario_id = usuario_id.strip()

        for usuario in self.usuarios:
            if usuario.usuario == usuario_id:
                return usuario

        return None

    def buscar_usuario_por_identificador(self, identificador: str):
        identificador = identificador.strip().upper()

        for usuario in self.usuarios:
            if usuario.identificador.upper() == identificador:
                return usuario

        return None

    # =========================================================
    # GESTIÓN DE USUARIOS - SEMANA 16
    # =========================================================

    def generar_identificador_usuario(self) -> str:
        numero = 1

        while True:
            identificador = f"U{numero:03d}"

            if not self.buscar_usuario_por_identificador(identificador):
                return identificador

            numero += 1

    def registrar_usuario(
        self,
        identificador: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str
    ) -> tuple[bool, str]:

        identificador = identificador.strip().upper()
        nombre = nombre.strip()
        usuario = usuario.strip()
        contrasena = contrasena.strip()
        rol = rol.strip()

        valido, mensaje = self._validar_datos_usuario(
            identificador,
            nombre,
            usuario,
            contrasena,
            rol
        )

        if not valido:
            return False, mensaje

        if self.buscar_usuario_por_identificador(identificador):
            return False, "Ya existe un usuario con ese identificador."

        if self.buscar_usuario(usuario):
            return False, "Ya existe una cuenta con ese nombre de usuario."

        nuevo_usuario = Usuario(
            identificador,
            nombre,
            usuario,
            contrasena,
            rol
        )

        self.usuarios.append(nuevo_usuario)
        self._guardar_usuarios()

        return True, "Usuario registrado correctamente."

    def actualizar_usuario(
        self,
        identificador: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str
    ) -> tuple[bool, str]:

        identificador = identificador.strip().upper()
        nombre = nombre.strip()
        usuario = usuario.strip()
        contrasena = contrasena.strip()
        rol = rol.strip()

        usuario_existente = self.buscar_usuario_por_identificador(
            identificador
        )

        if not usuario_existente:
            return False, "No existe un usuario con ese identificador."

        if usuario_existente.rol == "Administrador":
            return (
                False,
                "Las cuentas Administrador no se modifican "
                "desde esta sección."
            )

        valido, mensaje = self._validar_datos_usuario(
            identificador,
            nombre,
            usuario,
            contrasena,
            rol
        )

        if not valido:
            return False, mensaje

        otro_usuario = self.buscar_usuario(usuario)

        if (
            otro_usuario
            and otro_usuario.identificador != identificador
        ):
            return (
                False,
                "Ya existe otra cuenta con ese nombre de usuario."
            )

        usuario_existente.nombre = nombre
        usuario_existente.usuario = usuario
        usuario_existente.contrasena = contrasena
        usuario_existente.rol = rol

        self._guardar_usuarios()

        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(
        self,
        identificador: str,
        identificador_administrador_actual: str
    ) -> tuple[bool, str]:

        identificador = identificador.strip().upper()
        identificador_administrador_actual = (
            identificador_administrador_actual.strip().upper()
        )

        usuario = self.buscar_usuario_por_identificador(
            identificador
        )

        if not usuario:
            return False, "No existe un usuario con ese identificador."

        if identificador == identificador_administrador_actual:
            return (
                False,
                "No puede eliminar la cuenta administrativa "
                "con la que inició sesión."
            )

        if usuario.rol == "Administrador":
            return (
                False,
                "Las cuentas Administrador no pueden eliminarse "
                "desde esta sección."
            )

        self.usuarios.remove(usuario)
        self._guardar_usuarios()

        return True, "Usuario eliminado correctamente."

    # =========================================================
    # VENTAS
    # =========================================================

    def generar_identificador_venta(self) -> str:
        numero = len(self.ventas) + 1
        return f"V{numero:03d}"

    def registrar_venta(
        self,
        usuario_id: str,
        producto_codigo: str
    ) -> tuple[bool, str]:

        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip().upper()

        if not usuario_id or not producto_codigo:
            return False, "Debe seleccionar un usuario y un producto."

        usuario = self.buscar_usuario(usuario_id)

        if not usuario:
            return False, "El usuario seleccionado no existe."

        producto = self.buscar_producto(producto_codigo)

        if not producto:
            return False, "El producto seleccionado no existe."

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario.usuario,
            producto.codigo,
            date.today().strftime("%d/%m/%Y")
        )

        self.ventas.append(nueva_venta)
        self._guardar_ventas()

        return True, "Venta registrada correctamente."

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: str,
        stock: str
    ) -> tuple[bool, str]:

        codigo = codigo.strip().upper()
        nombre = nombre.strip()
        categoria = categoria.strip()

        valido, mensaje, precio_numero, stock_numero = (
            self._validar_datos_producto(
                codigo,
                nombre,
                categoria,
                precio,
                stock
            )
        )

        if not valido:
            return False, mensaje

        if self.buscar_producto(codigo):
            return False, "Ya existe un producto con ese código."

        nuevo_producto = Producto(
            codigo,
            nombre,
            categoria,
            precio_numero,
            stock_numero
        )

        self.productos.append(nuevo_producto)
        self._guardar_productos()

        return True, "Producto registrado correctamente."

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: str,
        stock: str
    ) -> tuple[bool, str]:

        codigo = codigo.strip().upper()
        nombre = nombre.strip()
        categoria = categoria.strip()

        producto = self.buscar_producto(codigo)

        if not producto:
            return False, "No existe un producto con ese código."

        valido, mensaje, precio_numero, stock_numero = (
            self._validar_datos_producto(
                codigo,
                nombre,
                categoria,
                precio,
                stock
            )
        )

        if not valido:
            return False, mensaje

        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio_numero
        producto.stock = stock_numero

        self._guardar_productos()

        return True, "Producto actualizado correctamente."

    def eliminar_producto(
        self,
        codigo: str
    ) -> tuple[bool, str]:

        producto = self.buscar_producto(codigo)

        if not producto:
            return False, "No existe un producto con ese código."

        self.productos.remove(producto)
        self._guardar_productos()

        return True, "Producto eliminado correctamente."