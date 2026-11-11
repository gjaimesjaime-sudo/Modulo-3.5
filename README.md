# 🎮 GAMEZONE PRO
### Sistema de Gestión y Ranking para Torneos de Videojuegos

<p align="center">
  <strong>GAMEZONE PRO</strong><br>
  Plataforma móvil para la gestión de jugadores, torneos, mensajes y rankings competitivos.
</p>

---

## 📌 Descripción del proyecto

**GameZone Pro** es una aplicación móvil desarrollada en Python utilizando Kivy, diseñada para administrar y gestionar torneos de videojuegos, jugadores y sistemas de clasificación competitiva.

El sistema permite gestionar usuarios mediante roles, consultar rankings basados en puntos ELO, visualizar torneos, administrar jugadores y facilitar la comunicación entre los participantes.

El proyecto utiliza una arquitectura cliente-servidor, donde la aplicación móvil se comunica con una API REST que procesa las solicitudes y permite acceder a la información almacenada en MySQL.

## 🎯 Objetivos

- Desarrollar una plataforma móvil para la gestión de torneos de videojuegos.
- Implementar un sistema de clasificación competitiva mediante ELO.
- Administrar jugadores y usuarios con diferentes roles.
- Facilitar la comunicación entre los participantes.
- Integrar Python con MySQL mediante una API REST.
- Proporcionar una interfaz gráfica moderna e intuitiva.

## 🛠️ Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje principal |
| Kivy | Desarrollo de la aplicación móvil |
| MySQL | Gestión de base de datos |
| PHP | Desarrollo de la API REST actual |
| Requests / urllib | Comunicación HTTP |
| XAMPP | Servidor local |
| GitHub | Control de versiones |
| Buildozer | Generación de APK para Android |

## 📱 Características principales

### 🏠 Inicio
- Interfaz principal de GameZone Pro.
- Acceso a las diferentes secciones.
- Diseño inspirado en Persona 5 Royal.

### 💬 Mensajes
- Visualización de conversaciones.
- Organización de chats.
- Comunicación entre participantes.

### 🏆 Torneos
- Consulta de torneos disponibles.
- Visualización de información de competición.
- Gestión de torneos mediante funciones administrativas.

### 📊 Ranking
- Clasificación de jugadores.
- Visualización de puntos ELO.
- Estadísticas de victorias, derrotas y empates.
- Seguimiento del rendimiento competitivo.

### 👤 Jugadores
- Consulta de jugadores registrados.
- Visualización de información de participantes.
- Administración de jugadores.

### ⚙️ Perfil
- Información de la cuenta.
- Visualización de datos del usuario.
- Gestión de información personal.

### 🔐 Sistema de usuarios
- Inicio de sesión.
- Registro de usuarios.
- Roles de administrador y jugador.
- Control de permisos según el rol.

## 🗄️ Base de datos

El proyecto utiliza MySQL para almacenar la información de la plataforma.

**Nombre de la base de datos:**

`gamezonepro`

Entre las entidades del sistema se encuentran:

- Usuarios.
- Jugadores.
- Roles.
- Permisos.
- Torneos.
- Inscripciones.
- Mensajes.
- Ranking.
- Resultados.
- Historial ELO.

La estructura definitiva de tablas y relaciones se encuentra definida en el archivo SQL del proyecto.

## 🔌 Arquitectura del sistema

GameZone Pro utiliza una arquitectura cliente-servidor:

```text
          GAMEZONE PRO
                |
                v
       Aplicación móvil
          Python/Kivy
                |
                v
          Solicitudes HTTP
                |
                v
            API REST
             PHP
                |
                v
          MySQL Database
                |
                v
          gamezonepro
```

La aplicación móvil envía solicitudes HTTP a la API REST. El servidor procesa las peticiones, consulta o modifica los registros de MySQL y devuelve respuestas en formato JSON.

## 💻 Requisitos del sistema

