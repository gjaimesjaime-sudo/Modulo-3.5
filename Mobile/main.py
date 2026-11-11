

from datetime import datetime
import json
import threading
import urllib.request
import urllib.error

from pathlib import Path



from kivy.app import App

from kivy.clock import Clock

from kivy.animation import Animation

from kivy.core.window import Window

from kivy.metrics import dp, sp

from kivy.properties import NumericProperty

from kivy.graphics import Color, Rectangle, Line

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout

from kivy.uix.gridlayout import GridLayout

from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.label import Label

from kivy.uix.button import Button

from kivy.uix.widget import Widget

from kivy.uix.scrollview import ScrollView

from kivy.uix.textinput import TextInput

from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
# =========================================================# GAMEZONE PRO MOBILE# =========================================================
ROJO = (0.96, 0.035, 0.12, 1)

ROJO_OSCURO = (0.43, 0.015, 0.055, 1)

ROJO_BRILLO = (1.0, 0.16, 0.23, 1)



NEGRO = (0.035, 0.035, 0.045, 1)

PANEL = (0.085, 0.085, 0.105, 1)

PANEL_CLARO = (0.13, 0.13, 0.16, 1)



BLANCO = (0.97, 0.96, 0.95, 1)

GRIS = (0.68, 0.69, 0.73, 1)

GRIS_OSCURO = (0.17, 0.17, 0.20, 1)

VERDE = (0.35, 0.88, 0.58, 1)

# =========================================================
# CONEXIÓN CON LA API PHP DE GAMEZONE PRO
# En Windows: localhost funciona con XAMPP.
# En Android: reemplaza localhost por la IP LAN de tu PC.
# =========================================================
API_BASE_URL = "http://192.168.1.19/gamezone_pro/api"
API_LOGIN_URL = f"{API_BASE_URL}/usuarios/iniciar_sesion.php"
API_RANKING_URL = f"{API_BASE_URL}/ranking/listar.php"
API_JUGADORES_URL = f"{API_BASE_URL}/jugadores/listar.php"
API_TIMEOUT = 15


def solicitud_api(url, metodo="GET", datos=None, token=None):
    encabezados = {"Accept": "application/json"}
    cuerpo = None
    if datos is not None:
        encabezados["Content-Type"] = "application/json; charset=UTF-8"
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
    if token:
        encabezados["Authorization"] = f"Bearer {token}"
    solicitud = urllib.request.Request(
        url, data=cuerpo, headers=encabezados, method=metodo
    )
    try:
        with urllib.request.urlopen(solicitud, timeout=API_TIMEOUT) as respuesta:
            contenido = respuesta.read().decode("utf-8")
            return json.loads(contenido) if contenido else {}
    except urllib.error.HTTPError as error:
        contenido = error.read().decode("utf-8", errors="replace")
        try:
            resultado = json.loads(contenido)
        except (json.JSONDecodeError, TypeError):
            resultado = {"success": False, "mensaje": f"Error HTTP {error.code}"}
        resultado.setdefault("success", False)
        resultado["http_code"] = error.code
        return resultado
    except urllib.error.URLError as error:
        raise ConnectionError(
            "No se pudo conectar con la API. Comprueba XAMPP, la URL y la red. "
            f"Detalle: {getattr(error, 'reason', error)}"
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError("La API devolvió una respuesta que no es JSON válido.") from error
# =========================================================# CONFIGURACIÓN DE IMÁGENES# =========================================================
CONFIG_IMAGENES_LISTADO = {

    "alto_tarjeta": dp(95),

    "espaciado": dp(7),

    "padding_horizontal": dp(4),

    "padding_vertical": dp(6),

    "fit_mode": "cover",

}



BASE_DIR = Path(__file__).resolve().parent





def buscar_imagen_opcion(numero):



    nombre = f"Options{numero}.png"



    candidatas = [

        BASE_DIR / "assets" / "Background" / nombre,

        BASE_DIR / "Assets" / "Background" / nombre,

        BASE_DIR / "assets" / "background" / nombre,

        BASE_DIR / "Background" / nombre,

        BASE_DIR.parent / "assets" / "Background" / nombre,

        BASE_DIR.parent / "Assets" / "Background" / nombre,

    ]



    encontrada = next(

        (ruta for ruta in candidatas if ruta.is_file()),

        None

    )



    if encontrada is None:



        for carpeta in (

            BASE_DIR / "assets",

            BASE_DIR.parent / "assets",

            BASE_DIR

        ):



            if carpeta.is_dir():



                encontrada = next(

                    carpeta.rglob(nombre),

                    None

                )



                if encontrada is not None and encontrada.is_file():

                    break



    return encontrada





RUTAS_IMAGENES_OPCIONES = {

    numero: buscar_imagen_opcion(numero)

    for numero in range(1, 6)

}



Window.clearcolor = NEGRO
# =========================================================# COMPONENTES REUTILIZABLES# =========================================================
class Panel(BoxLayout):



    def __init__(self, color=PANEL, **kwargs):



        super().__init__(**kwargs)



        self.color_panel = color



        with self.canvas.before:



            Color(*self.color_panel)



            self.bg_rect = Rectangle(

                pos=self.pos,

                size=self.size

            )



            Color(*ROJO)



            self.acento = Rectangle(

                pos=self.pos,

                size=(self.width, dp(2))

            )



        self.bind(

            pos=self.actualizar_bg,

            size=self.actualizar_bg

        )



    def actualizar_bg(self, *_):



        self.bg_rect.pos = self.pos

        self.bg_rect.size = self.size



        self.acento.pos = (

            self.x,

            self.top - dp(2)

        )



        self.acento.size = (

            self.width,

            dp(2)

        )





class Texto(Label):



    def __init__(

        self,

        text="",

        color=BLANCO,

        size=15,

        bold=False,

        **kwargs

    ):



        halign = kwargs.pop("halign", "left")

        valign = kwargs.pop("valign", "middle")

        markup = kwargs.pop("markup", False)



        super().__init__(**kwargs)



        self.text = text

        self.color = color

        self.font_size = sp(size)

        self.bold = bold

        self.halign = halign

        self.valign = valign

        self.markup = markup



        self.bind(size=self.actualizar_texto)



    def actualizar_texto(self, *_):



        self.text_size = (

            self.width,

            self.height

        )





def crear_boton(

    texto,

    callback=None,

    color=ROJO,

    alto=42,

    font_size=12

):



    boton = Button(

        text=texto,

        size_hint_y=None,

        height=dp(alto),

        font_size=sp(font_size),

        bold=True,

        color=BLANCO,

        background_normal="",

        background_down="",

        background_color=color

    )



    if callback:

        boton.bind(on_release=callback)



    return boton





def crear_scroll_lista(espaciado=8, padding=None):



    scroll = ScrollView(

        do_scroll_x=False,

        bar_width=dp(3)

    )



    lista = GridLayout(

        cols=1,

        spacing=dp(espaciado),

        padding=padding or [dp(2), dp(3)],

        size_hint_y=None

    )



    lista.bind(

        minimum_height=lista.setter("height")

    )



    scroll.add_widget(lista)



    return scroll, lista
# =========================================================# TARJETAS DEL MENÚ# =========================================================
class TarjetaP5(FloatLayout):



    def __init__(

        self,

        icono,

        titulo,

        subtitulo,

        estado,

        callback=None,

        **kwargs

    ):



        super().__init__(**kwargs)



        self.size_hint_y = None

        self.height = dp(112)



        self.callback = callback



        with self.canvas.before:



            Color(*ROJO_OSCURO)



            self.sombra = Rectangle(

                pos=self.pos,

                size=self.size

            )



        self.bind(

            pos=self.actualizar_sombra,

            size=self.actualizar_sombra

        )



        self.inner = FloatLayout(

            size_hint=(0.97, 0.90),

            pos_hint={

                "center_x": 0.485,

                "center_y": 0.53

            }

        )



        with self.inner.canvas.before:



            Color(*BLANCO)



            self.rect_borde = Rectangle(

                pos=self.inner.pos,

                size=self.inner.size

            )



            Color(0.015, 0.015, 0.02, 1)



            self.rect_fondo = Rectangle(

                pos=self.inner.pos,

                size=self.inner.size

            )



            Color(*ROJO)



            self.fr_item = Rectangle(

                pos=self.inner.pos,

                size=(dp(45), dp(4))

            )



        self.inner.bind(

            pos=self.actualizar_tarjeta,

            size=self.actualizar_tarjeta

        )



        avatar = FloatLayout(

            size_hint=(None, 0.70),

            width=dp(54),

            pos_hint={

                "x": 0.025,

                "center_y": 0.49

            }

        )



        with avatar.canvas.before:



            Color(0.015, 0.015, 0.02, 1)



            self.avatar_borde = Rectangle(

                pos=avatar.pos,

                size=avatar.size

            )



            Color(*ROJO)



            self.avatar_bg = Rectangle(

                pos=avatar.pos,

                size=avatar.size

            )



        avatar.bind(

            pos=self.actualizar_avatar,

            size=self.actualizar_avatar

        )



        avatar.add_widget(

            Label(

                text=icono,

                bold=True,

                font_size=sp(21),

                color=BLANCO

            )

        )



        self.inner.add_widget(avatar)



        text_box = BoxLayout(

            orientation="vertical",

            spacing=dp(1),

            size_hint=(0.66, 0.84),

            pos_hint={

                "x": 0.255,

                "center_y": 0.48

            }

        )



        text_box.add_widget(

            Texto(

                text=titulo,

                color=BLANCO,

                size=14,

                bold=True,

                size_hint_y=0.38

            )

        )



        text_box.add_widget(

            Texto(

                text=subtitulo,

                color=GRIS,

                size=10,

                size_hint_y=0.34

            )

        )



        text_box.add_widget(

            Texto(

                text=f"◆  {estado}",

                color=ROJO,

                size=9,

                bold=True,

                size_hint_y=0.28

            )

        )



        self.inner.add_widget(text_box)



        self.inner.add_widget(

            Label(

                text="///",

                color=ROJO,

                bold=True,

                font_size=sp(14),

                size_hint=(None, None),

                size=(dp(35), dp(22)),

                pos_hint={

                    "right": 0.99,

                    "top": 0.98

                }

            )

        )



        linea = Widget(

            size_hint=(None, None),

            size=(dp(4), dp(23)),

            pos_hint={

                "right": 0.985,

                "center_y": 0.34

            }

        )



        with linea.canvas.before:



            Color(*ROJO)



            linea.rect = Rectangle(

                pos=linea.pos,

                size=linea.size

            )



        linea.bind(

            pos=lambda obj, value: setattr(

                obj.rect, "pos", value

            ),

            size=lambda obj, value: setattr(

                obj.rect, "size", value

            )

        )



        self.inner.add_widget(linea)



        self.add_widget(self.inner)



        self.btn_click = Button(

            text="",

            size_hint=(1, 1),

            pos_hint={"x": 0, "y": 0},

            background_normal="",

            background_down="",

            background_color=(0, 0, 0, 0)

        )



        if callback:

            self.btn_click.bind(

                on_release=self.ejecutar_callback

            )



        self.add_widget(self.btn_click)



    def actualizar_sombra(self, *_):



        self.sombra.pos = (

            self.x + dp(5),

            self.y - dp(4)

        )



        self.sombra.size = self.size



    def actualizar_tarjeta(self, instancia, *_):



        self.rect_borde.pos = (

            instancia.x - dp(2),

            instancia.y - dp(2)

        )



        self.rect_borde.size = (

            instancia.width + dp(4),

            instancia.height + dp(4)

        )



        self.rect_fondo.pos = instancia.pos

        self.rect_fondo.size = instancia.size



        self.fr_item.pos = (

            instancia.x + dp(3),

            instancia.top - dp(7)

        )



        self.fr_item.size = (

            max(dp(20), instancia.width * 0.45),

            dp(4)

        )



    def actualizar_avatar(self, instancia, *_):



        self.avatar_borde.pos = instancia.pos

        self.avatar_borde.size = instancia.size



        self.avatar_bg.pos = (

            instancia.x + dp(3),

            instancia.y + dp(3)

        )



        self.avatar_bg.size = (

            max(0, instancia.width - dp(6)),

            max(0, instancia.height - dp(6))

        )



    def ejecutar_callback(self, *_):



        if self.callback:

            self.callback()
# =========================================================# BASE Y NAVEGACIÓN# =========================================================
class BaseScreen(Screen):



    def __init__(self, titulo, **kwargs):



        super().__init__(**kwargs)



        self.titulo = titulo



        self.raiz = BoxLayout(

            orientation="vertical",

            spacing=0

        )



        with self.canvas.before:



            Color(*NEGRO)



            self.fondo = Rectangle(

                pos=self.pos,

                size=self.size

            )



        self.bind(

            pos=self.actualizar_fondo,

            size=self.actualizar_fondo

        )



        self.add_widget(self.raiz)



    def actualizar_fondo(self, *_):



        self.fondo.pos = self.pos

        self.fondo.size = self.size



    def construir_encabezado(self):



        header = Panel(

            color=NEGRO,

            orientation="vertical",

            padding=[dp(20), dp(8)],

            spacing=dp(1),

            size_hint_y=None,

            height=dp(82)

        )



        header.add_widget(

            Texto(

                text="[b]/// GAMEZONE [color=F52640]PRO[/color]  ◆[/b]",

                markup=True,

                size=13,

                color=BLANCO

            )

        )



        header.add_widget(

            Texto(

                text=f"◢  {self.titulo.upper()}  ◤",

                size=23,

                color=BLANCO,

                bold=True

            )

        )



        return header



    def crear_navegacion(self):



        nav = Panel(

            color=(0.055, 0.055, 0.07, 1),

            orientation="horizontal",

            size_hint_y=None,

            height=dp(64),

            padding=[dp(7), dp(5)],

            spacing=dp(5)

        )



        opciones = [

            ("INI", "INICIO", "inicio"),

            ("MSG", "MENSAJES", "mensajes"),

            ("RNK", "RANKING", "ranking"),

            ("PRF", "PERFIL", "perfil")

        ]



        for icono, nombre, destino in opciones:



            columna = BoxLayout(

                orientation="vertical",

                spacing=dp(1)

            )



            activo = (

                self.manager is not None

                and self.manager.current == destino

            )



            color = ROJO_BRILLO if activo else GRIS



            boton = Button(

                text=icono,

                font_size=sp(14),

                color=color,

                background_normal="",

                background_down="",

                background_color=(

                    (0.20, 0.045, 0.065, 1)

                    if activo else (0, 0, 0, 0)

                ),

                size_hint_y=0.66

            )



            boton.bind(

                on_release=lambda _, d=destino: self.ir_a(d)

            )



            columna.add_widget(boton)



            columna.add_widget(

                Texto(

                    text=nombre,

                    color=color,

                    size=8,

                    bold=activo,

                    halign="center",

                    size_hint_y=0.34

                )

            )



            nav.add_widget(columna)



        return nav



    def ir_a(self, destino):



        if self.manager and destino in self.manager.screen_names:



            if destino == self.manager.current:

                return



            self.manager.transition = SlideTransition(

                direction="left",

                duration=0.24

            )



            self.manager.current = destino



    def preparar(self, contenido):



        self.raiz.clear_widgets()



        self.raiz.add_widget(

            self.construir_encabezado()

        )



        self.raiz.add_widget(contenido)



        self.raiz.add_widget(

            self.crear_navegacion()

        )
# =========================================================# TARJETAS ANIMADAS DE INICIO# =========================================================
class TarjetaInicio(FloatLayout):



    intensidad_sombra = NumericProperty(0)



    def __init__(self, **kwargs):



        super().__init__(**kwargs)



        self.size_hint = (None, None)



        self.width = min(

            Window.width - dp(36),

            dp(440)

        )



        self.height = CONFIG_IMAGENES_LISTADO["alto_tarjeta"]



        self.intensidad_sombra = 0



        with self.canvas.before:



            self.color_sombra = Color(

                0.96, 0.035, 0.12, 0

            )



            self.rect_sombra = Rectangle(

                pos=self.pos,

                size=self.size

            )



            self.color_brillo = Color(

                1, 0.08, 0.16, 0

            )



            self.rect_brillo = Rectangle(

                pos=self.pos,

                size=self.size

            )



            self.color_linea = Color(

                1, 0.16, 0.23, 0

            )



            self.linea_seleccion = Rectangle(

                pos=self.pos,

                size=(self.width, dp(3))

            )



        self.bind(

            pos=self.actualizar_efectos,

            size=self.actualizar_efectos,

            intensidad_sombra=self.actualizar_efectos

        )



    def actualizar_efectos(self, *_):



        intensidad = self.intensidad_sombra



        self.rect_sombra.pos = (

            self.x + dp(3),

            self.y - dp(3)

        )



        self.rect_sombra.size = self.size



        self.color_sombra.rgba = (

            0.96,

            0.035,

            0.12,

            0.12 + intensidad * 0.65

        )



        self.rect_brillo.pos = (

            self.x - dp(2),

            self.y - dp(2)

        )



        self.rect_brillo.size = (

            self.width + dp(4),

            self.height + dp(4)

        )



        self.color_brillo.rgba = (

            1,

            0.08,

            0.16,

            intensidad * 0.30

        )



        self.linea_seleccion.pos = (

            self.x + dp(8),

            self.y - dp(2)

        )



        self.linea_seleccion.size = (

            max(0, self.width - dp(16)),

            dp(3)

        )



        self.color_linea.rgba = (

            1,

            0.16,

            0.23,

            intensidad

        )
# =========================================================# INICIO SCREEN# =========================================================
class InicioScreen(BaseScreen):



    def __init__(self, **kwargs):



        super().__init__("Inicio", **kwargs)



        self.tarjetas_inicio = []

        self.destinos_inicio = []

        self.indice_seleccionado = -1

        self.animaciones_flotantes = []

        self.actualizacion_programada = None



        contenido = FloatLayout()



        with contenido.canvas.before:



            Color(*ROJO_OSCURO)



            self.bg_rojo = Rectangle(

                pos=contenido.pos,

                size=contenido.size

            )



        contenido.bind(

            pos=lambda obj, value: setattr(

                self.bg_rojo, "pos", value

            ),

            size=lambda obj, value: setattr(

                self.bg_rojo, "size", value

            )

        )



        layout = BoxLayout(

            orientation="vertical",

            padding=[dp(10), dp(6)],

            spacing=dp(4)

        )
# BARRA SUPERIOR
        top_bar = BoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=dp(30),

            padding=[dp(5), 0]

        )



        top_bar.add_widget(

            Texto(

                text="MENÚ PRINCIPAL",

                color=BLANCO,

                size=14,

                bold=True

            )

        )



        top_bar.add_widget(

            Texto(

                text="05 OPCIONES",

                color=BLANCO,

                size=10,

                bold=True,

                halign="right"

            )

        )



        layout.add_widget(top_bar)
