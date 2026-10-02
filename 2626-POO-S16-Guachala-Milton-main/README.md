# Restaurante App - Semana 16

## Estudiante

Milton Paul Guachala Quinatoa

## Descripción

En esta Semana 16 seguí trabajando con el mismo proyecto `restaurante_app` que ya venía haciendo desde la Semana 15.

En esta versión mantuve las partes que ya tenía, como el inicio de sesión, la navegación, los productos, las ventas y los archivos JSON donde se guardan los datos.

Lo principal que hice esta semana fue mejorar la parte de **Usuarios**. Ahora el administrador puede registrar, consultar, actualizar y eliminar usuarios desde la aplicación. Para esto utilicé un formulario y una tabla `Treeview`.

También agregué el atributo `rol` en la clase `Usuario`, para poder diferenciar entre `Administrador`, `Empleado` y `Cliente`.

En esta actividad aprendí un poco más sobre cómo funcionan los eventos en Tkinter, principalmente usando `bind()`, callbacks y algunos eventos del teclado.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── icons/
│   └── logo/
└── main.py
```

## Gestión de usuarios

La parte de Usuarios solamente puede ser utilizada por el usuario que tiene el rol de `Administrador`.

Desde esta sección se puede:

- Registrar usuarios como `Empleado` o `Cliente`.
- Ver los usuarios que están registrados.
- Seleccionar un usuario desde la tabla.
- Cargar los datos del usuario seleccionado en el formulario.
- Actualizar los datos de un usuario.
- Eliminar un usuario con una confirmación.
- Limpiar el formulario.
- Evitar eliminar por accidente la cuenta del administrador que está usando el sistema.

En la tabla se muestran datos como la identificación, nombre, usuario, correo y rol. La contraseña no se muestra.

## Eventos que utilicé

En esta semana pude aplicar la diferencia entre usar `command=` y `bind()`.

### Botones con `command=`

Los botones principales de Usuarios utilizan `command=`:

- Registrar
- Actualizar
- Eliminar
- Limpiar

### Eventos con `bind()`

También utilicé algunos eventos para que la aplicación pueda responder a diferentes acciones:

- `<<TreeviewSelect>>`: cuando selecciono un usuario de la tabla, sus datos se cargan en el formulario.
- `<Return>`: permite registrar un usuario utilizando la tecla Enter.
- `<Escape>`: permite limpiar el formulario y quitar la selección.
- `<<ComboboxSelected>>`: detecta cuando cambio el rol en el `Combobox`.

El funcionamiento que seguí fue más o menos así:

```text
El usuario realiza una acción
        ↓
Se genera un evento
        ↓
bind()
        ↓
Se ejecuta el callback
        ↓
Se utiliza RestauranteServicio
        ↓
Se guardan los cambios en usuarios.json
        ↓
Se actualiza la interfaz
```

## Roles

En el proyecto utilicé tres tipos de roles:

- `Administrador`
- `Empleado`
- `Cliente`

La cuenta de administrador que ya tenía se mantiene para poder entrar a la gestión de usuarios.

Desde el formulario no se pueden crear nuevos usuarios con el rol de Administrador. Los nuevos usuarios solamente pueden ser `Empleado` o `Cliente`.

## Separación de las partes del proyecto

En este proyecto traté de mantener separadas las diferentes partes.

La interfaz se encarga principalmente de mostrar los datos y recibir las acciones del usuario.

`RestauranteServicio` se encarga de realizar las operaciones y validaciones de usuarios, productos y ventas.

`ArchivoServicio` se utiliza para leer y guardar la información de los archivos JSON.

De esta manera la interfaz no tiene que estar leyendo o escribiendo directamente los archivos JSON.

## Persistencia de usuarios

Los usuarios se guardan en:

```text
restaurante_app/datos/usuarios.json
```

Cuando registro, actualizo o elimino un usuario, los cambios se guardan nuevamente en este archivo.

Así, cuando cierro y vuelvo a abrir el programa, los usuarios que ya había registrado siguen apareciendo.

## Credenciales para probar el proyecto

| Usuario | Contraseña | Rol |
|---|---|---|
| `Milton` | `admin` | Administrador |
| `Sofia` | `sofia123` | Cliente |
| `Carlos` | `carlos123` | Cliente |
| `Valentina` | `vale123` | Cliente |
| `Diego` | `diego123` | Cliente |
| `Camila` | `camila123` | Cliente |
| `Andres` | `andres123` | Cliente |
| `Gabriela` | `gabi123` | Cliente |

Para probar la gestión de usuarios se puede ingresar con:

```text
Usuario: Milton
Contraseña: admin
```

Después de iniciar sesión se puede entrar a la sección de Usuarios y registrar un nuevo usuario como `Empleado` o `Cliente`.

## Cómo ejecutar el proyecto

Primero se debe abrir la carpeta `restaurante_app` en VS Code.

Después, desde la terminal se puede ejecutar:

```powershell
python main.py
```

También se puede utilizar la opción **Run Python File** de VS Code.

## Comprobaciones de la Semana 16

Para comprobar que las funciones de esta semana trabajan correctamente se puede hacer lo siguiente:

1. Iniciar la aplicación con `Milton / admin`.
2. Entrar a la sección `Usuarios`.
3. Registrar un usuario como `Cliente` o `Empleado`.
4. Revisar que aparezca en el `Treeview`.
5. Seleccionar una fila y comprobar que sus datos aparezcan en el formulario.
6. Cambiar algún dato y utilizar `Actualizar`.
7. Seleccionar un usuario y utilizar `Eliminar`.
8. Probar la tecla `Escape` para limpiar el formulario.
9. Probar la tecla `Enter` para registrar un usuario.
10. Cambiar el rol en el `Combobox`.
11. Cerrar y volver a abrir el programa para comprobar que los usuarios se mantengan guardados.
12. Comprobar que las partes de Productos y Ventas sigan funcionando.

## Lo que aprendí en esta semana

En esta semana pude entender un poco mejor cómo trabajar con eventos en Tkinter. Antes utilizaba principalmente los botones con `command=`, pero ahora también pude utilizar `bind()` para responder a eventos como seleccionar una fila, presionar Enter o Escape y cambiar una opción del `Combobox`.

También pude seguir practicando la separación entre la interfaz, los modelos y los servicios, para que no toda la lógica del programa quede dentro de la ventana.

## Nota

Este proyecto continúa con el trabajo que ya había realizado en las semanas anteriores. Para esta semana me enfoqué principalmente en mejorar la gestión de usuarios y en aplicar los eventos de Tkinter que se solicitaron en la actividad.
