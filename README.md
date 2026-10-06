# 🎮 GAMEZONE PRO

### `PHANTOM EDITION // BETA 1.0`

> **Your Battle. Your Rank. Your Legacy.**

GameZone Pro es un proyecto de gestión y visualización para torneos de videojuegos, desarrollado en **Python** con una interfaz gráfica inspirada en la estética visual de los menús de **Persona 5 Royal**.

Esta primera beta se centra exclusivamente en la **interfaz gráfica y experiencia visual** del sistema. La lógica, base de datos y funcionalidades principales serán implementadas en futuras versiones.

---

## 🟥 Estado del proyecto

**Versión actual:** `Beta 1.0`

**Estado:** 🟡 En desarrollo

| Componente | Estado |
|---|---|
| 🎨 Interfaz gráfica | ✅ Implementada |
| 🖥️ Ventana principal | ✅ Implementada |
| 🧭 Menú lateral | ✅ Implementado |
| 🏠 Dashboard | ✅ Implementado |
| 👥 Gestión de jugadores | 🟡 Diseño inicial |
| 🏆 Ranking | 🟡 Diseño inicial |
| ⚔️ Torneos | 🟡 Diseño inicial |
| 📊 Estadísticas | 🟡 Diseño inicial |
| 🗄️ Base de datos | ❌ Pendiente |
| ⚙️ Sistema de ranking ELO | ❌ Pendiente |
| 🎮 Gestión de partidas | ❌ Pendiente |
| 🔐 Sistema de usuarios | ❌ Pendiente |

---

# ✨ Características de esta Beta

### 🎨 Interfaz Phantom Edition

La interfaz utiliza una estética inspirada en el estilo visual de **Persona 5 Royal**, utilizando:

- 🟥 Rojo como color principal
- ⬛ Fondos negros y oscuros
- ⬜ Tipografía blanca de alto contraste
- 🔺 Elementos geométricos
- ⚡ Diseño agresivo y dinámico
- 🎭 Concepto visual `Phantom Edition`
- 📐 Composición asimétrica

El objetivo es evitar el aspecto tradicional de un panel administrativo y darle al sistema una identidad más cercana a una interfaz de videojuego.

---

## 🖥️ Dashboard

La pantalla principal actualmente contiene:

- **GAMEZONE PRO**
- Mensaje de bienvenida
- Estado del sistema
- Panel de jugadores
- Ranking
- Torneos activos
- Actividad reciente
- Menú de navegación
- Indicador de sistema online
- Identidad visual Phantom Edition

---

# 🧭 Menú principal

La interfaz cuenta actualmente con las siguientes secciones:

```text
┌──────────────────────────────┐
│      PHANTOM MENU            │
├──────────────────────────────┤
│ ▶ HOME                       │
│ ◆ PLAYERS                    │
│ ★ RANKING                    │
│ ▲ TOURNAMENTS                │
│ ● RESULTS                    │
│ ■ STATISTICS                 │
└──────────────────────────────┘
```

En esta beta los botones funcionan principalmente como **elementos visuales de navegación**. Las funciones asociadas serán desarrolladas posteriormente.

---

# 🛠️ Tecnologías utilizadas

## Python

Lenguaje principal utilizado para el desarrollo del proyecto.

## CustomTkinter

Framework utilizado para construir la interfaz gráfica moderna de GameZone Pro.

## Tkinter

Utilizado para elementos gráficos adicionales y composición del fondo.

---

# 📁 Estructura actual

La primera beta mantiene una arquitectura sencilla para facilitar el desarrollo inicial:

```text
Gamezone - Persona 3/
│
├── main.py
│
└── README.md
```

### `main.py`

Contiene actualmente:

- Configuración de la aplicación
- Ventana principal
- Tema visual
- Colores
- Sidebar
- Menú
- Dashboard
- Tarjetas informativas
- Elementos decorativos
- Footer
- Composición visual

