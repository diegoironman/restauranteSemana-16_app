class Usuario:
    ROLES_VALIDOS = (
        "Administrador",
        "Empleado",
        "Cliente"
    )

    def __init__(
        self,
        identificador: str,
        nombre: str,
        usuario: str,
        contrasena: str,
        rol: str
    ) -> None:
        self.identificador = identificador.strip().upper()
        self.nombre = nombre.strip()
        self.usuario = usuario.strip()
        self.contrasena = contrasena.strip()
        self.rol = rol.strip()

        if not self.identificador:
            raise ValueError(
                "El identificador no puede estar vacío."
            )

        if not self.nombre:
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if not self.usuario:
            raise ValueError(
                "El usuario no puede estar vacío."
            )

        if not self.contrasena:
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        if self.rol not in self.ROLES_VALIDOS:
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )

    def convertir_a_diccionario(self) -> dict:
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    def __str__(self) -> str:
        return (
            f"{self.identificador} - "
            f"{self.nombre} - "
            f"{self.usuario} - "
            f"{self.rol}"
        )