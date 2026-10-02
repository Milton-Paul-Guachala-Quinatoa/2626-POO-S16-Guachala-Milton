from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificacion", datos.get("identificador", "")),
                datos.get("nombre", ""),
                datos.get("correo", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", datos.get("contrasena", "")),
                datos.get("rol", "Administrador" if datos.get("usuario", "") == "Milton" else "Cliente"),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("categoria", ""),
                datos.get("precio", 0),
                datos.get("stock", 0),
            )
            for datos in productos_json
        ]

        # Semana 15: carga las ventas persistidas para mostrarlas en la interfaz.
        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("producto_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contrasena):
        for usuario_registrado in self.usuarios:
            if usuario_registrado.usuario == usuario and usuario_registrado.contrasena == contrasena:
                return usuario_registrado
        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        return self.usuarios

    def listar_productos(self):
        return self.productos

    def listar_ventas(self):
        return self.ventas

    def guardar_usuarios(self):
        datos = [
            {
                "identificacion": usuario.identificacion,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "usuario": usuario.usuario,
                "contraseña": usuario.contrasena,
                "rol": usuario.rol,
            }
            for usuario in self.usuarios
        ]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def guardar_productos(self):
        datos = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "precio": producto.precio,
                "stock": producto.stock,
            }
            for producto in self.productos
        ]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario):
        nombre_usuario = nombre_usuario.strip()
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    def registrar_usuario(self, identificacion, nombre, correo, usuario, contrasena, rol):
        nuevo_usuario = Usuario(identificacion, nombre, correo, usuario, contrasena, rol)

        if nuevo_usuario.rol == "Administrador":
            raise ValueError("No se pueden registrar nuevos administradores desde esta pantalla.")
        if self.buscar_usuario_por_identificacion(nuevo_usuario.identificacion) is not None:
            raise ValueError("Ya existe un usuario con esa identificacion.")
        if self.buscar_usuario_por_nombre_usuario(nuevo_usuario.usuario) is not None:
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return nuevo_usuario

    def actualizar_usuario(self, identificacion, nombre, correo, usuario, contrasena, rol,
                           identificacion_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificacion(identificacion)

        if usuario_actual is None:
            raise ValueError("No existe un usuario con esa identificacion.")

        datos_validados = Usuario(identificacion, nombre, correo, usuario, contrasena, rol)
        usuario_con_mismo_login = self.buscar_usuario_por_nombre_usuario(datos_validados.usuario)
        if (
            usuario_con_mismo_login is not None
            and usuario_con_mismo_login.identificacion != usuario_actual.identificacion
        ):
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        if datos_validados.rol == "Administrador" and identificacion != identificacion_usuario_actual:
            raise ValueError("Solo la cuenta administradora actual puede conservar el rol Administrador.")

        if (
            identificacion_usuario_actual == usuario_actual.identificacion
            and usuario_actual.rol == "Administrador"
            and datos_validados.rol != "Administrador"
        ):
            raise ValueError("No puede cambiar el rol del administrador actual.")

        usuario_actual.nombre = datos_validados.nombre
        usuario_actual.correo = datos_validados.correo
        usuario_actual.usuario = datos_validados.usuario
        usuario_actual.contrasena = datos_validados.contrasena
        usuario_actual.rol = datos_validados.rol
        self.guardar_usuarios()
        return usuario_actual

    def eliminar_usuario(self, identificacion, identificacion_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificacion(identificacion)

        if usuario_actual is None:
            raise ValueError("No existe un usuario con esa identificacion.")
        if usuario_actual.identificacion == identificacion_usuario_actual:
            raise ValueError("No puede eliminar el usuario actualmente autenticado.")

        self.usuarios.remove(usuario_actual)
        self.guardar_usuarios()
        return usuario_actual

    def buscar_producto_por_codigo(self, codigo):
        codigo = codigo.strip()
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def buscar_usuario_por_identificacion(self, identificacion):
        identificacion = identificacion.strip()
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def registrar_producto(self, codigo, nombre, categoria, precio, stock):
        nuevo_producto = Producto(codigo, nombre, categoria, precio, stock)
        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un producto con ese codigo.")
        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(self, codigo, nombre, categoria, precio, stock):
        producto_actual = self.buscar_producto_por_codigo(codigo)
        if producto_actual is None:
            raise ValueError("No existe un producto con ese codigo.")

        datos_validados = Producto(codigo, nombre, categoria, precio, stock)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.categoria = datos_validados.categoria
        producto_actual.precio = datos_validados.precio
        producto_actual.stock = datos_validados.stock
        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo):
        producto_actual = self.buscar_producto_por_codigo(codigo)
        if producto_actual is None:
            raise ValueError("No existe un producto con ese codigo.")
        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual

    def generar_identificador_venta(self):
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def guardar_ventas(self):
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "producto_codigo": venta.producto_codigo,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def registrar_venta(self, usuario_id, producto_codigo):
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if self.buscar_usuario_por_identificacion(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        producto = self.buscar_producto_por_codigo(producto_codigo)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")
        if producto.stock <= 0:
            raise ValueError("No hay stock disponible para el producto seleccionado.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )
        producto.stock -= 1
        self.ventas.append(nueva_venta)
        self.guardar_productos()
        self.guardar_ventas()
        return nueva_venta
