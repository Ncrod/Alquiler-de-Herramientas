Hola primer commit
# Alquiler de Herramientas

Sistema de consola en Python para gestionar el préstamo de herramientas dentro de una organización. Permite administrar el inventario de herramientas, los usuarios del sistema, las solicitudes de préstamo y los préstamos activos, además de generar reportes de uso. Toda la información se guarda en archivos JSON y cada acción relevante queda registrada en un log de eventos.

> Este es un proyecto académico, desarrollado con fines de aprendizaje en programación con Python. No está pensado para uso en producción.

## Características

- Gestión de herramientas: crear, listar, buscar, actualizar, inactivar o eliminar.
- Gestión de usuarios con dos roles: Administrador y Usuario.
- Sistema de solicitudes: el usuario solicita una herramienta y el administrador la aprueba o rechaza.
- Registro y devolución de préstamos, con control automático de stock y fecha límite de devolución.
- Detección de préstamos vencidos.
- Reportes: stock bajo, préstamos activos y vencidos, historial por usuario, herramientas más solicitadas y usuarios más activos.
- Registro de eventos (info, advertencia, error) en un archivo de log con fecha y hora.
- Persistencia de datos en archivos JSON, sin necesidad de una base de datos externa.

## Estructura del proyecto

```
Alquiler-de-Herramientas/
├── main.py                  # Punto de entrada, menús y flujo principal
├── config.py                 # Rutas de archivos y constantes del sistema
├── modulos/
│   ├── almacenamiento.py     # Lectura y escritura genérica de archivos JSON
│   ├── herramientas.py       # CRUD de herramientas
│   ├── usuarios.py           # CRUD de usuarios
│   ├── permisos.py           # Inicio de sesión, roles y solicitudes
│   ├── prestamos.py          # Registro y devolución de préstamos
│   ├── reportes.py           # Generación de reportes
│   ├── logs.py                # Registro de eventos en archivo de log
│   └── utilidades.py         # Funciones auxiliares (entrada de datos, validaciones)
├── data/
│   ├── herramientas.json
│   ├── usuarios.json
│   ├── prestamos.json
│   └── solicitudes.json
└── logs/
    └── eventos.log
```

## Requisitos

- Python 3.10 o superior (no requiere librerías externas, solo módulos estándar).

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/Ncrod/Alquiler-de-Herramientas.git
   cd Alquiler-de-Herramientas
   ```
2. Verificar que las carpetas `data/` y `logs/` existan (se crean automáticamente si no existen al guardar información).

## Uso

Ejecutar el programa desde la raíz del proyecto:

```
python main.py
```

Si es la primera vez que se ejecuta y no hay usuarios registrados, el sistema pedirá crear un administrador inicial con id 1.

Después de iniciar sesión con el id de usuario, el sistema muestra un menú distinto según el rol:

**Menú Administrador**
1. Herramientas (crear, listar, buscar, actualizar, eliminar o inactivar)
2. Usuarios (crear, listar, buscar, actualizar, eliminar)
3. Préstamos (registrar, devolver, listar todos, aprobar o rechazar solicitudes pendientes)
4. Reportes (stock bajo, préstamos activos y vencidos, historial por usuario, herramientas más solicitadas, usuarios más activos)

**Menú Usuario**
1. Ver herramientas disponibles
2. Buscar herramienta
3. Solicitar una herramienta
4. Ver mis solicitudes
5. Ver mi historial de préstamos

## Datos

La información se guarda en archivos JSON dentro de la carpeta `data/`:

- `herramientas.json`: id, nombre, categoría, cantidad disponible, estado y valor estimado de cada herramienta.
- `usuarios.json`: id, nombres, apellidos, teléfono, dirección y tipo de usuario (Administrador o Usuario).
- `prestamos.json`: id, usuario, herramienta, cantidad, fecha de inicio, fecha estimada de devolución, fecha real de devolución, estado y observaciones.
- `solicitudes.json`: id, usuario, herramienta, cantidad, fecha y estado de la solicitud (Pendiente, Aprobada o Rechazada).

Cada evento importante del sistema (inicio de sesión, creación de registros, préstamos, errores, etc.) se registra en `logs/eventos.log` con fecha, hora, tipo de evento y usuario relacionado.

## Autores

- Nicolás Rodríguez
- Oliver Estivemsom Moreno Patiño