# SCROLL
        self.scroll_inicio = ScrollView(

            do_scroll_x=False,

            bar_width=dp(3),

            scroll_type=["bars", "content"],

            effect_cls="ScrollEffect"

        )



        self.lista_inicio = GridLayout(

            cols=1,

            spacing=CONFIG_IMAGENES_LISTADO["espaciado"],

            padding=[

                CONFIG_IMAGENES_LISTADO["padding_horizontal"],

                CONFIG_IMAGENES_LISTADO["padding_vertical"],

                CONFIG_IMAGENES_LISTADO["padding_horizontal"],

                dp(12)

            ],

            size_hint_y=None

        )



        self.lista_inicio.bind(

            minimum_height=self.lista_inicio.setter("height")

        )
# OPCIONES
        opciones = [

            (

                "✉",

                "MENSAJES",

                "Consulta tus conversaciones y avisos",

                "NUEVOS AVISOS",

                "mensajes"

            ),

            (

                "VS",

                "TORNEOS",

                "Inscríbete y participa en eventos activos",

                "DISPONIBLE",

                "torneos"

            ),

            (

                "★",

                "RANKING",

                "Consulta la tabla de clasificación ELO",

                "ACTUALIZADO",

                "ranking"

            ),

            (

                "♟",

                "JUGADORES",

                "Encuentra rivales y compañeros de equipo",

                "EN LÍNEA",

                "jugadores"

            ),

            (

                "●",

                "PERFIL",

                "Revisa tus estadísticas y logros",

                "MI CUENTA",

                "perfil"

            )

        ]



        for indice, datos in enumerate(opciones):



            icono, titulo, subtitulo, estado, destino = datos



            contenedor = AnchorLayout(

                size_hint=(1, None),

                height=CONFIG_IMAGENES_LISTADO["alto_tarjeta"],

                anchor_x="center",

                anchor_y="center"

            )



            tarjeta = TarjetaInicio()



            tarjeta.width = min(

                Window.width - dp(36),

                dp(440)

            )



            ruta_imagen = RUTAS_IMAGENES_OPCIONES.get(

                indice + 1

            )



            if ruta_imagen is not None and ruta_imagen.is_file():



                imagen = Image(

                    source=str(ruta_imagen),

                    fit_mode=CONFIG_IMAGENES_LISTADO["fit_mode"],

                    size_hint=(1, 1),

                    pos_hint={"x": 0, "y": 0}

                )



                tarjeta.add_widget(imagen)



            else:



                tarjeta.add_widget(

                    Texto(

                        text=f"Imagen Options{indice + 1}.png no encontrada",

                        color=BLANCO,

                        size=11,

                        bold=True,

                        size_hint=(0.95, 0.3),

                        pos_hint={

                            "x": 0.025,

                            "center_y": 0.5

                        }

                    )

                )
