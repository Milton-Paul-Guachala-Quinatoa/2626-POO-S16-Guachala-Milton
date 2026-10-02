class Usuario:
    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(self, identificacion, nombre, correo, usuario, contrasena, rol):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def validar_texto(valor, campo):
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")
        return valor.strip()

    @property
    def identificacion(self): return self._identificacion
    @identificacion.setter
    def identificacion(self, valor): self._identificacion = self.validar_texto(valor, "identificacion")

    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, valor): self._nombre = self.validar_texto(valor, "nombre")

    @property
    def correo(self): return self._correo
    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor:
            raise ValueError("El correo no es valido.")
        self._correo = valor.strip()

    @property
    def usuario(self): return self._usuario
    @usuario.setter
    def usuario(self, valor): self._usuario = self.validar_texto(valor, "usuario")

    @property
    def contrasena(self): return self._contrasena
    @contrasena.setter
    def contrasena(self, valor): self._contrasena = self.validar_texto(valor, "contrasena")

    @property
    def rol(self): return self._rol
    @rol.setter
    def rol(self, valor):
        rol_validado = self.validar_texto(valor, "rol")
        if rol_validado not in self.ROLES_PERMITIDOS:
            raise ValueError("El rol seleccionado no es valido.")
        self._rol = rol_validado
