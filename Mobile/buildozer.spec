
[app]

# Información de GameZone Pro
title = GameZone Pro
package.name = gamezonepro
package.domain = com.gamezonepro

# Directorio del proyecto
source.dir = .

# Archivos que se incluirán
source.include_exts = py,kv,png,jpg,jpeg,webp,atlas,ttf,otf,json,txt,mp3,wav

# Carpetas excluidas
source.exclude_dirs = tests,bin,.git,.venv,__pycache__,.buildozer

# Versión
version = 1.1.0

# Dependencias
requirements = python3,kivy

# Pantalla
orientation = portrait
fullscreen = 0

# Permisos
android.permissions = INTERNET
android.add_uses_cleartexttraffic = True

# Android
android.api = 35
android.minapi = 24
android.archs = arm64-v8a

# Python for Android
p4a.branch = develop
p4a.bootstrap = sdl2

# Licencias
android.accept_sdk_license = True

# Registro
log_level = 2
warn_on_root = 1


[buildozer]

# Directorios de compilación
build_dir = ./.buildozer
bin_dir = ./bin