# TEXTO SOBRE LA IMAGEN
            texto_sobre_imagen = BoxLayout(

                orientation="vertical",

                spacing=dp(1),

                padding=[dp(3), dp(1)],

                size_hint=(0.44, 0.76),

                pos_hint={

                    "x": 0.52,

                    "center_y": 0.46

                }

            )



            texto_sobre_imagen.add_widget(

                Texto(

                    text=titulo,

                    color=BLANCO,

                    size=12,

                    bold=True,

                    size_hint_y=0.38

                )

            )



            texto_sobre_imagen.add_widget(

                Texto(

                    text=subtitulo,

                    color=BLANCO,

                    size=8,

                    size_hint_y=0.36

                )

            )



            texto_sobre_imagen.add_widget(

                Texto(

                    text=f"◆ {estado}",

                    color=ROJO_BRILLO,

                    size=8,

                    bold=True,

                    size_hint_y=0.26

                )

            )



            tarjeta.add_widget(texto_sobre_imagen)
# BOTÓN TRANSPARENTE
            boton = Button(

                text="",

                size_hint=(1, 1),

                pos_hint={"x": 0, "y": 0},

                background_normal="",

                background_down="",

                background_color=(0, 0, 0, 0)

            )



            boton.bind(

                on_release=lambda _btn, t=tarjeta, d=destino:

                self.seleccionar_opcion(t, d)

            )



            tarjeta.add_widget(boton)



            contenedor.add_widget(tarjeta)



            self.lista_inicio.add_widget(contenedor)



            self.tarjetas_inicio.append(tarjeta)

            self.destinos_inicio.append(destino)



        self.scroll_inicio.add_widget(self.lista_inicio)



        layout.add_widget(self.scroll_inicio)



        contenido.add_widget(layout)
# NAVEGACIÓN INFERIOR
        self.raiz.clear_widgets()



        self.raiz.add_widget(contenido)



        self.raiz.add_widget(

            self.crear_navegacion()

        )
# EVENTOS DEL SCROLL
        self.scroll_inicio.bind(

            scroll_y=self.programar_actualizacion_seleccion,

            pos=self.programar_actualizacion_seleccion,

            size=self.programar_actualizacion_seleccion

        )



        self.lista_inicio.bind(

            size=self.programar_actualizacion_seleccion,

            pos=self.programar_actualizacion_seleccion

        )
# ENTRADA A INICIO
    def on_enter(self, *_):



        Clock.schedule_once(

            self.animar_tarjetas_inicio,

            0.12

        )



        Clock.schedule_once(

            self.programar_actualizacion_seleccion,

            0.65

        )
# ANIMACIÓN DE ENTRADA
    def animar_tarjetas_inicio(self, *_):



        for indice, tarjeta in enumerate(self.tarjetas_inicio):



            Animation.cancel_all(tarjeta)



            tarjeta.opacity = 0



            ancho = min(

                Window.width - dp(36),

                dp(440)

            )



            tarjeta.width = max(

                dp(220),

                ancho - dp(12)

            )



            tarjeta.intensidad_sombra = 0



            animacion = Animation(

                opacity=1,

                width=ancho,

                duration=0.32,

                t="out_cubic"

            )



            Clock.schedule_once(

                lambda _dt, widget=tarjeta, anim=animacion:

                anim.start(widget),

                indice * 0.09

            )



        Clock.schedule_once(

            self.programar_actualizacion_seleccion,

            0.85

        )
# MOVIMIENTO FLOTANTE
    def iniciar_flotacion(self, tarjeta):



        if tarjeta == self.tarjeta_seleccionada():

            return



        Animation.cancel_all(tarjeta, "width")



        ancho = min(

            Window.width - dp(36),

            dp(440)

        )



        animacion = (

            Animation(

                width=ancho + dp(3),

                duration=0.85,

                t="in_out_sine"

            )

            +

            Animation(

                width=ancho,

                duration=0.85,

                t="in_out_sine"

            )

        )



        animacion.repeat = True

        animacion.start(tarjeta)



        self.animaciones_flotantes.append(

            (tarjeta, animacion)

        )



    def detener_flotacion(self, tarjeta):



        Animation.cancel_all(tarjeta, "width")



    def iniciar_animaciones_secundarias(self, *_):



        for indice, tarjeta in enumerate(self.tarjetas_inicio):



            if indice != self.indice_seleccionado:



                Clock.schedule_once(

                    lambda _dt, t=tarjeta:

                    self.iniciar_flotacion(t),

                    indice * 0.10

                )



    def tarjeta_seleccionada(self):



        if 0 <= self.indice_seleccionado < len(self.tarjetas_inicio):



            return self.tarjetas_inicio[

                self.indice_seleccionado

            ]



        return None
# DETECCIÓN AUTOMÁTICA DEL SCROLL
    def programar_actualizacion_seleccion(self, *_):



        if self.actualizacion_programada is not None:



            self.actualizacion_programada.cancel()



        self.actualizacion_programada = Clock.schedule_once(

            self.actualizar_seleccion_scroll,

            0.06

        )



    def actualizar_seleccion_scroll(self, *_):



        self.actualizacion_programada = None



        if not self.tarjetas_inicio:

            return



        scroll = self.scroll_inicio



        centro_scroll = scroll.to_window(

            scroll.width / 2,

            scroll.height / 2

        )[1]



        esquina_inferior = scroll.to_window(0, 0)



        esquina_superior = scroll.to_window(

            scroll.width,

            scroll.height

        )



        limite_inferior = esquina_inferior[1]

        limite_superior = esquina_superior[1]



        mejor_indice = -1

        menor_distancia = float("inf")



        for indice, tarjeta in enumerate(self.tarjetas_inicio):



            centro_tarjeta = tarjeta.to_window(

                tarjeta.width / 2,

                tarjeta.height / 2

            )[1]



            inferior = tarjeta.to_window(0, 0)[1]



            superior = tarjeta.to_window(

                0,

                tarjeta.height

            )[1]



            visible = (

                superior > limite_inferior

                and inferior < limite_superior

            )



            if not visible:

                continue



            distancia = abs(

                centro_tarjeta - centro_scroll

            )



            if distancia < menor_distancia:



                menor_distancia = distancia

                mejor_indice = indice



        if mejor_indice >= 0:



            self.cambiar_seleccion(mejor_indice)
# CAMBIAR TARJETA SELECCIONADA
    def cambiar_seleccion(self, nuevo_indice):



        if nuevo_indice == self.indice_seleccionado:

            return



        anterior = self.indice_seleccionado



        self.indice_seleccionado = nuevo_indice



        if anterior >= 0:



            tarjeta_anterior = self.tarjetas_inicio[anterior]



            Animation.cancel_all(

                tarjeta_anterior,

                "intensidad_sombra"

            )



            animacion_salida = Animation(

                intensidad_sombra=0,

                duration=0.20,

                t="out_quad"

            )



            animacion_salida.start(tarjeta_anterior)



            self.iniciar_flotacion(tarjeta_anterior)



        tarjeta_actual = self.tarjetas_inicio[nuevo_indice]



        self.detener_flotacion(tarjeta_actual)



        Animation.cancel_all(

            tarjeta_actual,

            "intensidad_sombra",

            "width"

        )



        ancho = min(

            Window.width - dp(36),

            dp(440)

        )



        animacion_entrada = Animation(

            intensidad_sombra=1,

            width=ancho,

            duration=0.24,

            t="out_back"

        )



        animacion_entrada.start(tarjeta_actual)
# SELECCIÓN MANUAL
    def seleccionar_opcion(self, tarjeta, destino):



        try:



            indice = self.tarjetas_inicio.index(tarjeta)



        except ValueError:



            return



        self.cambiar_seleccion(indice)



        Animation.cancel_all(

            tarjeta,

            "width"

        )



        ancho = min(

            Window.width - dp(36),

            dp(440)

        )



        animacion = (

            Animation(

                width=ancho + dp(4),

                duration=0.09,

                t="out_quad"

            )

            +

            Animation(

                width=ancho,

                duration=0.13,

                t="out_back"

            )

        )



        animacion.bind(

            on_complete=lambda *_:

            Clock.schedule_once(

                lambda _dt: self.ir_a(destino),

                0.06

            )

        )



        animacion.start(tarjeta)
# LIMPIAR ANIMACIONES AL SALIR
    def on_leave(self, *_):



        for tarjeta in self.tarjetas_inicio:



            Animation.cancel_all(tarjeta)



        self.animaciones_flotantes.clear()
# =========================================================# MENSAJES# =========================================================
class BurbujaChat(BoxLayout):



    def __init__(

        self,

        autor,

        mensaje,

        hora,

        propio=False,

        **kwargs

    ):



        super().__init__(

            orientation="vertical",

            size_hint_y=None,

            spacing=dp(4),

            padding=[dp(10), dp(8)],

            **kwargs

        )



        fondo = ROJO if propio else BLANCO



        color_texto = BLANCO if propio else NEGRO



        color_meta = (

            (1, 0.78, 0.80, 1)

            if propio else GRIS_OSCURO

        )



        with self.canvas.before:



            Color(*fondo)



            self.bg_rect = Rectangle(

                pos=self.pos,

                size=self.size

            )



        self.bind(

            pos=self.actualizar_fondo,

            size=self.actualizar_fondo

        )



        self.add_widget(

            Texto(

                text=autor.upper(),

                color=color_meta,

                size=10,

                bold=True,

                size_hint_y=None,

                height=dp(17)

            )

        )



        cuerpo = Label(

            text=mensaje,

            color=color_texto,

            font_size=sp(13),

            halign="left",

            valign="middle",

            size_hint_y=None

        )



        cuerpo.bind(

            width=lambda obj, w: setattr(

                obj,

                "text_size",

                (max(dp(40), w), None)

            ),

            texture_size=lambda obj, value: setattr(

                obj,

                "height",

                value[1] + dp(8)

            )

        )



        self.add_widget(cuerpo)



        self.add_widget(

            Texto(

                text=hora,

                color=color_meta,

                size=9,

                halign="right",

                size_hint_y=None,

                height=dp(15)

            )

        )



        self.bind(

            minimum_height=self.setter("height")

        )



    def actualizar_fondo(self, *_):



        self.bg_rect.pos = self.pos

        self.bg_rect.size = self.size





class MensajesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Mensajes", **kwargs)
        self.conversaciones = []
        self.mensajes = []
        self.usuario_actual = None
        self.estado = "Cargando conversaciones..."
        self.construir_interfaz()

    def on_pre_enter(self, *_):
        self.cargar_conversaciones()

    def construir_interfaz(self):
        contenido = BoxLayout(orientation="vertical", padding=[dp(10), dp(8)], spacing=dp(7))
        barra = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(6))
        barra.add_widget(Texto(text="PHANTOM CHAT", color=BLANCO, size=13, bold=True))
        barra.add_widget(Widget())
        barra.add_widget(crear_boton("↻", self.cargar_conversaciones, ROJO_OSCURO, alto=30))
        contenido.add_widget(barra)

        self.lista_contactos = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.lista_contactos.bind(minimum_height=self.lista_contactos.setter("height"))
        self.scroll_contactos = ScrollView(do_scroll_x=False, size_hint_y=None, height=dp(105), bar_width=dp(2))
        self.scroll_contactos.add_widget(self.lista_contactos)
        contenido.add_widget(self.scroll_contactos)

        self.header_chat = Panel(color=ROJO_OSCURO, orientation="horizontal", size_hint_y=None, height=dp(38), padding=dp(8))
        self.header_chat.add_widget(Texto(text="◆ SELECCIONA UNA CONVERSACIÓN", color=BLANCO, size=11, bold=True))
        contenido.add_widget(self.header_chat)

        self.scroll_chat = ScrollView(do_scroll_x=False, bar_width=dp(3), scroll_type=["bars", "content"])
        self.area_chat = GridLayout(cols=1, spacing=dp(7), padding=[dp(4), dp(8)], size_hint_y=None)
        self.area_chat.bind(minimum_height=self.area_chat.setter("height"))
        self.scroll_chat.add_widget(self.area_chat)
        contenido.add_widget(self.scroll_chat)

        compositor = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(46), spacing=dp(6))
        self.entrada = TextInput(hint_text="Escribe un mensaje...", multiline=False, font_size=sp(14), foreground_color=BLANCO, hint_text_color=GRIS, background_normal="", background_active="", background_color=PANEL_CLARO, padding=[dp(10), dp(12)], cursor_color=ROJO)
        self.entrada.bind(on_text_validate=self.enviar_mensaje)
        boton = crear_boton("➤", self.enviar_mensaje, ROJO, alto=46, font_size=20)
        boton.size_hint_x = None; boton.width = dp(52)
        compositor.add_widget(self.entrada); compositor.add_widget(boton)
        contenido.add_widget(compositor)
        self.preparar(contenido)
        self.mostrar_estado("Inicia sesión para consultar tus mensajes.")

    def mostrar_estado(self, mensaje):
        self.area_chat.clear_widgets()
        self.area_chat.add_widget(Texto(text=mensaje, color=GRIS, size=11, halign="center", size_hint_y=None, height=dp(50)))

    def cargar_conversaciones(self, *_):
        app = App.get_running_app()
        if not app.token: return
        self.mostrar_estado("Consultando conversaciones...")
        app.ejecutar_api(f"{API_BASE_URL}/mensajes/listar_conversaciones.php", callback=self._conversaciones_recibidas)

    def _conversaciones_recibidas(self, respuesta, error):
        if error or not respuesta.get("success"):
            self.mostrar_estado(error or respuesta.get("mensaje", "No se pudieron cargar las conversaciones.")); return
        self.conversaciones = respuesta.get("conversaciones", [])
        self.lista_contactos.clear_widgets()
        if not self.conversaciones:
            self.lista_contactos.add_widget(Texto(text="AÚN NO TIENES CONVERSACIONES", color=GRIS, size=10, halign="center", size_hint_y=None, height=dp(42)))
            if self.usuario_actual:
                self.abrir_conversacion(self.usuario_actual)
            else:
                self.mostrar_estado("Tus conversaciones aparecerán aquí cuando recibas o envíes un mensaje.")
            return
        for c in self.conversaciones:
            nombre = c.get("nombre_usuario", "Jugador")
            ultimo = c.get("ultimo_contenido", "Sin mensajes") or "Sin mensajes"
            no_leidos = int(c.get("no_leidos") or 0)
            etiqueta = f"{nombre}  ·  {no_leidos} nuevos\n{ultimo[:55]}"
            b = crear_boton(etiqueta, lambda _, dato=c: self.abrir_conversacion(dato), PANEL_CLARO, alto=54, font_size=10)
            self.lista_contactos.add_widget(b)
        if self.usuario_actual:
            match = next((c for c in self.conversaciones if int(c["id_usuario"]) == int(self.usuario_actual["id_usuario"])), None)
            if match: self.abrir_conversacion(match)

    def abrir_conversacion(self, contacto):
        self.usuario_actual = contacto
        nombre = contacto.get("nombre_usuario", "Jugador")
        self.header_chat.clear_widgets()
        self.header_chat.add_widget(Texto(text=f"◆ {nombre.upper()}", color=BLANCO, size=11, bold=True))
        app = App.get_running_app()
        url = f"{API_BASE_URL}/mensajes/listar.php?usuario_id={int(contacto['id_usuario'])}"
        self.mostrar_estado("Cargando mensajes...")
        app.ejecutar_api(url, callback=self._mensajes_recibidos)

    def _mensajes_recibidos(self, respuesta, error):
        if error or not respuesta.get("success"):
            self.mostrar_estado(error or respuesta.get("mensaje", "No se pudieron cargar los mensajes.")); return
        self.mensajes = respuesta.get("mensajes", [])
        self.area_chat.clear_widgets()
        app = App.get_running_app(); mi_id = int((app.usuario or {}).get("id_usuario") or 0)
        for dato in self.mensajes:
            propio = int(dato.get("id_remitente") or 0) == mi_id
            fecha = str(dato.get("fecha_envio", ""))
            hora = fecha[11:16] if len(fecha) >= 16 else fecha
            fila = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(82))
            burbuja = BurbujaChat(autor="TÚ" if propio else dato.get("remitente", "JUGADOR"), mensaje=dato.get("contenido", ""), hora=hora, propio=propio)
            if propio: fila.add_widget(Widget()); fila.add_widget(burbuja)
            else: fila.add_widget(burbuja); fila.add_widget(Widget())
            self.area_chat.add_widget(fila)
        if not self.mensajes: self.mostrar_estado("Todavía no hay mensajes. ¡Envía el primero!")
        Clock.schedule_once(lambda dt: setattr(self.scroll_chat, "scroll_y", 0), .1)

    def enviar_mensaje(self, *_):
        texto = self.entrada.text.strip()
        if not texto or not self.usuario_actual: return
        app = App.get_running_app(); self.entrada.disabled = True
        datos = {"id_destinatario": int(self.usuario_actual["id_usuario"]), "contenido": texto}
        app.ejecutar_api(f"{API_BASE_URL}/mensajes/enviar.php", metodo="POST", datos=datos, callback=self._mensaje_enviado)

    def _mensaje_enviado(self, respuesta, error):
        self.entrada.disabled = False
        if error or not respuesta.get("success"):
            self.mostrar_estado(error or respuesta.get("mensaje", "No se pudo enviar el mensaje.")); return
        self.entrada.text = ""
        self.abrir_conversacion(self.usuario_actual)


class JugadoresScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Jugadores", **kwargs)
        self.jugadores = []
        self.estado = "Inicia sesión para consultar jugadores."
        self.construir_interfaz()

    def on_pre_enter(self, *_): self.cargar_jugadores()

    def construir_interfaz(self):
        contenido = BoxLayout(orientation="vertical", padding=[dp(12), dp(8)], spacing=dp(7))
        barra = BoxLayout(size_hint_y=None, height=dp(32), spacing=dp(6))
        barra.add_widget(Texto(text="PLAYER DATABASE", color=BLANCO, size=13, bold=True)); barra.add_widget(Widget())
        barra.add_widget(crear_boton("↻", self.cargar_jugadores, ROJO_OSCURO, alto=30))
        contenido.add_widget(barra)
        self.scroll, self.lista = crear_scroll_lista(espaciado=dp(7), padding=[dp(3), dp(4)])
        contenido.add_widget(self.scroll)
        self.preparar(contenido)
        self.mostrar_estado(self.estado)

    def mostrar_estado(self, mensaje):
        self.lista.clear_widgets(); self.lista.add_widget(Texto(text=mensaje, color=GRIS, size=11, halign="center", size_hint_y=None, height=dp(55)))

    def cargar_jugadores(self, *_):
        app=App.get_running_app()
        if not app.token:return
        self.mostrar_estado("Consultando jugadores...")
        app.ejecutar_api(f"{API_BASE_URL}/jugadores/listar.php", callback=self._recibidos)

    def _recibidos(self, respuesta, error):
        if error or not respuesta.get("success"):
            self.estado=error or respuesta.get("mensaje", "No se pudieron consultar los jugadores.");self.mostrar_estado(self.estado);return
        self.jugadores=respuesta.get("jugadores",[]);self.lista.clear_widgets()
        if not self.jugadores:self.mostrar_estado("Todavía no hay jugadores registrados.");return
        for i,j in enumerate(self.jugadores,1):
            card=Panel(color=PANEL_CLARO,orientation="horizontal",size_hint_y=None,height=dp(78),padding=dp(9),spacing=dp(8))
            card.add_widget(Texto(text=f"#{i}",color=ROJO_BRILLO,size=18,bold=True,halign="center",size_hint_x=.15))
            info=BoxLayout(orientation="vertical",spacing=dp(2))
            info.add_widget(Texto(text=j.get("nickname") or j.get("nombre_usuario","Jugador"),color=BLANCO,size=12,bold=True))
            info.add_widget(Texto(text=f"{j.get('victorias',0)} V  ·  {j.get('derrotas',0)} D  ·  {j.get('empates',0)} E",color=GRIS,size=9))
            card.add_widget(info)
            card.add_widget(Texto(text=f"{j.get('elo',0)} ELO",color=VERDE,size=11,bold=True,halign="right",size_hint_x=.22))
            btn=crear_boton("CHAT",lambda _,dato=j:self.abrir_chat(dato),ROJO_OSCURO,alto=32,font_size=9)
            btn.size_hint_x=None;btn.width=dp(55);card.add_widget(btn)
            self.lista.add_widget(card)

    def abrir_chat(self, jugador):
        app=App.get_running_app()
        if int(jugador.get("id_usuario") or 0)==int((app.usuario or {}).get("id_usuario") or 0):
            return
        pantalla=app.sm.get_screen("mensajes")
        contacto={"id_usuario":int(jugador["id_usuario"]),"nombre_usuario":jugador.get("nombre_usuario") or jugador.get("nickname") or "Jugador"}
        pantalla.usuario_actual=contacto
        app.sm.current="mensajes"
        Clock.schedule_once(lambda dt:pantalla.abrir_conversacion(contacto),.15)


class TorneosScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Torneos", **kwargs)
        self.torneos=[];self.estado="Inicia sesión para consultar torneos."
        self.construir_interfaz()

    def on_pre_enter(self,*_):
        self.construir_interfaz()
        self.cargar_torneos()

    def construir_interfaz(self):
        contenido=BoxLayout(orientation="vertical",padding=[dp(12),dp(8)],spacing=dp(7))
        barra=BoxLayout(size_hint_y=None,height=dp(30),spacing=dp(6))
        barra.add_widget(Texto(text="EVENTOS ACTIVOS",color=BLANCO,size=13,bold=True));barra.add_widget(Widget())
        app = App.get_running_app()
        if app and app.usuario and int(app.usuario.get("id_rol") or 0) == 1:
            barra.add_widget(crear_boton("⚙ ADMIN",lambda *_: setattr(app.sm,"current","admin_torneos"),ROJO,alto=30,font_size=9))
        barra.add_widget(crear_boton("↻ ACTUALIZAR",self.cargar_torneos,ROJO_OSCURO,alto=30,font_size=9));contenido.add_widget(barra)
        self.scroll,self.lista=crear_scroll_lista(espaciado=dp(9),padding=[dp(4),dp(4)])
        contenido.add_widget(self.scroll);self.preparar(contenido);self.mostrar_estado(self.estado)

    def mostrar_estado(self,mensaje):
        self.lista.clear_widgets();self.lista.add_widget(Texto(text=mensaje,color=GRIS,size=11,halign="center",size_hint_y=None,height=dp(55)))

    def cargar_torneos(self,*_):
        app=App.get_running_app()
        if not app.token:return
        self.mostrar_estado("Consultando torneos en el servidor...")
        app.ejecutar_api(f"{API_BASE_URL}/torneos/listar.php",callback=self._torneos_recibidos)

    def _torneos_recibidos(self,respuesta,error):
        if error or not respuesta.get("success"):
            self.estado=error or respuesta.get("mensaje","No se pudieron cargar los torneos.");self.mostrar_estado(self.estado);return
        self.torneos=respuesta.get("torneos",[]);self.lista.clear_widgets()
        if not self.torneos:self.mostrar_estado("No hay torneos disponibles.");return
        for t in self.torneos:
            card=Panel(color=PANEL_CLARO,orientation="vertical",size_hint_y=None,height=dp(142),padding=[dp(11),dp(8)],spacing=dp(4))
            card.add_widget(Texto(text=t.get("nombre","TORNEO").upper(),color=BLANCO,size=13,bold=True,size_hint_y=None,height=dp(21)))
            card.add_widget(Texto(text=f"Juego: {t.get('juego','—')}",color=GRIS,size=10,size_hint_y=None,height=dp(17)))
            fecha=str(t.get("fecha_inicio",""))
            card.add_widget(Texto(text=f"{fecha}  |  {t.get('inscritos',0)} / {t.get('max_jugadores',0)} jugadores",color=BLANCO,size=9,size_hint_y=None,height=dp(17)))
            estado=t.get("estado","proximo").replace("_"," ").upper()
            card.add_widget(Texto(text=f"ESTADO: {estado}",color=ROJO_BRILLO,size=9,bold=True,size_hint_y=None,height=dp(16)))
            inscrito=bool(t.get("inscrito"));cupos=int(t.get("cupos_disponibles",0));activo=t.get("estado")=="inscripciones"
            if inscrito: label="RETIRAR INSCRIPCIÓN";color=ROJO_OSCURO
            elif activo and cupos>0:label="INSCRIBIRSE";color=ROJO
            else:label="NO DISPONIBLE";color=GRIS_OSCURO
            btn=crear_boton(label,lambda _,dato=t:self.toggle_inscripcion(dato),color=color,alto=31,font_size=9)
            btn.disabled=not inscrito and (not activo or cupos<=0);card.add_widget(btn);self.lista.add_widget(card)

    def toggle_inscripcion(self,torneo):
        app=App.get_running_app();inscrito=bool(torneo.get("inscrito"))
        url=f"{API_BASE_URL}/torneos/{'cancelar' if inscrito else 'inscribirse'}.php"
        self.mostrar_estado("Actualizando inscripción...")
        app.ejecutar_api(url,metodo="POST",datos={"id_torneo":int(torneo["id_torneo"])},callback=self._accion_inscripcion)

    def _accion_inscripcion(self,respuesta,error):
        if error or not respuesta.get("success"):
            self.estado=error or respuesta.get("mensaje","No se pudo actualizar la inscripción.");self.cargar_torneos();return
        self.estado=respuesta.get("mensaje","Inscripción actualizada.");self.cargar_torneos()