La beta está diseñada deliberadamente como un **prototipo de interfaz en un solo archivo**.

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/GameZone-Pro.git
```

Entrar en la carpeta:

```bash
cd GameZone-Pro
```

---

## 2. Instalar dependencias

El proyecto requiere Python y CustomTkinter.

Instalar CustomTkinter:

```bash
pip install customtkinter
```

---

## 3. Ejecutar GameZone Pro

```bash
python main.py
```

También puede ejecutarse mediante:

```bash
py main.py
```

---

# 🖼️ Vista conceptual

La interfaz está diseñada alrededor de una identidad visual denominada:

```text
GAMEZONE PRO
       //
PHANTOM EDITION
```

La intención de esta primera beta es establecer primero la **identidad visual del sistema** antes de comenzar a implementar la lógica.

---

# 🗺️ Roadmap

## 🔴 Beta 1.0 — PHANTOM UI

**Estado: ACTUAL**

- [x] Crear ventana principal
- [x] Crear identidad GameZone Pro
- [x] Crear interfaz oscura
- [x] Implementar paleta rojo/negro/blanco
- [x] Crear Phantom Menu
- [x] Crear Dashboard
- [x] Crear tarjetas informativas
- [x] Crear indicadores del sistema

---

## 🟠 Beta 2.0 — SYSTEM CORE

**Planeado**

- [ ] Sistema de jugadores
- [ ] Registro de jugadores
- [ ] Edición de jugadores
- [ ] Eliminación de jugadores
- [ ] Sistema de torneos
- [ ] Registro de partidas
- [ ] Resultados

---

## 🟡 Beta 3.0 — RANKING SYSTEM

**Planeado**

- [ ] Sistema ELO
- [ ] Ranking global
- [ ] Historial de posiciones
- [ ] Historial ELO
- [ ] Estadísticas de jugadores
- [ ] Clasificación por torneo

---

## 🟢 Beta 4.0 — DATABASE

**Planeado**

- [ ] Implementar SQLite
- [ ] Crear tablas
- [ ] Conectar interfaz con la base de datos
- [ ] Persistencia de información
- [ ] Sistema de consultas

---

## 🔵 Release 1.0

**Objetivo final**

```text
GAMEZONE PRO
      │
      ├── PLAYERS
      │
      ├── RANKING
      │
      ├── TOURNAMENTS
      │
      ├── RESULTS
      │
      ├── STATISTICS
      │
      └── DATABASE
```

Convertir el prototipo visual en un sistema completo de gestión de torneos competitivos.

---

# 🎯 Objetivo del proyecto

GameZone Pro busca convertirse en una plataforma para administrar torneos de videojuegos y proporcionar una experiencia visual diferente a los sistemas tradicionales de gestión.

El proyecto combina:

**Software + videojuegos + competición + diseño UI**

con el objetivo de crear una aplicación que no solamente sea funcional, sino que también tenga una identidad visual propia.

---

# ⚠️ Estado actual

Esta versión es una **beta temprana**.

Actualmente:

- No existe una base de datos.
- No existe persistencia de información.
- No existe sistema ELO funcional.
- No existe autenticación.
- No existe gestión real de torneos.
- Los datos mostrados en pantalla son elementos de demostración.
- La navegación funcional será implementada posteriormente.

El objetivo de esta versión es validar y desarrollar la **interfaz visual de GameZone Pro**.

---

# 📌 Próximo objetivo

> **Transformar la Phantom Edition de un prototipo visual en un sistema completo de gestión competitiva.**

La siguiente etapa estará enfocada en comenzar a convertir los elementos visuales en componentes funcionales.

---

# 👨‍💻 Autor

**Giovanni Paolo Jaimes Jaime**

Estudiante de Desarrollo de Software.

### Proyecto académico / personal

**GameZone Pro — Phantom Edition**

---

# 📜 Licencia

Este proyecto se encuentra actualmente en desarrollo.

La licencia definitiva será definida en una versión posterior.

---

<div align="center">

### 🎮 GAMEZONE PRO

**PHANTOM EDITION**

`BETA 1.0`

> **YOUR BATTLE. YOUR RANK. YOUR LEGACY.**

</div>
