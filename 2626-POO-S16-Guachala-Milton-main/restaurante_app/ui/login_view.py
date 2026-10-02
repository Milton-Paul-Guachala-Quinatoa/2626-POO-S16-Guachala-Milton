import tkinter as tk
from pathlib import Path
from tkinter import ttk


class LoginView(tk.Frame):
    def __init__(self, master, restaurante_servicio, al_iniciar_sesion):
        super().__init__(master, bg="#eaf4f2")
        self.restaurante_servicio = restaurante_servicio
        self.al_iniciar_sesion = al_iniciar_sesion
        self.usuario_entry = None
        self.contrasena_entry = None
        self.mensaje_error = None
        self.logo = None
        self.definir_estilos()
        self.construir_interfaz()

    def definir_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Login.TButton", background="#147d75", foreground="#ffffff",
                         font=("Arial", 11, "bold"), padding=(14, 9), borderwidth=0)
        estilo.map("Login.TButton", background=[("active", "#0f665f")])

    def cargar_logo(self):
        ruta = Path(__file__).resolve().parent.parent / "assets" / "logo" / "logo.png"
        if not ruta.exists():
            return None
        original = tk.PhotoImage(file=str(ruta)).subsample(6, 6)
        self.logo = original
        return self.logo

    def construir_interfaz(self):
        contenedor = tk.Frame(self, bg="#ffffff", padx=38, pady=30,
                              highlightbackground="#d5e5e2", highlightthickness=1)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        logo = self.cargar_logo()
        if logo is not None:
            tk.Label(contenedor, image=logo, bg="#ffffff").pack(pady=(0, 8))

        tk.Label(contenedor, text="Restaurante App", bg="#ffffff", fg="#124e4a",
                 font=("Arial", 22, "bold")).pack(pady=(0, 5))
        tk.Label(contenedor, text="Inicio de sesion", bg="#ffffff", fg="#65736f",
                 font=("Arial", 11)).pack(pady=(0, 22))

        tk.Label(contenedor, text="Usuario", bg="#ffffff", fg="#29423e",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        self.usuario_entry = tk.Entry(contenedor, width=30, font=("Arial", 11),
                                      relief="solid", bd=1)
        self.usuario_entry.pack(pady=(4, 14), ipady=5)
        self.usuario_entry.focus()

        tk.Label(contenedor, text="Contrasena", bg="#ffffff", fg="#29423e",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        self.contrasena_entry = tk.Entry(contenedor, width=30, font=("Arial", 11),
                                         show="*", relief="solid", bd=1)
        self.contrasena_entry.pack(pady=(4, 14), ipady=5)
        self.contrasena_entry.bind("<Return>", lambda evento: self.iniciar_sesion())

        self.mensaje_error = tk.Label(contenedor, text="", bg="#ffffff", fg="#b42318",
                                      font=("Arial", 10))
        self.mensaje_error.pack(pady=(0, 14))

        ttk.Button(contenedor, text="Iniciar sesion", command=self.iniciar_sesion,
                   style="Login.TButton").pack(fill="x")

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contrasena_entry.get().strip()
        if not usuario or not contrasena:
            self.mensaje_error.config(text="Ingrese usuario y contrasena.")
            return
        usuario_validado = self.restaurante_servicio.validar_acceso(usuario, contrasena)
        if usuario_validado is None:
            self.mensaje_error.config(text="Credenciales incorrectas.")
            return
        self.mensaje_error.config(text="")
        self.al_iniciar_sesion(usuario_validado)