# =========================================================
# PANEL DE ADMINISTRACIÓN DE TORNEOS
# =========================================================
class AdminTorneosScreen(BaseScreen):
    URL_ADMIN = f"{API_BASE_URL}/admin/torneos"

    def __init__(self, **kwargs):
        super().__init__("Administración de torneos", **kwargs)
        self.torneos = []
        self.inscripciones = []
        self.torneo_seleccionado = None
        self.modo_inscripciones = False
        self.id_edicion = None
        self.estado = "Cargando administración..."
        self.construir_interfaz()

    def on_pre_enter(self, *_):
        app = App.get_running_app()
        if not app.usuario or int(app.usuario.get("id_rol") or 0) != 1:
            app.sm.current = "torneos"
            return
        if self.modo_inscripciones and self.torneo_seleccionado:
            self.cargar_inscripciones(self.torneo_seleccionado)
        else:
            self.cargar_torneos()

    def _etiqueta(self, texto):
        return Texto(text=texto, color=GRIS, size=9, bold=True,
                     size_hint_y=None, height=dp(17))

    def _entrada(self, hint, texto="", alto=40, multiline=False):
        return TextInput(text=str(texto or ""), hint_text=hint, multiline=multiline,
                         size_hint_y=None, height=dp(alto), font_size=sp(11),
                         foreground_color=BLANCO, hint_text_color=GRIS,
                         background_normal="", background_active="",
                         background_color=PANEL_CLARO,
                         padding=[dp(9), dp(9)], cursor_color=ROJO)

    def construir_interfaz(self):
        contenido = BoxLayout(orientation="vertical", padding=[dp(10), dp(7)], spacing=dp(6))
        barra = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        if self.modo_inscripciones:
            barra.add_widget(crear_boton("← TORNEOS", self.volver_torneos, ROJO_OSCURO, alto=31, font_size=9))
            titulo = self.torneo_seleccionado.get("nombre", "PARTICIPANTES") if self.torneo_seleccionado else "PARTICIPANTES"
            barra.add_widget(Texto(text=titulo.upper(), color=BLANCO, size=11, bold=True))
            barra.add_widget(Widget())
            barra.add_widget(crear_boton("↻", self.refrescar_inscripciones, ROJO, alto=31, font_size=12))
        else:
            barra.add_widget(crear_boton("← TORNEOS", lambda *_: setattr(App.get_running_app().sm,"current","torneos"), ROJO_OSCURO, alto=31, font_size=8))
            barra.add_widget(Texto(text="/// CONTROL DE EVENTOS", color=ROJO_BRILLO, size=11, bold=True))
            barra.add_widget(Widget())
            barra.add_widget(crear_boton("+ NUEVO", self.nuevo_torneo, ROJO, alto=31, font_size=9))
            barra.add_widget(crear_boton("↻", self.cargar_torneos, ROJO_OSCURO, alto=31, font_size=12))
        contenido.add_widget(barra)

        self.scroll, self.lista = crear_scroll_lista(espaciado=dp(8), padding=[dp(3), dp(4)])
        contenido.add_widget(self.scroll)
        self.preparar(contenido)

        if self.modo_inscripciones:
            self._dibujar_inscripciones()
        else:
            self._dibujar_formulario()
            self._dibujar_torneos()

    def _dibujar_formulario(self):
        panel = Panel(color=PANEL, orientation="vertical", size_hint_y=None,
                      padding=[dp(10), dp(9)], spacing=dp(5))
        panel.bind(minimum_height=panel.setter("height"))
        panel.add_widget(Texto(text="◆ " + ("EDITAR TORNEO" if self.id_edicion else "CREAR TORNEO"),
                               color=ROJO_BRILLO, size=12, bold=True,
                               size_hint_y=None, height=dp(22)))
        panel.add_widget(self._etiqueta("NOMBRE DEL TORNEO"))
        self.in_nombre = self._entrada("Ej. Phantom Arena")
        panel.add_widget(self.in_nombre)
        panel.add_widget(self._etiqueta("JUEGO"))
        self.in_juego = self._entrada("Ej. Persona 5 Royal")
        panel.add_widget(self.in_juego)
        panel.add_widget(self._etiqueta("DESCRIPCIÓN"))
        self.in_descripcion = self._entrada("Reglas e información del torneo", alto=62, multiline=True)
        panel.add_widget(self.in_descripcion)
        panel.add_widget(self._etiqueta("FORMATO"))
        self.in_formato = Spinner(text="eliminacion_simple", values=(
            "eliminacion_simple", "eliminacion_doble", "round_robin", "suizo"),
            size_hint_y=None, height=dp(40), background_normal="",
            background_color=PANEL_CLARO, color=BLANCO, font_size=sp(11))
        panel.add_widget(self.in_formato)
        panel.add_widget(self._etiqueta("MÁXIMO DE JUGADORES"))
        self.in_max = self._entrada("16", "16")
        panel.add_widget(self.in_max)
        panel.add_widget(self._etiqueta("FECHA DE INICIO (AAAA-MM-DD HH:MM:SS)"))
        self.in_inicio = self._entrada("2026-11-15 18:00:00")
        panel.add_widget(self.in_inicio)
        panel.add_widget(self._etiqueta("FECHA DE FINALIZACIÓN (OPCIONAL)"))
        self.in_fin = self._entrada("2026-11-15 21:00:00")
        panel.add_widget(self.in_fin)
        acciones = BoxLayout(size_hint_y=None, height=dp(39), spacing=dp(6))
        acciones.add_widget(crear_boton("GUARDAR TORNEO", self.guardar_torneo, ROJO, alto=38, font_size=9))
        acciones.add_widget(crear_boton("LIMPIAR", self.nuevo_torneo, ROJO_OSCURO, alto=38, font_size=9))
        panel.add_widget(acciones)
        self.lista.add_widget(panel)
        self.lista.add_widget(Texto(text="◆ TORNEOS REGISTRADOS", color=BLANCO, size=12, bold=True,
                                    size_hint_y=None, height=dp(25)))

    def _dibujar_torneos(self):
        if not self.torneos:
            self.lista.add_widget(Texto(text=self.estado or "No hay torneos registrados.", color=GRIS,
                                        size=10, halign="center", size_hint_y=None, height=dp(50)))
            return
        for torneo in self.torneos:
            card = Panel(color=PANEL_CLARO, orientation="vertical", size_hint_y=None,
                         height=dp(151), padding=[dp(9), dp(7)], spacing=dp(3))
            card.add_widget(Texto(text=torneo.get("nombre", "TORNEO").upper(), color=BLANCO,
                                  size=12, bold=True, size_hint_y=None, height=dp(20)))
            card.add_widget(Texto(text=f"{torneo.get('juego','—')}  |  {torneo.get('formato','').replace('_',' ').upper()}",
                                  color=GRIS, size=9, size_hint_y=None, height=dp(17)))
            card.add_widget(Texto(text=f"{torneo.get('fecha_inicio','')}  |  {torneo.get('inscritos',0)}/{torneo.get('max_jugadores',0)} inscritos  |  {torneo.get('confirmados',0)} confirmados",
                                  color=BLANCO, size=9, size_hint_y=None, height=dp(17)))
            card.add_widget(Texto(text=f"ESTADO: {torneo.get('estado','').replace('_',' ').upper()}",
                                  color=ROJO_BRILLO, size=9, bold=True, size_hint_y=None, height=dp(16)))
            fila = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(5))
            fila.add_widget(crear_boton("EDITAR", lambda _, t=torneo: self.editar_torneo(t), ROJO_OSCURO, alto=32, font_size=8))
            fila.add_widget(crear_boton("JUGADORES", lambda _, t=torneo: self.abrir_inscripciones(t), ROJO, alto=32, font_size=8))
            siguiente = {"proximo":"inscripciones", "inscripciones":"en_curso", "en_curso":"finalizado"}.get(torneo.get("estado"))
            if siguiente:
                fila.add_widget(crear_boton(siguiente.replace("_"," ").upper(),
                                            lambda _, t=torneo, e=siguiente: self.cambiar_estado(t,e),
                                            ROJO_OSCURO, alto=32, font_size=8))
            if torneo.get("estado") not in ("finalizado", "cancelado"):
                fila.add_widget(crear_boton("CANCELAR", lambda _, t=torneo: self.cambiar_estado(t,"cancelado"), ROJO_OSCURO, alto=32, font_size=8))
            card.add_widget(fila)
            self.lista.add_widget(card)

    def _dibujar_inscripciones(self):
        if not self.inscripciones:
            self.lista.add_widget(Texto(text="Este torneo todavía no tiene inscripciones.", color=GRIS,
                                        size=10, halign="center", size_hint_y=None, height=dp(50)))
            return
        for ins in self.inscripciones:
            card = Panel(color=PANEL_CLARO, orientation="vertical", size_hint_y=None,
                         height=dp(105), padding=[dp(9), dp(6)], spacing=dp(3))
            card.add_widget(Texto(text=f"{ins.get('nickname','JUGADOR')}  |  {ins.get('nombre_usuario','')}",
                                  color=BLANCO, size=11, bold=True, size_hint_y=None, height=dp(19)))
            card.add_widget(Texto(text=f"ELO {ins.get('elo',0)}  |  {ins.get('victorias',0)} V  {ins.get('derrotas',0)} D  |  {ins.get('estado','').upper()}",
                                  color=GRIS, size=9, size_hint_y=None, height=dp(17)))
            fila = BoxLayout(size_hint_y=None, height=dp(31), spacing=dp(4))
            estado = ins.get("estado")
            if estado in ("inscrito", "confirmado"):
                fila.add_widget(crear_boton("CONFIRMAR", lambda _, i=ins: self.gestionar_inscripcion(i,"confirmado"), VERDE, alto=29, font_size=8))
                fila.add_widget(crear_boton("RETIRAR", lambda _, i=ins: self.gestionar_inscripcion(i,"retirado"), ROJO_OSCURO, alto=29, font_size=8))
                fila.add_widget(crear_boton("DESCALIFICAR", lambda _, i=ins: self.gestionar_inscripcion(i,"descalificado"), ROJO, alto=29, font_size=8))
            else:
                fila.add_widget(Texto(text="INSCRIPCIÓN CERRADA", color=GRIS, size=8))
            card.add_widget(fila)
            self.lista.add_widget(card)

    def cargar_torneos(self, *_):
        app = App.get_running_app()
        if not app.token: return
        self.lista.clear_widgets()
        self.lista.add_widget(Texto(text="Consultando torneos...", color=GRIS, size=10, halign="center"))
        app.ejecutar_api(f"{self.URL_ADMIN}/listar.php", callback=self._torneos_recibidos)

    def _torneos_recibidos(self, respuesta, error):
        if error or not respuesta or not respuesta.get("success"):
            self.estado = error or (respuesta or {}).get("mensaje", "No se pudieron cargar los torneos.")
            self.lista.clear_widgets(); self._dibujar_torneos(); return
        self.torneos = respuesta.get("torneos", [])
        self.estado = "Torneos cargados."
        self.construir_interfaz()

    def nuevo_torneo(self, *_):
        self.id_edicion = None
        self.construir_interfaz()

    def editar_torneo(self, torneo):
        self.id_edicion = int(torneo["id_torneo"])
        self.construir_interfaz()
        self.in_nombre.text = torneo.get("nombre", "")
        self.in_juego.text = torneo.get("juego", "")
        self.in_descripcion.text = torneo.get("descripcion") or ""
        self.in_formato.text = torneo.get("formato", "eliminacion_simple")
        self.in_max.text = str(torneo.get("max_jugadores", 16))
        self.in_inicio.text = str(torneo.get("fecha_inicio", ""))
        self.in_fin.text = str(torneo.get("fecha_fin") or "")

    def guardar_torneo(self, *_):
        try:
            max_jugadores = int(self.in_max.text.strip())
        except ValueError:
            self.estado = "El máximo de jugadores debe ser un número."
            return
        datos = {"nombre":self.in_nombre.text.strip(), "juego":self.in_juego.text.strip(),
                 "descripcion":self.in_descripcion.text.strip(), "formato":self.in_formato.text,
                 "max_jugadores":max_jugadores, "fecha_inicio":self.in_inicio.text.strip(),
                 "fecha_fin":self.in_fin.text.strip() or None}
        if not datos["nombre"] or not datos["juego"] or not datos["fecha_inicio"]:
            self.estado = "Completa nombre, juego y fecha de inicio."
            return
        if self.id_edicion: datos["id_torneo"] = self.id_edicion
        endpoint = "actualizar.php" if self.id_edicion else "crear.php"
        self.estado = "Guardando torneo..."
        App.get_running_app().ejecutar_api(f"{self.URL_ADMIN}/{endpoint}", metodo="POST", datos=datos,
                                           callback=self._torneo_guardado)

    def _torneo_guardado(self, respuesta, error):
        if error or not respuesta or not respuesta.get("success"):
            self.estado = error or (respuesta or {}).get("mensaje", "No se pudo guardar el torneo.")
            self.construir_interfaz()
            return
        self.id_edicion = None
        self.estado = respuesta.get("mensaje", "Torneo guardado.")
        self.cargar_torneos()

    def cambiar_estado(self, torneo, estado):
        datos = {"id_torneo":int(torneo["id_torneo"]), "estado":estado}
        App.get_running_app().ejecutar_api(f"{self.URL_ADMIN}/cambiar_estado.php", metodo="POST", datos=datos,
                                           callback=lambda r,e:self._accion_admin(r,e,"Estado actualizado."))

    def _accion_admin(self, respuesta, error, correcto):
        if error or not respuesta or not respuesta.get("success"):
            self.estado = error or (respuesta or {}).get("mensaje", "No se pudo completar la operación.")
        else:
            self.estado = respuesta.get("mensaje", correcto)
        self.cargar_torneos()

    def abrir_inscripciones(self, torneo):
        self.torneo_seleccionado = torneo
        self.modo_inscripciones = True
        self.inscripciones = []
        self.construir_interfaz()
        self.cargar_inscripciones(torneo)

    def cargar_inscripciones(self, torneo=None):
        if torneo is not None: self.torneo_seleccionado = torneo
        if not self.torneo_seleccionado: return
        ident = int(self.torneo_seleccionado["id_torneo"])
        url = f"{self.URL_ADMIN}/inscripciones.php?id_torneo={ident}"
        self.lista.clear_widgets()
        self.lista.add_widget(Texto(text="Consultando participantes...", color=GRIS, size=10))
        App.get_running_app().ejecutar_api(url, callback=self._inscripciones_recibidas)

    def _inscripciones_recibidas(self, respuesta, error):
        if error or not respuesta or not respuesta.get("success"):
            self.estado = error or (respuesta or {}).get("mensaje", "No se pudieron consultar las inscripciones.")
            self.lista.clear_widgets(); self._dibujar_inscripciones(); return
        self.inscripciones = respuesta.get("inscripciones", [])
        self.lista.clear_widgets()
        self.lista.add_widget(Texto(text=f"{respuesta.get('total',0)} INSCRIPCIONES", color=ROJO_BRILLO,
                                    size=11, bold=True, size_hint_y=None, height=dp(25)))
        self._dibujar_inscripciones()

    def gestionar_inscripcion(self, inscripcion, estado):
        datos = {"id_inscripcion":int(inscripcion["id_inscripcion"]), "estado":estado}
        App.get_running_app().ejecutar_api(f"{self.URL_ADMIN}/gestionar_inscripcion.php", metodo="POST", datos=datos,
                                           callback=lambda r,e:self._inscripcion_gestionada(r,e))

    def _inscripcion_gestionada(self, respuesta, error):
        if error or not respuesta or not respuesta.get("success"):
            self.estado = error or (respuesta or {}).get("mensaje", "No se pudo actualizar la inscripción.")
        else:
            self.estado = respuesta.get("mensaje", "Inscripción actualizada.")
        self.cargar_inscripciones()

    def refrescar_inscripciones(self, *_):
        self.cargar_inscripciones()

    def volver_torneos(self, *_):
        self.modo_inscripciones = False
        self.torneo_seleccionado = None
        self.construir_interfaz()
        self.cargar_torneos()


class ContenidoScreen(BaseScreen):



    def __init__(self, titulo, descripcion, **kwargs):



        super().__init__(titulo, **kwargs)



        contenido = FloatLayout()



        with contenido.canvas.before:



            Color(*NEGRO)



            self.fondo_contenido = Rectangle(

                pos=contenido.pos,

                size=contenido.size

            )



            Color(*ROJO_OSCURO)



            self.franga_lateral = Rectangle(

                pos=contenido.pos,

                size=(dp(7), contenido.height)

            )



        contenido.bind(

            pos=self.actualizar_fondo_contenido,

            size=self.actualizar_fondo_contenido

        )



        layout = BoxLayout(

            orientation="vertical",

            padding=[dp(18), dp(12)],

            spacing=dp(12)

        )



        encabezado = BoxLayout(

            orientation="vertical",

            size_hint_y=None,

            height=dp(76),

            spacing=dp(2)

        )



        encabezado.add_widget(

            Texto(

                text="/// GAMEZONE // SYSTEM",

                color=ROJO,

                size=11,

                bold=True

            )

        )



        encabezado.add_widget(

            Texto(

                text=titulo.upper(),

                color=BLANCO,

                size=28,

                bold=True

            )

        )



        layout.add_widget(encabezado)



        panel = FloatLayout(

            size_hint_y=None,

            height=dp(205)

        )



        with panel.canvas.before:



            Color(*ROJO_OSCURO)



            self.sombra_panel = Rectangle(

                pos=panel.pos,

                size=panel.size

            )



            Color(0.005, 0.005, 0.008, 1)



            self.marco_panel = Rectangle(

                pos=panel.pos,

                size=panel.size

            )



            Color(*BLANCO)



            self.superficie_panel = Rectangle(

                pos=(panel.x + dp(5), panel.y + dp(5)),

                size=(

                    max(0, panel.width - dp(10)),

                    max(0, panel.height - dp(10))

                )

            )



            Color(0.005, 0.005, 0.008, 1)



            self.contorno_angular = Line(

                points=[],

                close=True,

                width=1.8

            )



            Color(*ROJO)



            self.acento_rojo = Line(

                points=[],

                width=dp(4)

            )



        panel.bind(

            pos=self.actualizar_panel_contenido,

            size=self.actualizar_panel_contenido

        )



        textos = BoxLayout(

            orientation="vertical",

            padding=[dp(18), dp(17)],

            spacing=dp(7)

        )



        textos.add_widget(

            Texto(

                text="◆  SECCIÓN SELECCIONADA",

                color=ROJO,

                size=12,

                bold=True,

                size_hint_y=None,

                height=dp(23)

            )

        )



        textos.add_widget(

            Texto(

                text=titulo.upper(),

                color=NEGRO,

                size=23,

                bold=True,

                size_hint_y=None,

                height=dp(36)

            )

        )



        textos.add_widget(

            Texto(

                text=descripcion,

                color=GRIS_OSCURO,

                size=14

            )

        )



        textos.add_widget(

            Texto(

                text="///  GAMEZONE SYSTEM",

                color=ROJO,

                size=10,

                bold=True,

                size_hint_y=None,

                height=dp(20)

            )

        )



        panel.add_widget(textos)



        layout.add_widget(panel)



        layout.add_widget(

            Texto(

                text="━━━━━━━━━━━━━━━━━━━━",

                color=ROJO,

                size=15,

                bold=True,

                size_hint_y=None,

                height=dp(24)

            )

        )



        layout.add_widget(

            Texto(

                text="PREPÁRATE PARA EL SIGUIENTE DESAFÍO",

                color=BLANCO,

                size=12,

                bold=True,

                size_hint_y=None,

                height=dp(25)

            )

        )



        layout.add_widget(Widget())



        contenido.add_widget(layout)



        self.preparar(contenido)



    def actualizar_fondo_contenido(self, instancia, *_):



        self.fondo_contenido.pos = instancia.pos

        self.fondo_contenido.size = instancia.size



        self.franga_lateral.pos = instancia.pos



        self.franga_lateral.size = (

            dp(7),

            instancia.height

        )



    def actualizar_panel_contenido(self, instancia, *_):



        self.sombra_panel.pos = (

            instancia.x + dp(6),

            instancia.y - dp(5)

        )



        self.sombra_panel.size = instancia.size



        self.marco_panel.pos = instancia.pos

        self.marco_panel.size = instancia.size



        self.superficie_panel.pos = (

            instancia.x + dp(5),

            instancia.y + dp(5)

        )



        self.superficie_panel.size = (

            max(0, instancia.width - dp(10)),

            max(0, instancia.height - dp(10))

        )



        self.contorno_angular.points = [

            instancia.x + dp(12),

            instancia.y + dp(5),



            instancia.right - dp(5),

            instancia.y + dp(5),



            instancia.right - dp(12),

            instancia.top - dp(5),



            instancia.x + dp(5),

            instancia.top - dp(5)

        ]



        self.acento_rojo.points = [

            instancia.x + dp(12),

            instancia.top - dp(12),



            instancia.x + instancia.width * 0.48,

            instancia.top - dp(12)

        ]