- Python 3.10 o superior para el entorno de desarrollo.
- Kivy.
- MySQL.
- XAMPP.
- Git.
- Android para ejecutar la aplicación móvil compilada.

## ⚙️ Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/GameZone.git
```

### 2. Entrar al proyecto

```bash
cd GameZone
```

### 3. Crear el entorno virtual

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

Windows:

```bash
.venv\Scripts\activate
```

### 5. Instalar dependencias

```bash
pip install kivy requests
```

Instala también las dependencias adicionales indicadas por los archivos del proyecto.

### 6. Configurar XAMPP

1. Abrir XAMPP.
2. Iniciar Apache.
3. Iniciar MySQL.
4. Acceder a phpMyAdmin.
5. Importar el archivo SQL de GameZone Pro.
6. Comprobar que exista la base de datos `gamezonepro`.

### 7. Configurar la API

Colocar los archivos PHP dentro del directorio de publicación de Apache, por ejemplo:

```text
C:\xampp\htdocs\GameZone\api\
```

Configurar la conexión a MySQL en:

```text
api/config/conexion.php
```

### 8. Configurar la dirección de conexión

La aplicación móvil debe utilizar la dirección IP local del equipo donde se ejecuta XAMPP cuando se prueba desde un teléfono conectado a la misma red Wi-Fi.

Ejemplo:

```text
http://192.168.1.100/GameZone/api/
```

La dirección es ilustrativa y debe reemplazarse por la IP real del equipo.

### 9. Ejecutar la aplicación

```bash
python main.py
```

## 📂 Estructura general del proyecto

```text
GameZone/
│
├── mobile/
│   ├── main.py
│   ├── buildozer.spec
│   ├── IMG/
│   │   └── Logo.jpg
│   └── Assets/
│
├── api/
│   ├── config/
│   │   └── conexion.php
│   ├── usuarios/
│   ├── jugadores/
│   ├── torneos/
│   ├── mensajes/
│   └── ranking/
│
├── database/
│   └── gamezonepro.sql
│
├── README.md
└── .gitignore
```

*La estructura representa la organización general prevista; los nombres y directorios deben coincidir con los existentes en el repositorio.*

## 🏅 Sistema de clasificación ELO

GameZone Pro incorpora un sistema de puntuación ELO para representar el nivel competitivo de los jugadores.

El sistema permite:

- Calcular cambios en los puntos ELO.
- Actualizar la clasificación.
- Registrar resultados de partidas.
- Consultar estadísticas competitivas.

El valor K utilizado en el planteamiento original del sistema es **30**.

## 🔒 Seguridad

El proyecto contempla:

- Autenticación de usuarios.
- Separación de permisos mediante roles.
- Validación de solicitudes.
- Protección de credenciales de conexión.
- Comunicación entre cliente y servidor mediante API REST.

No se deben publicar contraseñas, tokens ni credenciales de MySQL en el repositorio.

## 🚀 Compilación para Android

GameZone Pro utiliza Buildozer para generar su aplicación Android.

La configuración se encuentra en:

```text
mobile/buildozer.spec
```

El proyecto también contempla la automatización de compilaciones mediante GitHub Actions.

El resultado esperado es un archivo APK instalable en dispositivos Android.

## 👨‍💻 Autor

**Giovanni Paolo Jaimes Jaime**

Proyecto académico desarrollado para el área de Desarrollo de Software.

## 📚 Propósito académico

GameZone Pro forma parte de un proyecto de desarrollo de software orientado a la aplicación de conocimientos sobre:

- Desarrollo de aplicaciones móviles.
- Programación en Python.
- Bases de datos relacionales.
- Desarrollo de API REST.
- Comunicación cliente-servidor.
- Administración de usuarios y permisos.
- Control de versiones.

---

<p align="center">
  🎮 <strong>GAMEZONE PRO</strong><br>
  <em>Play. Compete. Rise.</em>
</p>
