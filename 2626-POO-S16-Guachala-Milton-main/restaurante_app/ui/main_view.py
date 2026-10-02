import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f5f8f7")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}
        self.iconos = {}
        self.logo_sidebar = None
        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_categoria_entry = None
        self.producto_precio_entry = None
        self.producto_stock_entry = None
        self.tabla_productos = None
        self.usuario_identificacion_entry = None
        self.usuario_nombre_entry = None
        self.usuario_correo_entry = None
        self.usuario_login_entry = None
        self.usuario_contrasena_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_estado = None
        self.usuario_identificacion_seleccionada = None
        self.tabla_usuarios = None
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}
        self.definir_estilos()
        self.construir_interfaz()

    def definir_estilos(self):
        self.color_fondo = "#f5f8f7"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#164e4a"
        self.color_texto = "#29423e"
        self.color_secundario = "#dceeea"
        self.color_resaltado = "#147d75"
        self.color_dorado = "#c99a2e"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("MenuApp.TButton", background="#23645f", foreground="#ffffff",
                         font=("Arial", 10, "bold"), padding=(12, 10), borderwidth=0, anchor="w")
        estilo.map("MenuApp.TButton", background=[("active", "#2d7a73")])
        estilo.configure("MenuActivo.TButton", background=self.color_resaltado, foreground="#ffffff",
                         font=("Arial", 10, "bold"), padding=(12, 10), borderwidth=0, anchor="w")
        estilo.map("MenuActivo.TButton", background=[("active", "#0f665f")])
        estilo.configure("Secundario.TButton", background="#dceeea", foreground="#164e4a",
                         font=("Arial", 10, "bold"), padding=(10, 7), borderwidth=0)
        estilo.configure("Accion.TButton", background="#147d75", foreground="#ffffff",
                         font=("Arial", 10, "bold"), padding=(10, 7), borderwidth=0)
        estilo.map("Accion.TButton", background=[("active", "#0f665f")])
        estilo.configure("Eliminar.TButton", background="#c45151", foreground="#ffffff",
                         font=("Arial", 10, "bold"), padding=(10, 7), borderwidth=0)
        estilo.map("Eliminar.TButton", background=[("active", "#a63f3f")])
        estilo.configure("Treeview.Heading", background="#dceeea", foreground="#164e4a",
                         font=("Arial", 10, "bold"))
        estilo.configure("Treeview", rowheight=28, font=("Arial", 10), fieldbackground="#ffffff")

    def cargar_icono(self, nombre_archivo):
        ruta = Path(__file__).resolve().parent.parent / "assets" / "icons" / nombre_archivo
        if not ruta.exists():
            return None
        icono = tk.PhotoImage(file=str(ruta))
        self.iconos[nombre_archivo] = icono
        return icono

    def cargar_logo(self):
        ruta = Path(__file__).resolve().parent.parent / "assets" / "logo" / "icono.png"
        if not ruta.exists():
            return None
        self.logo_sidebar = tk.PhotoImage(file=str(ruta)).subsample(4, 4)
        return self.logo_sidebar

    def crear_boton(self, contenedor, texto, comando, estilo, icono=None):
        imagen = self.cargar_icono(icono) if icono else None
        if imagen:
            return ttk.Button(contenedor, text=texto, command=comando, style=estilo,
                              image=imagen, compound="left")
        return ttk.Button(contenedor, text=texto, command=comando, style=estilo)

    def construir_interfaz(self):
        sidebar = tk.Frame(self, bg=self.color_encabezado, width=205, padx=15, pady=18)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = self.cargar_logo()
        if logo:
            tk.Label(sidebar, image=logo, bg=self.color_encabezado).pack(anchor="center", pady=(0, 6))
        tk.Label(sidebar, text="RESTAURANTE APP", bg=self.color_encabezado, fg="#ffffff",
                 font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(sidebar, text=self.usuario_actual.nombre, bg=self.color_encabezado, fg="#d8ebe7",
                 font=("Arial", 10), wraplength=170, justify="left").pack(anchor="w", pady=(0, 22))

        self.crear_boton_menu(sidebar, "Inicio", self.mostrar_inicio, "home.png")
        if self.usuario_actual.rol == "Administrador":
            self.crear_boton_menu(sidebar, "Usuarios", self.mostrar_usuarios, "users.png")
        self.crear_boton_menu(sidebar, "Productos", self.mostrar_productos, "books.png")
        self.crear_boton_menu(sidebar, "Ventas", self.mostrar_ventas, "sales.png")

        tk.Frame(sidebar, bg=self.color_encabezado).pack(fill="both", expand=True)
        self.crear_boton(sidebar, "Cerrar sesion", self.cerrar_sesion, "Eliminar.TButton", "logout.png").pack(fill="x", pady=(16, 0))

        principal = tk.Frame(self, bg=self.color_fondo)
        principal.pack(side="left", fill="both", expand=True)
        self.contenido = tk.Frame(principal, bg=self.color_fondo, padx=28, pady=24)
        self.contenido.pack(fill="both", expand=True)
        barra_estado = tk.Frame(principal, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")
        self.etiqueta_estado = tk.Label(barra_estado, bg=self.color_secundario, fg=self.color_texto,
                                        font=("Arial", 10))
        self.etiqueta_estado.pack(side="left")
        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando, icono):
        boton = self.crear_boton(contenedor, texto, comando, "MenuApp.TButton", icono)
        boton.pack(fill="x", pady=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            boton.configure(style="MenuActivo.TButton" if texto == seccion else "MenuApp.TButton")

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_barra_estado(self):
        self.etiqueta_estado.config(text=(f"Productos: {self.restaurante_servicio.cantidad_productos()} | "
                                          f"Usuarios: {self.restaurante_servicio.cantidad_usuarios()} | "
                                          f"Ventas: {self.restaurante_servicio.cantidad_ventas()} | Datos JSON locales"))

    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()
        self.crear_titulo_seccion("Panel principal")
        tk.Label(self.contenido, text="Consulte usuarios y gestione los productos desde el menu lateral.",
                 bg=self.color_fondo, fg=self.color_texto, font=("Arial", 12)).pack(anchor="w", pady=(0, 22))
        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")
        self.crear_tarjeta_resumen(resumen, "Usuarios registrados", self.restaurante_servicio.cantidad_usuarios())
        self.crear_tarjeta_resumen(resumen, "Productos registrados", self.restaurante_servicio.cantidad_productos())

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16,
                           highlightbackground="#d8e6e2", highlightthickness=1)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))
        tk.Label(tarjeta, text=titulo, bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(tarjeta, text=str(valor), bg=self.color_panel, fg=self.color_resaltado,
                 font=("Arial", 24, "bold")).pack(anchor="w", pady=(8, 0))

    def mostrar_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showerror("Usuarios", "Solo el administrador puede acceder a esta seccion.")
            return

        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()
        self.crear_titulo_seccion("Gestion de usuarios")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(cuerpo, text="Datos del usuario", bg=self.color_panel,
                                   fg=self.color_encabezado, font=("Arial", 10, "bold"),
                                   padx=14, pady=14)
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_identificacion_entry = self.crear_campo(formulario, "Identificacion", 0)
        self.usuario_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.usuario_correo_entry = self.crear_campo(formulario, "Correo", 2)
        self.usuario_login_entry = self.crear_campo(formulario, "Usuario", 3)
        self.usuario_contrasena_entry = self.crear_campo(formulario, "Contrasena", 4, show="*")

        tk.Label(formulario, text="Rol", bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="w",
                                                  pady=(0, 8), padx=(0, 10))

        self.usuario_rol_combo = ttk.Combobox(
            formulario, values=("Empleado", "Cliente"), state="readonly", width=25
        )
        self.usuario_rol_combo.grid(row=5, column=1, sticky="ew", pady=(0, 8))
        self.usuario_rol_combo.set("Cliente")

        self.usuario_rol_estado = tk.Label(
            formulario, text="Rol seleccionado: Cliente", bg=self.color_panel,
            fg=self.color_texto, font=("Arial", 9)
        )
        self.usuario_rol_estado.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 8))

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_usuario, "Accion.TButton", "add.png"),
            ("Actualizar", self.actualizar_usuario, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_usuario, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_usuario, "Secundario.TButton", "clean.png"),
        )
        for texto, comando, estilo, icono in botones:
            self.crear_boton(acciones, texto, comando, estilo, icono).pack(fill="x", pady=(0, 7))

        listado = self.crear_listado(cuerpo, "Usuarios registrados", usar_grid=True)
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificacion", "nombre", "usuario", "correo", "rol"),
            ("Identificacion", "Nombre", "Usuario", "Correo", "Rol"),
        )

        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
        self.usuario_rol_combo.bind("<Return>", self.al_presionar_enter)
        for widget in (
            self.usuario_identificacion_entry,
            self.usuario_nombre_entry,
            self.usuario_correo_entry,
            self.usuario_login_entry,
            self.usuario_contrasena_entry,
            self.usuario_rol_combo,
            self.tabla_usuarios,
        ):
            widget.bind("<Escape>", self.al_presionar_escape)
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self.al_seleccionar_rol)

        self.refrescar_usuarios()

    def refrescar_usuarios(self):
        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.correo,
                    usuario.rol,
                ),
            )
        self.actualizar_barra_estado()

    def obtener_datos_usuario(self):
        return (
            self.usuario_identificacion_entry.get(),
            self.usuario_nombre_entry.get(),
            self.usuario_correo_entry.get(),
            self.usuario_login_entry.get(),
            self.usuario_contrasena_entry.get(),
            self.usuario_rol_combo.get(),
        )

    def registrar_usuario(self):
        try:
            self.restaurante_servicio.registrar_usuario(*self.obtener_datos_usuario())
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def al_seleccionar_usuario(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        valores = self.tabla_usuarios.item(seleccion[0], "values")
        if not valores:
            return

        identificacion = valores[0]
        usuario = self.restaurante_servicio.buscar_usuario_por_identificacion(identificacion)
        if usuario is None:
            return

        self.cargar_usuario_en_formulario(usuario)

    def cargar_usuario_en_formulario(self, usuario):
        self.limpiar_campos_usuario()
        self.usuario_identificacion_seleccionada = usuario.identificacion
        self.usuario_identificacion_entry.insert(0, usuario.identificacion)
        self.usuario_nombre_entry.insert(0, usuario.nombre)
        self.usuario_correo_entry.insert(0, usuario.correo)
        self.usuario_login_entry.insert(0, usuario.usuario)
        self.usuario_contrasena_entry.insert(0, usuario.contrasena)

        if (
            usuario.identificacion == self.usuario_actual.identificacion
            and usuario.rol == "Administrador"
        ):
            self.usuario_rol_combo.configure(values=("Administrador",), state="disabled")
        else:
            self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")

        self.usuario_rol_combo.set(usuario.rol)
        self.actualizar_texto_rol(usuario.rol)

    def actualizar_usuario(self):
        if self.usuario_identificacion_seleccionada is None:
            messagebox.showerror("Usuarios", "Seleccione un usuario de la tabla.")
            return

        identificacion, nombre, correo, usuario, contrasena, rol = self.obtener_datos_usuario()
        if identificacion != self.usuario_identificacion_seleccionada:
            messagebox.showerror("Usuarios", "No cambie la identificacion del usuario seleccionado.")
            return

        try:
            self.restaurante_servicio.actualizar_usuario(
                identificacion,
                nombre,
                correo,
                usuario,
                contrasena,
                rol,
                self.usuario_actual.identificacion,
            )
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def eliminar_usuario(self):
        if self.usuario_identificacion_seleccionada is None:
            messagebox.showerror("Usuarios", "Seleccione un usuario de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Usuarios",
            "Desea eliminar el usuario seleccionado?",
        )
        if not confirmar:
            return

        try:
            self.restaurante_servicio.eliminar_usuario(
                self.usuario_identificacion_seleccionada,
                self.usuario_actual.identificacion,
            )
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def limpiar_campos_usuario(self):
        for entrada in (
            self.usuario_identificacion_entry,
            self.usuario_nombre_entry,
            self.usuario_correo_entry,
            self.usuario_login_entry,
            self.usuario_contrasena_entry,
        ):
            entrada.delete(0, tk.END)

    def limpiar_formulario_usuario(self):
        self.limpiar_campos_usuario()
        self.usuario_identificacion_seleccionada = None
        self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")
        self.usuario_rol_combo.set("Cliente")
        self.actualizar_texto_rol("Cliente")

        if self.tabla_usuarios is not None:
            for item in self.tabla_usuarios.selection():
                self.tabla_usuarios.selection_remove(item)

        self.usuario_identificacion_entry.focus()

    def al_presionar_enter(self, event):
        # Semana 16: Enter ejecuta el registro mediante un evento de teclado.
        self.registrar_usuario()

    def al_presionar_escape(self, event):
        # Semana 16: Escape cancela la seleccion y limpia el formulario.
        self.limpiar_formulario_usuario()

    def al_seleccionar_rol(self, event):
        self.actualizar_texto_rol(self.usuario_rol_combo.get())

    def actualizar_texto_rol(self, rol):
        if self.usuario_rol_estado is not None:
            self.usuario_rol_estado.config(text=f"Rol seleccionado: {rol}")

    def mostrar_productos(self):
        self.marcar_seccion("Productos")
        self.limpiar_contenido()
        self.crear_titulo_seccion("Gestion de productos")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(cuerpo, text="Datos del producto", bg=self.color_panel,
                                   fg=self.color_encabezado, font=("Arial", 10, "bold"),
                                   padx=14, pady=14)
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))
        formulario.grid_columnconfigure(1, weight=1)

        self.producto_codigo_entry = self.crear_campo(formulario, "Codigo", 0)
        self.producto_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.producto_categoria_entry = self.crear_campo(formulario, "Categoria", 2)
        self.producto_precio_entry = self.crear_campo(formulario, "Precio", 3)
        self.producto_stock_entry = self.crear_campo(formulario, "Stock", 4)

        acciones = tk.LabelFrame(cuerpo, text="Acciones", bg=self.color_panel,
                                 fg=self.color_encabezado, font=("Arial", 10, "bold"),
                                 padx=14, pady=14)
        acciones.grid(row=0, column=0, sticky="s", padx=(0, 18), pady=(0, 0))

        botones = [
            ("Registrar", self.registrar_producto, "Accion.TButton", "add.png"),
            ("Cargar / Consultar", self.cargar_producto_en_formulario, "Secundario.TButton", "search.png"),
            ("Actualizar", self.actualizar_producto, "Accion.TButton", "edit.png"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton", "delete.png"),
            ("Limpiar", self.limpiar_formulario_producto, "Secundario.TButton", "clean.png"),
        ]
        for texto, comando, estilo, icono in botones:
            self.crear_boton(acciones, texto, comando, estilo, icono).pack(fill="x", pady=(0, 7))

        listado = self.crear_listado(cuerpo, "Productos registrados", usar_grid=True)
        self.tabla_productos = self.crear_tabla(listado,
                                                ("codigo", "nombre", "categoria", "precio", "stock"),
                                                ("Codigo", "Nombre", "Categoria", "Precio", "Stock"))
        self.refrescar_productos()

    def obtener_datos_producto(self):
        return (self.producto_codigo_entry.get(), self.producto_nombre_entry.get(),
                self.producto_categoria_entry.get(), self.producto_precio_entry.get(),
                self.producto_stock_entry.get())

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(*self.obtener_datos_producto())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def cargar_producto_en_formulario(self):
        codigo = self.producto_codigo_entry.get().strip()
        producto = self.restaurante_servicio.buscar_producto_por_codigo(codigo)
        if producto is None:
            messagebox.showerror("Productos", "No existe un producto con ese codigo.")
            return
        self.limpiar_formulario_producto()
        self.producto_codigo_entry.insert(0, producto.codigo)
        self.producto_nombre_entry.insert(0, producto.nombre)
        self.producto_categoria_entry.insert(0, producto.categoria)
        self.producto_precio_entry.insert(0, str(producto.precio))
        self.producto_stock_entry.insert(0, str(producto.stock))

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(*self.obtener_datos_producto())
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def eliminar_producto(self):
        try:
            self.restaurante_servicio.eliminar_producto(self.producto_codigo_entry.get())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def limpiar_formulario_producto(self):
        for entrada in (self.producto_codigo_entry, self.producto_nombre_entry,
                        self.producto_categoria_entry, self.producto_precio_entry,
                        self.producto_stock_entry):
            if entrada is not None:
                entrada.delete(0, tk.END)

    def refrescar_productos(self):
        self.limpiar_tabla(self.tabla_productos)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert("", tk.END, values=(producto.codigo, producto.nombre,
                                                              producto.categoria, f"${producto.precio:.2f}", producto.stock))
        self.actualizar_barra_estado()

    def mostrar_ventas(self):
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()
        self.crear_titulo_seccion("Ventas")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(cuerpo, text="Registrar venta", bg=self.color_panel,
                                   fg=self.color_encabezado, font=("Arial", 10, "bold"),
                                   padx=14, pady=14)
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_venta_combo = self.crear_selector_venta(formulario, "Usuario", 0,
                                                              self.obtener_opciones_usuarios_venta())
        self.producto_venta_combo = self.crear_selector_venta(formulario, "Producto", 1,
                                                               self.obtener_opciones_productos_venta())

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # El boton usa command= para ejecutar el callback de venta al hacer clic.
        self.crear_boton(acciones, "Registrar venta", self.registrar_venta,
                         "Accion.TButton", "add.png").pack(fill="x")

        listado = self.crear_listado(cuerpo, "Ventas registradas", usar_grid=True)
        self.tabla_ventas = self.crear_tabla(listado,
                                             ("identificador", "usuario", "producto", "fecha"),
                                             ("Venta", "Usuario", "Producto", "Fecha"))
        self.refrescar_ventas()

    def crear_selector_venta(self, contenedor, etiqueta, fila, opciones):
        tk.Label(contenedor, text=etiqueta, bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 10, "bold")).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        selector = ttk.Combobox(contenedor, values=list(opciones.keys()), state="readonly", width=30)
        selector.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return selector

    def obtener_opciones_usuarios_venta(self):
        self.opciones_usuarios_venta = {
            f"{usuario.identificacion} - {usuario.nombre}": usuario.identificacion
            for usuario in self.restaurante_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        self.opciones_productos_venta = {
            f"{producto.codigo} - {producto.nombre}": producto.codigo
            for producto in self.restaurante_servicio.listar_productos()
        }
        return self.opciones_productos_venta

    def registrar_venta(self):
        usuario_id = self.opciones_usuarios_venta.get(self.usuario_venta_combo.get(), "")
        producto_codigo = self.opciones_productos_venta.get(self.producto_venta_combo.get(), "")
        try:
            # Delega la relacion usuario-producto y la persistencia al servicio.
            self.restaurante_servicio.registrar_venta(usuario_id, producto_codigo)
            self.limpiar_formulario_venta()
            self.refrescar_ventas()
            self.refrescar_productos()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as error:
            messagebox.showerror("Ventas", str(error))

    def limpiar_formulario_venta(self):
        self.usuario_venta_combo.set("")
        self.producto_venta_combo.set("")

    def refrescar_ventas(self):
        self.limpiar_tabla(self.tabla_ventas)
        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario_por_identificacion(venta.usuario_id)
            producto = self.restaurante_servicio.buscar_producto_por_codigo(venta.producto_codigo)
            texto_usuario = venta.usuario_id if usuario is None else f"{usuario.identificacion} - {usuario.nombre}"
            texto_producto = venta.producto_codigo if producto is None else f"{producto.codigo} - {producto.nombre}"
            self.tabla_ventas.insert("", tk.END, values=(venta.identificador, texto_usuario,
                                                          texto_producto, venta.fecha))
        # Refresca la tabla para mostrar de inmediato la respuesta del sistema.
        self.actualizar_barra_estado()

    def crear_titulo_seccion(self, texto):
        tk.Label(self.contenido, text=texto, bg=self.color_fondo, fg=self.color_encabezado,
                 font=("Arial", 20, "bold")).pack(anchor="w", pady=(0, 16))

    def crear_campo(self, contenedor, etiqueta, fila, show=None):
        tk.Label(contenedor, text=etiqueta, bg=self.color_panel, fg=self.color_texto,
                 font=("Arial", 10, "bold")).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        entrada = tk.Entry(contenedor, width=25, font=("Arial", 10), relief="solid", bd=1, show=show)
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(contenedor, text=titulo, bg=self.color_panel, fg=self.color_encabezado,
                                font=("Arial", 10, "bold"), padx=12, pady=12)
        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)
        return listado

    def crear_tabla(self, contenedor, columnas, encabezados):
        frame = tk.Frame(contenedor, bg=self.color_panel)
        frame.pack(fill="both", expand=True)
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=125, anchor="w")
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        if tabla is None:
            return
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()