# =========================================================# TORNEOS# =========================================================
# =========================================================# =========================================================
# RANKING - CLASIFICACIÓN ELO
# =========================================================

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*NEGRO)
            self.fondo = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._actualizar_fondo, size=self._actualizar_fondo)

        raiz = BoxLayout(orientation="vertical", padding=[dp(24), dp(20)], spacing=dp(12))
        raiz.add_widget(Widget())
        tarjeta = Panel(
            color=PANEL, orientation="vertical", padding=[dp(20), dp(18)],
            spacing=dp(12), size_hint_y=None, height=dp(390)
        )
        tarjeta.add_widget(Texto(
            text="[b]/// GAMEZONE [color=F52640]PRO[/color] ◆[/b]",
            markup=True, color=BLANCO, size=19, halign="center"
        ))
        tarjeta.add_widget(Texto(
            text="◢ ACCESO DE JUGADOR ◤", color=ROJO_BRILLO,
            size=13, bold=True, halign="center"
        ))
        tarjeta.add_widget(Texto(
            text="Inicia sesión para acceder a tu cuenta y al ranking global.",
            color=GRIS, size=10, halign="center"
        ))
        tarjeta.add_widget(Texto(
            text="USUARIO O CORREO", color=GRIS, size=10, bold=True,
            size_hint_y=None, height=dp(20)
        ))
        self.entrada_identificador = TextInput(
            hint_text="Ingresa tu usuario o correo", multiline=False,
            size_hint_y=None, height=dp(48), font_size=sp(13),
            foreground_color=BLANCO, hint_text_color=GRIS,
            background_normal="", background_active="",
            background_color=PANEL_CLARO, padding=[dp(12), dp(13)],
            cursor_color=ROJO
        )
        tarjeta.add_widget(self.entrada_identificador)
        tarjeta.add_widget(Texto(
            text="CONTRASEÑA", color=GRIS, size=10, bold=True,
            size_hint_y=None, height=dp(20)
        ))
        self.entrada_password = TextInput(
            hint_text="Ingresa tu contraseña", password=True, multiline=False,
            size_hint_y=None, height=dp(48), font_size=sp(13),
            foreground_color=BLANCO, hint_text_color=GRIS,
            background_normal="", background_active="",
            background_color=PANEL_CLARO, padding=[dp(12), dp(13)],
            cursor_color=ROJO
        )
        self.entrada_password.bind(on_text_validate=self.iniciar_sesion)
        tarjeta.add_widget(self.entrada_password)
        self.mensaje = Texto(
            text="", color=ROJO_BRILLO, size=10, halign="center",
            size_hint_y=None, height=dp(30)
        )
        tarjeta.add_widget(self.mensaje)
        self.boton_login = crear_boton(
            "INICIAR SESIÓN", self.iniciar_sesion, color=ROJO, alto=48
        )
        tarjeta.add_widget(self.boton_login)
        raiz.add_widget(tarjeta)
        raiz.add_widget(Widget())
        self.add_widget(raiz)

    def _actualizar_fondo(self, *_):
        self.fondo.pos = self.pos
        self.fondo.size = self.size

    def iniciar_sesion(self, *_):
        identificador = self.entrada_identificador.text.strip()
        password = self.entrada_password.text
        if not identificador or not password:
            self.mensaje.text = "Ingresa tu usuario/correo y contraseña."
            return
        self.boton_login.disabled = True
        self.boton_login.text = "CONECTANDO..."
        self.mensaje.color = GRIS
        self.mensaje.text = "Verificando credenciales..."
        App.get_running_app().iniciar_sesion(identificador, password)

    def finalizar(self, exito, mensaje):
        self.boton_login.disabled = False
        self.boton_login.text = "INICIAR SESIÓN"
        self.mensaje.color = VERDE if exito else ROJO_BRILLO
        self.mensaje.text = mensaje
        if exito:
            self.entrada_password.text = ""


class RankingScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Ranking", **kwargs)
        self.jugadores = []
        self.estado = "Inicia sesión para consultar el ranking."
        self.construir_interfaz()

    def on_pre_enter(self, *_):
        app = App.get_running_app()
        if app and app.token:
            app.cargar_ranking()

    def actualizar_datos(self, jugadores=None, mensaje=None):
        if jugadores is not None:
            self.jugadores = jugadores
        if mensaje is not None:
            self.estado = mensaje
        self.construir_interfaz()

    def construir_interfaz(self):
        contenido = BoxLayout(orientation="vertical", padding=[dp(12), dp(8)], spacing=dp(7))
        barra = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(6))
        barra.add_widget(Texto(text="TOP PLAYERS", color=BLANCO, size=13, bold=True))
        barra.add_widget(Widget())
        barra.add_widget(crear_boton("↻ ACTUALIZAR", self.refrescar, color=ROJO_OSCURO, alto=30, font_size=9))
        contenido.add_widget(barra)

        if self.jugadores:
            promedio = round(sum(int(j.get("victorias", 0) or 0) for j in self.jugadores) / len(self.jugadores))
            elo_maximo = max(int(j.get("elo", 0) or 0) for j in self.jugadores)
        else:
            promedio = 0
            elo_maximo = 0
        resumen = GridLayout(cols=2, spacing=dp(7), size_hint_y=None, height=dp(95))
        for valor, etiqueta in [
            (str(len(self.jugadores)), "JUGADORES"),
            (str(elo_maximo), "ELO MÁXIMO"),
            (str(promedio), "PROMEDIO VICTORIAS"),
            ("01", "TEMPORADA")
        ]:
            tarjeta = Panel(color=PANEL_CLARO, orientation="vertical", padding=dp(7), spacing=dp(2))
            tarjeta.add_widget(Texto(text=valor, color=ROJO_BRILLO, size=21, bold=True, halign="center"))
            tarjeta.add_widget(Texto(text=etiqueta, color=GRIS, size=9, bold=True, halign="center"))
            resumen.add_widget(tarjeta)
        contenido.add_widget(resumen)
        contenido.add_widget(Texto(
            text="◆ CLASIFICACIÓN GENERAL", color=BLANCO, size=13, bold=True,
            size_hint_y=None, height=dp(26)
        ))
        if not self.jugadores:
            contenido.add_widget(Texto(
                text=self.estado, color=GRIS, size=11, halign="center"
            ))
        else:
            scroll, lista = crear_scroll_lista(espaciado=dp(7), padding=[dp(3), dp(4)])
            ordenados = sorted(self.jugadores, key=lambda jugador: int(jugador.get("elo", 0) or 0), reverse=True)
            for posicion, jugador in enumerate(ordenados, start=1):
                tarjeta = Panel(
                    color=PANEL_CLARO, orientation="horizontal", size_hint_y=None,
                    height=dp(76), padding=[dp(8), dp(6)], spacing=dp(8)
                )
                tarjeta.add_widget(Texto(
                    text=f'#{jugador.get("posicion", posicion)}',
                    color=ROJO_BRILLO if posicion == 1 else BLANCO,
                    size=19, bold=True, halign="center", size_hint_x=0.17
                ))
                info = BoxLayout(orientation="vertical", spacing=dp(2))
                info.add_widget(Texto(text=str(jugador.get("nombre", "Jugador")), color=BLANCO, size=13, bold=True))
                info.add_widget(Texto(
                    text=f'{jugador.get("victorias", 0)} VICTORIAS  |  {jugador.get("derrotas", 0)} DERROTAS',
                    color=GRIS, size=9
                ))
                tarjeta.add_widget(info)
                tarjeta.add_widget(Texto(
                    text=f'{jugador.get("elo", 0)} ELO', color=VERDE,
                    size=12, bold=True, halign="right", size_hint_x=0.30
                ))
                lista.add_widget(tarjeta)
            contenido.add_widget(scroll)
        self.preparar(contenido)

    def refrescar(self, *_):
        app = App.get_running_app()
        if app and app.token:
            self.actualizar_datos(mensaje="Actualizando ranking...")
            app.cargar_ranking()
        else:
            self.actualizar_datos(mensaje="Debes iniciar sesión para consultar el ranking.")


# =========================================================
# PERFIL DEL JUGADOR
# =========================================================

class PerfilScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__("Perfil", **kwargs)
        self.nombre_usuario="Jugador";self.correo="";self.biografia="";self.apodo="";self.elo=0;self.victorias=0;self.derrotas=0;self.empates=0;self.partidas=0
        self.estado="Inicia sesión para consultar tu perfil."
        self.construir_interfaz()

    def on_pre_enter(self,*_): self.cargar_perfil()

    def construir_interfaz(self):
        contenido=BoxLayout(orientation="vertical",padding=[dp(12),dp(8)],spacing=dp(8))
        self.scroll,self.lista=crear_scroll_lista(espaciado=dp(9),padding=[dp(3),dp(5)])
        perfil=Panel(color=PANEL_CLARO,orientation="vertical",size_hint_y=None,height=dp(170),padding=dp(10),spacing=dp(4))
        perfil.add_widget(Texto(text="/// PLAYER IDENTIFICATION",color=ROJO,size=10,bold=True,halign="center"))
        perfil.add_widget(Texto(text="♟",color=ROJO_BRILLO,size=38,bold=True,halign="center"))
        perfil.add_widget(Texto(text=self.nombre_usuario,color=BLANCO,size=20,bold=True,halign="center"))
        perfil.add_widget(Texto(text=f"@{self.apodo}  |  GAMEZONE MEMBER",color=GRIS,size=10,halign="center"))
        perfil.add_widget(Texto(text="◆ PERFIL DE JUGADOR",color=VERDE,size=10,bold=True,halign="center"))
        self.lista.add_widget(perfil)
        self.lista.add_widget(Texto(text="◆ ESTADÍSTICAS COMPETITIVAS",color=BLANCO,size=13,bold=True,size_hint_y=None,height=dp(24)))
        stats=GridLayout(cols=2,spacing=dp(7),size_hint_y=None,height=dp(145))
        for valor,etiqueta in [(str(self.elo),"PUNTUACIÓN ELO"),(str(self.victorias),"VICTORIAS"),(str(self.derrotas),"DERROTAS"),(str(self.partidas),"PARTIDAS")]:
            c=Panel(color=PANEL_CLARO,orientation="vertical",padding=dp(7),spacing=dp(2));c.add_widget(Texto(text=valor,color=ROJO_BRILLO,size=22,bold=True,halign="center"));c.add_widget(Texto(text=etiqueta,color=GRIS,size=9,bold=True,halign="center"));stats.add_widget(c)
        self.lista.add_widget(stats)
        self.lista.add_widget(Texto(text="◆ CONFIGURACIÓN DE CUENTA",color=BLANCO,size=13,bold=True,size_hint_y=None,height=dp(26)))
        self.lista.add_widget(Texto(text="NOMBRE DE USUARIO",color=GRIS,size=10,bold=True,size_hint_y=None,height=dp(18)))
        self.entrada_nombre=TextInput(text=self.nombre_usuario,hint_text="Nombre de usuario",multiline=False,size_hint_y=None,height=dp(43),font_size=sp(13),foreground_color=BLANCO,hint_text_color=GRIS,background_normal="",background_active="",background_color=PANEL_CLARO,padding=[dp(10),dp(11)],cursor_color=ROJO);self.lista.add_widget(self.entrada_nombre)
        self.lista.add_widget(Texto(text="CORREO ELECTRÓNICO",color=GRIS,size=10,bold=True,size_hint_y=None,height=dp(18)))
        self.entrada_correo=TextInput(text=self.correo,hint_text="correo@ejemplo.com",multiline=False,size_hint_y=None,height=dp(43),font_size=sp(13),foreground_color=BLANCO,hint_text_color=GRIS,background_normal="",background_active="",background_color=PANEL_CLARO,padding=[dp(10),dp(11)],cursor_color=ROJO);self.lista.add_widget(self.entrada_correo)
        self.lista.add_widget(Texto(text="NICKNAME",color=GRIS,size=10,bold=True,size_hint_y=None,height=dp(18)))
        self.entrada_nickname=TextInput(text=self.apodo,hint_text="Nickname",multiline=False,size_hint_y=None,height=dp(43),font_size=sp(13),foreground_color=BLANCO,hint_text_color=GRIS,background_normal="",background_active="",background_color=PANEL_CLARO,padding=[dp(10),dp(11)],cursor_color=ROJO);self.lista.add_widget(self.entrada_nickname)
        self.lista.add_widget(Texto(text="BIOGRAFÍA",color=GRIS,size=10,bold=True,size_hint_y=None,height=dp(18)))
        self.entrada_bio=TextInput(text=self.biografia,hint_text="Cuéntales algo a otros jugadores",multiline=True,size_hint_y=None,height=dp(75),font_size=sp(12),foreground_color=BLANCO,hint_text_color=GRIS,background_normal="",background_active="",background_color=PANEL_CLARO,padding=[dp(10),dp(10)],cursor_color=ROJO);self.lista.add_widget(self.entrada_bio)
        self.mensaje_estado=Texto(text=self.estado,color=GRIS,size=10,halign="center",size_hint_y=None,height=dp(30));self.lista.add_widget(self.mensaje_estado)
        self.lista.add_widget(crear_boton("GUARDAR CAMBIOS",self.guardar_perfil,color=ROJO,alto=43))
        contenido.add_widget(self.scroll);self.preparar(contenido)

    def cargar_perfil(self):
        app=App.get_running_app()
        if not app.token:return
        app.ejecutar_api(f"{API_BASE_URL}/usuarios/perfil.php",callback=self._perfil_recibido)

    def _perfil_recibido(self,respuesta,error):
        if error or not respuesta.get("success"):
            self.mensaje_estado.text=error or respuesta.get("mensaje","No se pudo cargar el perfil.");return
        d=respuesta.get("perfil",{});self.nombre_usuario=d.get("nombre_usuario") or "Jugador";self.correo=d.get("correo") or "";self.biografia=d.get("biografia") or "";self.apodo=d.get("nickname") or "";self.elo=int(d.get("elo") or 0);self.victorias=int(d.get("victorias") or 0);self.derrotas=int(d.get("derrotas") or 0);self.empates=int(d.get("empates") or 0);self.partidas=int(d.get("partidas_jugadas") or 0)
        self.construir_interfaz()

    def guardar_perfil(self,*_):
        datos={"nombre_usuario":self.entrada_nombre.text.strip(),"correo":self.entrada_correo.text.strip(),"nickname":self.entrada_nickname.text.strip(),"biografia":self.entrada_bio.text.strip()}
        if not datos["nombre_usuario"] or not datos["correo"]:
            self.mensaje_estado.text="El nombre y correo son obligatorios.";return
        self.mensaje_estado.text="Guardando cambios..."
        App.get_running_app().ejecutar_api(f"{API_BASE_URL}/usuarios/actualizar_perfil.php",metodo="POST",datos=datos,callback=self._perfil_guardado)

    def _perfil_guardado(self,respuesta,error):
        if error or not respuesta.get("success"):
            self.mensaje_estado.text=error or respuesta.get("mensaje","No se pudo guardar el perfil.");return
        self.mensaje_estado.text=respuesta.get("mensaje","Perfil actualizado.");self.cargar_perfil()


# =========================================================
# APP PRINCIPAL
# =========================================================

class GameZoneProApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token=None;self.usuario=None;self._ranking_cargando=False

    def ejecutar_api(self,url,metodo="GET",datos=None,callback=None):
        if not self.token:
            if callback: Clock.schedule_once(lambda dt: callback({"success":False,"mensaje":"Inicia sesión nuevamente."},None),0)
            return
        def tarea():
            try:
                respuesta=solicitud_api(url,metodo=metodo,datos=datos,token=self.token)
                Clock.schedule_once(lambda dt: callback(respuesta,None) if callback else None,0)
            except Exception as exc:
                mensaje=str(exc)
                Clock.schedule_once(lambda dt: callback(None,mensaje) if callback else None,0)
        threading.Thread(target=tarea,daemon=True).start()

    def build(self):
        self.sm=ScreenManager();self.pantalla_login=LoginScreen(name="login")
        self.sm.add_widget(self.pantalla_login);self.sm.add_widget(InicioScreen(name="inicio"))
        self.sm.add_widget(TorneosScreen(name="torneos"));self.sm.add_widget(MensajesScreen(name="mensajes"))
        self.sm.add_widget(RankingScreen(name="ranking"));self.sm.add_widget(JugadoresScreen(name="jugadores"));self.sm.add_widget(PerfilScreen(name="perfil"))
        self.sm.add_widget(AdminTorneosScreen(name="admin_torneos"))
        self.sm.current="login";return self.sm

    def iniciar_sesion(self,identificador,password):
        def tarea():
            try:
                respuesta=solicitud_api(API_LOGIN_URL,metodo="POST",datos={"identificador":identificador,"password":password})
                if not respuesta.get("success") or not respuesta.get("token"):
                    mensaje=respuesta.get("mensaje","No fue posible iniciar sesión.");Clock.schedule_once(lambda dt:self.pantalla_login.finalizar(False,mensaje),0);return
                self.token=respuesta["token"];self.usuario=respuesta.get("usuario",{});Clock.schedule_once(lambda dt:self._login_correcto(),0)
            except Exception as error:
                mensaje=str(error);Clock.schedule_once(lambda dt:self.pantalla_login.finalizar(False,mensaje),0)
        threading.Thread(target=tarea,daemon=True).start()

    def _login_correcto(self):
        self.pantalla_login.finalizar(True,"Sesión iniciada correctamente.")
        perfil=self.sm.get_screen("perfil");datos=self.usuario or {}
        perfil.nombre_usuario=datos.get("nombre_usuario") or "Jugador";perfil.apodo=datos.get("nickname") or "";perfil.elo=int(datos.get("elo") or 0)
        self.sm.current="inicio"

    def cargar_ranking(self):
        if not self.token or self._ranking_cargando:return
        self._ranking_cargando=True;pantalla=self.sm.get_screen("ranking");pantalla.actualizar_datos(mensaje="Consultando clasificación en el servidor...")
        def tarea():
            try:
                respuesta=solicitud_api(API_RANKING_URL,token=self.token)
                if not respuesta.get("success"):
                    mensaje=respuesta.get("mensaje","No se pudo obtener el ranking.")
                    if respuesta.get("http_code")==401:Clock.schedule_once(lambda dt:self.cerrar_sesion("La sesión expiró. Inicia sesión nuevamente."),0)
                    Clock.schedule_once(lambda dt:pantalla.actualizar_datos([],mensaje),0);return
                jugadores=[]
                for fila in respuesta.get("ranking",[]):
                    jugadores.append({"posicion":int(fila.get("posicion") or len(jugadores)+1),"nombre":fila.get("nickname") or fila.get("nombre_usuario") or "Jugador","elo":int(fila.get("puntos_elo") or 0),"victorias":int(fila.get("victorias") or 0),"derrotas":int(fila.get("derrotas") or 0),"partidas_jugadas":int(fila.get("partidas_jugadas") or 0)})
                mensaje="Ranking actualizado correctamente." if jugadores else "Todavía no hay jugadores en el ranking."
                Clock.schedule_once(lambda dt:pantalla.actualizar_datos(jugadores,mensaje),0)
            except Exception as error:Clock.schedule_once(lambda dt:pantalla.actualizar_datos([],str(error)),0)
            finally:self._ranking_cargando=False
        threading.Thread(target=tarea,daemon=True).start()

    def cerrar_sesion(self,mensaje="Sesión cerrada."):
        self.token=None;self.usuario=None;self.pantalla_login.mensaje.text=mensaje;self.pantalla_login.mensaje.color=ROJO_BRILLO;self.sm.current="login"


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    GameZoneProApp().run()


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    GameZoneProApp().run()
