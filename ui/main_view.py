import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path


class MainView(tk.Frame):
    def __init__(
        self,
        master,
        restaurante_servicio,
        usuario_actual,
        al_cerrar_sesion
    ) -> None:
        super().__init__(master)

        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.entradas_producto = {}
        self.tabla_productos = None

        # Variables utilizadas en Ventas
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None

        ruta_base = Path(__file__).resolve().parent.parent
        ruta_assets = ruta_base / "assets"

        self.logo_img = tk.PhotoImage(
        file=ruta_assets / "logo.png"
        ).subsample(10, 10)

        self.icono_productos = tk.PhotoImage(
        file=ruta_assets / "products.png"
        ).subsample(50, 50)

        self.icono_usuarios = tk.PhotoImage(
        file=ruta_assets / "users.png"
        ).subsample(50, 50)

        self.icono_ventas = tk.PhotoImage(
        file=ruta_assets / "sales.png"
        ).subsample(50, 50)

        self.icono_salir = tk.PhotoImage(
        file=ruta_assets / "logout.png"
        ).subsample(50, 50)

        self.icono_agregar = tk.PhotoImage(
        file=ruta_assets / "add.png"
        ).subsample(50, 50)
        self.pack(fill="both", expand=True)

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        encabezado = tk.Frame(self)
        encabezado.pack(fill="x", padx=20, pady=15)
        tk.Label(
            encabezado,
            image=self.logo_img
        ).pack(
            side="left",
            padx=(0, 10)
        )

        titulo = tk.Label(
            encabezado,
            text="Panel principal - Restaurante App",
            font=("Arial", 18, "bold")
        )
        titulo.pack(side="left")

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            image=self.icono_salir,
            compound="left",
            command=self.al_cerrar_sesion
        ).pack(side="right")

        tk.Label(
            self,
            text=f"Bienvenido, {self.usuario_actual.nombre}",
            font=("Arial", 11)
        ).pack(pady=5)

        opciones = ttk.Frame(self)
        opciones.pack(pady=15)

        ttk.Button(
            opciones,
            text="Productos",
            image=self.icono_productos,
            compound="left",
            command=self.mostrar_productos
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            opciones,
            text="Usuarios",
            image=self.icono_usuarios,
            compound="left",
            command=self.mostrar_usuarios
        ).grid(row=0, column=1, padx=8)

        ttk.Button(
            opciones,
            text="Ventas",
            image=self.icono_ventas,
            compound="left",
            command=self.mostrar_ventas
        ).grid(row=0, column=2, padx=8)

        self.area_contenido = ttk.Frame(self)
        self.area_contenido.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.mostrar_productos()

    def limpiar_contenido(self) -> None:
        for componente in self.area_contenido.winfo_children():
            componente.destroy()

    # =========================================================
    # PRODUCTOS
    # =========================================================

    def mostrar_productos(self) -> None:
        self.limpiar_contenido()

        titulo = tk.Label(
            self.area_contenido,
            text="Gestión de productos",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=(0, 10))

        panel_principal = ttk.Frame(self.area_contenido)
        panel_principal.pack(fill="both", expand=True)

        formulario = ttk.LabelFrame(
            panel_principal,
            text="Datos del producto",
            padding=15
        )
        formulario.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        campos = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Categoría:", "categoria"),
            ("Precio:", "precio"),
            ("Stock:", "stock")
        ]

        self.entradas_producto = {}

        for fila, (texto, clave) in enumerate(campos):
            ttk.Label(
                formulario,
                text=texto
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=6
            )

            entrada = ttk.Entry(
                formulario,
                width=24
            )
            entrada.grid(
                row=fila,
                column=1,
                pady=6,
                padx=(10, 0)
            )

            self.entradas_producto[clave] = entrada

        acciones = ttk.LabelFrame(
            formulario,
            text="Acciones",
            padding=10
        )
        acciones.grid(
            row=len(campos),
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0)
        )

        ttk.Button(
            acciones,
            text="Registrar",
            image=self.icono_agregar,
            compound="left",
            command=self.registrar_producto
        ).grid(
            row=0,
            column=0,
            padx=4,
            pady=4
        )

        ttk.Button(
            acciones,
            text="Consultar",
            command=self.consultar_producto
        ).grid(
            row=0,
            column=1,
            padx=4,
            pady=4
        )

        ttk.Button(
            acciones,
            text="Actualizar",
            command=self.actualizar_producto
        ).grid(
            row=1,
            column=0,
            padx=4,
            pady=4
        )

        ttk.Button(
            acciones,
            text="Eliminar",
            command=self.eliminar_producto
        ).grid(
            row=1,
            column=1,
            padx=4,
            pady=4
        )

        ttk.Button(
            formulario,
            text="Limpiar formulario",
            command=self.limpiar_formulario
        ).grid(
            row=len(campos) + 1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(12, 0)
        )

        listado = ttk.LabelFrame(
            panel_principal,
            text="Productos registrados",
            padding=10
        )
        listado.pack(
            side="left",
            fill="both",
            expand=True
        )

        columnas = (
            "codigo",
            "nombre",
            "categoria",
            "precio",
            "stock"
        )

        self.tabla_productos = ttk.Treeview(
            listado,
            columns=columnas,
            show="headings",
            height=14
        )

        self.tabla_productos.heading(
            "codigo",
            text="Código"
        )
        self.tabla_productos.heading(
            "nombre",
            text="Nombre"
        )
        self.tabla_productos.heading(
            "categoria",
            text="Categoría"
        )
        self.tabla_productos.heading(
            "precio",
            text="Precio"
        )
        self.tabla_productos.heading(
            "stock",
            text="Stock"
        )

        self.tabla_productos.column(
            "codigo",
            width=90,
            anchor="center"
        )
        self.tabla_productos.column(
            "nombre",
            width=180
        )
        self.tabla_productos.column(
            "categoria",
            width=120
        )
        self.tabla_productos.column(
            "precio",
            width=80,
            anchor="center"
        )
        self.tabla_productos.column(
            "stock",
            width=70,
            anchor="center"
        )

        barra = ttk.Scrollbar(
            listado,
            orient="vertical",
            command=self.tabla_productos.yview
        )

        self.tabla_productos.configure(
            yscrollcommand=barra.set
        )

        self.tabla_productos.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        self.actualizar_tabla_productos()

    def obtener_datos_formulario(
        self
    ) -> tuple[str, str, str, str, str]:
        return (
            self.entradas_producto["codigo"].get(),
            self.entradas_producto["nombre"].get(),
            self.entradas_producto["categoria"].get(),
            self.entradas_producto["precio"].get(),
            self.entradas_producto["stock"].get()
        )

    def limpiar_formulario(self) -> None:
        for entrada in self.entradas_producto.values():
            entrada.delete(0, tk.END)

        self.entradas_producto["codigo"].focus()

    def actualizar_tabla_productos(self) -> None:
        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        productos = self.restaurante_servicio.listar_productos()

        for producto in productos:
            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"${producto.precio:.2f}",
                    producto.stock
                )
            )

    def registrar_producto(self) -> None:
        datos = self.obtener_datos_formulario()

        exito, mensaje = (
            self.restaurante_servicio.registrar_producto(
                *datos
            )
        )

        if exito:
            messagebox.showinfo(
                "Registro exitoso",
                mensaje
            )

            self.limpiar_formulario()
            self.actualizar_tabla_productos()

        else:
            messagebox.showwarning(
                "No se pudo registrar",
                mensaje
            )

    def consultar_producto(self) -> None:
        codigo = self.entradas_producto[
            "codigo"
        ].get()

        if not codigo.strip():
            messagebox.showwarning(
                "Código requerido",
                "Ingrese el código del producto que desea consultar."
            )
            return

        producto = (
            self.restaurante_servicio.buscar_producto(
                codigo
            )
        )

        if not producto:
            messagebox.showwarning(
                "Producto no encontrado",
                "No existe un producto con ese código."
            )
            return

        self.entradas_producto[
            "codigo"
        ].delete(0, tk.END)

        self.entradas_producto[
            "codigo"
        ].insert(0, producto.codigo)

        self.entradas_producto[
            "nombre"
        ].delete(0, tk.END)

        self.entradas_producto[
            "nombre"
        ].insert(0, producto.nombre)

        self.entradas_producto[
            "categoria"
        ].delete(0, tk.END)

        self.entradas_producto[
            "categoria"
        ].insert(0, producto.categoria)

        self.entradas_producto[
            "precio"
        ].delete(0, tk.END)

        self.entradas_producto[
            "precio"
        ].insert(0, str(producto.precio))

        self.entradas_producto[
            "stock"
        ].delete(0, tk.END)

        self.entradas_producto[
            "stock"
        ].insert(0, str(producto.stock))

        messagebox.showinfo(
            "Consulta realizada",
            "Los datos del producto se cargaron en el formulario."
        )

    def actualizar_producto(self) -> None:
        datos = self.obtener_datos_formulario()

        exito, mensaje = (
            self.restaurante_servicio.actualizar_producto(
                *datos
            )
        )

        if exito:
            messagebox.showinfo(
                "Actualización exitosa",
                mensaje
            )

            self.limpiar_formulario()
            self.actualizar_tabla_productos()

        else:
            messagebox.showwarning(
                "No se pudo actualizar",
                mensaje
            )

    def eliminar_producto(self) -> None:
        codigo = self.entradas_producto[
            "codigo"
        ].get()

        if not codigo.strip():
            messagebox.showwarning(
                "Código requerido",
                "Ingrese el código del producto que desea eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar el producto con código {codigo.upper()}?"
        )

        if not confirmar:
            return

        exito, mensaje = (
            self.restaurante_servicio.eliminar_producto(
                codigo
            )
        )

        if exito:
            messagebox.showinfo(
                "Eliminación exitosa",
                mensaje
            )

            self.limpiar_formulario()
            self.actualizar_tabla_productos()

        else:
            messagebox.showwarning(
                "No se pudo eliminar",
                mensaje
            )

    # =========================================================
    # USUARIOS
    # =========================================================

        # =========================================================
    # USUARIOS - SEMANA 16
    # =========================================================

    def mostrar_usuarios(self) -> None:
        self.limpiar_contenido()

        # -----------------------------------------------------
        # CONTROL DE ACCESO
        # -----------------------------------------------------
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning(
                "Acceso restringido",
                "Solo un usuario con rol Administrador "
                "puede gestionar usuarios."
            )

            tk.Label(
                self.area_contenido,
                text="Acceso restringido a la gestión de usuarios.",
                font=("Arial", 13, "bold")
            ).pack(pady=40)

            return

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------
        titulo = tk.Label(
            self.area_contenido,
            text="Gestión de usuarios",
            font=("Arial", 14, "bold")
        )
        titulo.pack(pady=(0, 10))

        panel_principal = ttk.Frame(
            self.area_contenido
        )
        panel_principal.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # FORMULARIO
        # -----------------------------------------------------
        formulario = ttk.LabelFrame(
            panel_principal,
            text="Datos del usuario",
            padding=15
        )
        formulario.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        self.usuario_identificador_var = tk.StringVar()
        self.usuario_nombre_var = tk.StringVar()
        self.usuario_cuenta_var = tk.StringVar()
        self.usuario_contrasena_var = tk.StringVar()
        self.usuario_rol_var = tk.StringVar()

        # Identificador
        ttk.Label(
            formulario,
            text="Identificador:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=6
        )

        self.usuario_identificador_entry = ttk.Entry(
            formulario,
            textvariable=self.usuario_identificador_var,
            width=25,
            state="readonly"
        )
        self.usuario_identificador_entry.grid(
            row=0,
            column=1,
            padx=(10, 0),
            pady=6
        )

        # Nombre
        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=6
        )

        self.usuario_nombre_entry = ttk.Entry(
            formulario,
            textvariable=self.usuario_nombre_var,
            width=25
        )
        self.usuario_nombre_entry.grid(
            row=1,
            column=1,
            padx=(10, 0),
            pady=6
        )

        # Usuario
        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=6
        )

        self.usuario_cuenta_entry = ttk.Entry(
            formulario,
            textvariable=self.usuario_cuenta_var,
            width=25
        )
        self.usuario_cuenta_entry.grid(
            row=2,
            column=1,
            padx=(10, 0),
            pady=6
        )

        # Contraseña
        ttk.Label(
            formulario,
            text="Contraseña:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=6
        )

        self.usuario_contrasena_entry = ttk.Entry(
            formulario,
            textvariable=self.usuario_contrasena_var,
            width=25,
            show="*"
        )
        self.usuario_contrasena_entry.grid(
            row=3,
            column=1,
            padx=(10, 0),
            pady=6
        )

        # Rol
        ttk.Label(
            formulario,
            text="Rol:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=6
        )

        self.usuario_rol_combo = ttk.Combobox(
            formulario,
            textvariable=self.usuario_rol_var,
            values=(
                "Empleado",
                "Cliente"
            ),
            state="readonly",
            width=22
        )
        self.usuario_rol_combo.grid(
            row=4,
            column=1,
            padx=(10, 0),
            pady=6
        )

        # -----------------------------------------------------
        # BOTONES
        # -----------------------------------------------------
        acciones = ttk.LabelFrame(
            formulario,
            text="Acciones",
            padding=10
        )
        acciones.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0)
        )

        ttk.Button(
            acciones,
            text="Registrar",
            command=self.registrar_usuario
        ).grid(
            row=0,
            column=0,
            padx=4,
            pady=4
        )

        ttk.Button(
            acciones,
            text="Actualizar",
            command=self.actualizar_usuario
        ).grid(
            row=0,
            column=1,
            padx=4,
            pady=4
        )

        ttk.Button(
            acciones,
            text="Eliminar",
            command=self.eliminar_usuario
        ).grid(
            row=1,
            column=0,
            padx=4,
            pady=4
        )

        ttk.Button(
            acciones,
            text="Limpiar",
            command=self.limpiar_formulario_usuario
        ).grid(
            row=1,
            column=1,
            padx=4,
            pady=4
        )

        # -----------------------------------------------------
        # TABLA
        # -----------------------------------------------------
        listado = ttk.LabelFrame(
            panel_principal,
            text="Usuarios registrados",
            padding=10
        )
        listado.pack(
            side="left",
            fill="both",
            expand=True
        )

        columnas = (
            "identificador",
            "nombre",
            "usuario",
            "rol"
        )

        self.tabla_usuarios = ttk.Treeview(
            listado,
            columns=columnas,
            show="headings",
            height=14
        )

        self.tabla_usuarios.heading(
            "identificador",
            text="ID"
        )
        self.tabla_usuarios.heading(
            "nombre",
            text="Nombre"
        )
        self.tabla_usuarios.heading(
            "usuario",
            text="Usuario"
        )
        self.tabla_usuarios.heading(
            "rol",
            text="Rol"
        )

        self.tabla_usuarios.column(
            "identificador",
            width=70,
            anchor="center"
        )
        self.tabla_usuarios.column(
            "nombre",
            width=150
        )
        self.tabla_usuarios.column(
            "usuario",
            width=100
        )
        self.tabla_usuarios.column(
            "rol",
            width=90,
            anchor="center"
        )

        barra = ttk.Scrollbar(
            listado,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )

        self.tabla_usuarios.configure(
            yscrollcommand=barra.set
        )

        self.tabla_usuarios.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # EVENTOS SEMANA 16
        # =====================================================

        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self.al_seleccionar_usuario
        )

        self.usuario_rol_combo.bind(
            "<<ComboboxSelected>>",
            self.al_cambiar_rol
        )

        widgets_formulario = (
            self.usuario_nombre_entry,
            self.usuario_cuenta_entry,
            self.usuario_contrasena_entry,
            self.usuario_rol_combo
        )

        for widget in widgets_formulario:
            widget.bind(
                "<Return>",
                self.al_presionar_enter
            )

            widget.bind(
                "<Escape>",
                self.al_presionar_escape
            )

        self.tabla_usuarios.bind(
            "<Escape>",
            self.al_presionar_escape
        )

        self.actualizar_tabla_usuarios()
        self.limpiar_formulario_usuario()

    # =========================================================
    # OBTENER DATOS
    # =========================================================

    def obtener_datos_formulario_usuario(self):
        return (
            self.usuario_identificador_var.get(),
            self.usuario_nombre_var.get(),
            self.usuario_cuenta_var.get(),
            self.usuario_contrasena_var.get(),
            self.usuario_rol_var.get()
        )

    # =========================================================
    # ACTUALIZAR TABLA
    # =========================================================

    def actualizar_tabla_usuarios(self) -> None:
        for fila in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(fila)

        usuarios = (
            self.restaurante_servicio.listar_usuarios()
        )

        for usuario in usuarios:
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.identificador,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol
                )
            )

    # =========================================================
    # LIMPIAR FORMULARIO
    # =========================================================

    def limpiar_formulario_usuario(self) -> None:
        nuevo_id = (
            self.restaurante_servicio
            .generar_identificador_usuario()
        )

        self.usuario_identificador_var.set(
            nuevo_id
        )

        self.usuario_nombre_var.set("")
        self.usuario_cuenta_var.set("")
        self.usuario_contrasena_var.set("")
        self.usuario_rol_var.set("Cliente")

        if hasattr(self, "tabla_usuarios"):
            seleccion = (
                self.tabla_usuarios.selection()
            )

            if seleccion:
                self.tabla_usuarios.selection_remove(
                    seleccion
                )

        self.usuario_nombre_entry.focus()

    # =========================================================
    # REGISTRAR
    # =========================================================

    def registrar_usuario(self) -> None:
        datos = (
            self.obtener_datos_formulario_usuario()
        )

        exito, mensaje = (
            self.restaurante_servicio.registrar_usuario(
                *datos
            )
        )

        if exito:
            messagebox.showinfo(
                "Registro exitoso",
                mensaje
            )

            self.actualizar_tabla_usuarios()
            self.limpiar_formulario_usuario()

        else:
            messagebox.showwarning(
                "No se pudo registrar",
                mensaje
            )

    # =========================================================
    # ACTUALIZAR
    # =========================================================

    def actualizar_usuario(self) -> None:
        datos = (
            self.obtener_datos_formulario_usuario()
        )

        exito, mensaje = (
            self.restaurante_servicio.actualizar_usuario(
                *datos
            )
        )

        if exito:
            messagebox.showinfo(
                "Actualización exitosa",
                mensaje
            )

            self.actualizar_tabla_usuarios()
            self.limpiar_formulario_usuario()

        else:
            messagebox.showwarning(
                "No se pudo actualizar",
                mensaje
            )

    # =========================================================
    # ELIMINAR
    # =========================================================

    def eliminar_usuario(self) -> None:
        identificador = (
            self.usuario_identificador_var.get()
        )

        if not identificador.strip():
            messagebox.showwarning(
                "Usuario requerido",
                "Seleccione el usuario que desea eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Desea eliminar el usuario seleccionado?"
        )

        if not confirmar:
            return

        exito, mensaje = (
            self.restaurante_servicio.eliminar_usuario(
                identificador,
                self.usuario_actual.identificador
            )
        )

        if exito:
            messagebox.showinfo(
                "Eliminación exitosa",
                mensaje
            )

            self.actualizar_tabla_usuarios()
            self.limpiar_formulario_usuario()

        else:
            messagebox.showwarning(
                "No se pudo eliminar",
                mensaje
            )

    # =========================================================
    # EVENTO TREEVIEW
    # =========================================================

    def al_seleccionar_usuario(self, event) -> None:
        seleccion = (
            self.tabla_usuarios.selection()
        )

        if not seleccion:
            return

        valores = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )

        identificador = valores[0]

        usuario = (
            self.restaurante_servicio
            .buscar_usuario_por_identificador(
                identificador
            )
        )

        if not usuario:
            return

        self.usuario_identificador_var.set(
            usuario.identificador
        )

        self.usuario_nombre_var.set(
            usuario.nombre
        )

        self.usuario_cuenta_var.set(
            usuario.usuario
        )

        self.usuario_contrasena_var.set(
            usuario.contrasena
        )

        self.usuario_rol_var.set(
            usuario.rol
        )

    # =========================================================
    # EVENTO ENTER
    # =========================================================

    def al_presionar_enter(self, event) -> None:
        self.registrar_usuario()

    # =========================================================
    # EVENTO ESCAPE
    # =========================================================

    def al_presionar_escape(self, event) -> None:
        self.limpiar_formulario_usuario()

    # =========================================================
    # EVENTO COMBOBOX
    # =========================================================

    def al_cambiar_rol(self, event) -> None:
        rol = self.usuario_rol_var.get()

        if rol == "Empleado":
            mensaje = (
                "Rol Empleado seleccionado."
            )
        else:
            mensaje = (
                "Rol Cliente seleccionado."
            )

        # Retroalimentación sencilla sin interrumpir
        # el trabajo del usuario.
        print(mensaje)
        
    # =========================================================
    # VENTAS
    # =========================================================

    def mostrar_ventas(self) -> None:
        self.limpiar_contenido()

        titulo = tk.Label(
            self.area_contenido,
            text="Registro de ventas",
            font=("Arial", 14, "bold")
        )
        titulo.pack(
            pady=(0, 10)
        )

        formulario = ttk.LabelFrame(
            self.area_contenido,
            text="Nueva venta",
            padding=15
        )
        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        # Usuarios disponibles
        usuarios = (
            self.restaurante_servicio.listar_usuarios()
        )

        self.opciones_usuarios_venta = {
            f"{usuario.usuario} - {usuario.nombre}":
                usuario.usuario
            for usuario in usuarios
        }

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=8,
            sticky="w"
        )

        self.usuario_venta_combo = ttk.Combobox(
            formulario,
            values=list(
                self.opciones_usuarios_venta.keys()
            ),
            state="readonly",
            width=35
        )

        self.usuario_venta_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        # Productos disponibles
        productos = (
            self.restaurante_servicio.listar_productos()
        )

        self.opciones_productos_venta = {
            f"{producto.codigo} - {producto.nombre}":
                producto.codigo
            for producto in productos
        }

        ttk.Label(
            formulario,
            text="Producto:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=8,
            sticky="w"
        )

        self.producto_venta_combo = ttk.Combobox(
            formulario,
            values=list(
                self.opciones_productos_venta.keys()
            ),
            state="readonly",
            width=35
        )

        self.producto_venta_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=8
        )

        # IMPORTANTE SEMANA 15:
        # command recibe la referencia al callback.
        ttk.Button(
            formulario,
            text="Registrar venta",
            image=self.icono_agregar,
            compound="left",
            command=self.registrar_venta
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=12
        )

        listado = ttk.LabelFrame(
            self.area_contenido,
            text="Ventas registradas",
            padding=10
        )
        listado.pack(
            fill="both",
            expand=True
        )

        columnas = (
            "identificador",
            "usuario",
            "producto",
            "fecha"
        )

        self.tabla_ventas = ttk.Treeview(
            listado,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tabla_ventas.heading(
            "identificador",
            text="Venta"
        )
        self.tabla_ventas.heading(
            "usuario",
            text="Usuario"
        )
        self.tabla_ventas.heading(
            "producto",
            text="Producto"
        )
        self.tabla_ventas.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla_ventas.column(
            "identificador",
            width=90,
            anchor="center"
        )
        self.tabla_ventas.column(
            "usuario",
            width=220
        )
        self.tabla_ventas.column(
            "producto",
            width=220
        )
        self.tabla_ventas.column(
            "fecha",
            width=110,
            anchor="center"
        )

        barra = ttk.Scrollbar(
            listado,
            orient="vertical",
            command=self.tabla_ventas.yview
        )

        self.tabla_ventas.configure(
            yscrollcommand=barra.set
        )

        self.tabla_ventas.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

        self.actualizar_tabla_ventas()

    def registrar_venta(self) -> None:
        texto_usuario = (
            self.usuario_venta_combo.get()
        )

        texto_producto = (
            self.producto_venta_combo.get()
        )

        usuario_id = (
            self.opciones_usuarios_venta.get(
                texto_usuario,
                ""
            )
        )

        producto_codigo = (
            self.opciones_productos_venta.get(
                texto_producto,
                ""
            )
        )

        exito, mensaje = (
            self.restaurante_servicio.registrar_venta(
                usuario_id,
                producto_codigo
            )
        )

        if exito:
            messagebox.showinfo(
                "Venta",
                mensaje
            )

            self.usuario_venta_combo.set("")
            self.producto_venta_combo.set("")

            self.actualizar_tabla_ventas()

        else:
            messagebox.showwarning(
                "No se pudo registrar la venta",
                mensaje
            )

    def actualizar_tabla_ventas(self) -> None:
        for fila in (
            self.tabla_ventas.get_children()
        ):
            self.tabla_ventas.delete(fila)

        ventas = (
            self.restaurante_servicio.listar_ventas()
        )

        for venta in ventas:
            usuario = (
                self.restaurante_servicio.buscar_usuario(
                    venta.usuario_id
                )
            )

            producto = (
                self.restaurante_servicio.buscar_producto(
                    venta.producto_codigo
                )
            )

            if usuario:
                texto_usuario = (
                    f"{usuario.usuario} - "
                    f"{usuario.nombre}"
                )
            else:
                texto_usuario = venta.usuario_id

            if producto:
                texto_producto = (
                    f"{producto.codigo} - "
                    f"{producto.nombre}"
                )
            else:
                texto_producto = (
                    venta.producto_codigo
                )

            self.tabla_ventas.insert(
                "",
                tk.END,
                values=(
                    venta.identificador,
                    texto_usuario,
                    texto_producto,
                    venta.fecha
                )
            )