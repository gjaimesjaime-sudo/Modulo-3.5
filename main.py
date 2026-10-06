# ============================================================
# GAMEZONE PRO
# PHANTOM EDITION
# Persona 5 Royal Inspired UI
# ============================================================

import customtkinter as ctk
import tkinter as tk


# ============================================================
# CONFIGURACIÓN
# ============================================================

ctk.set_appearance_mode("dark")


# ============================================================
# COLORES
# ============================================================

BLACK = "#050505"
DARK = "#0b0b0b"
DARK_2 = "#111111"

RED = "#e60012"
RED_DARK = "#a9000d"
RED_BRIGHT = "#ff1a2e"

WHITE = "#ffffff"
GRAY = "#a0a0a0"
DARK_GRAY = "#202020"


# ============================================================
# VENTANA
# ============================================================

app = ctk.CTk()

app.title("GAMEZONE PRO // PHANTOM EDITION")

app.geometry("1400x800")

app.minsize(1150, 700)

app.configure(
    fg_color=BLACK
)


# ============================================================
# CANVAS PRINCIPAL
# ============================================================

canvas = tk.Canvas(
    app,
    bg=BLACK,
    highlightthickness=0
)

canvas.pack(
    fill="both",
    expand=True
)


# ============================================================
# FONDO
# ============================================================

canvas.create_rectangle(
    0,
    0,
    2000,
    1000,
    fill=BLACK,
    outline=""
)


# ============================================================
# FORMAS ROJAS DEL FONDO
# ============================================================

canvas.create_polygon(
    900, -100,
    1500, -100,
    1150, 900,
    700, 900,
    fill=RED,
    outline=""
)

canvas.create_polygon(
    1100, -100,
    1500, -100,
    1350, 700,
    950, 700,
    fill=RED_DARK,
    outline=""
)

canvas.create_polygon(
    0, 650,
    600, 500,
    750, 800,
    0, 800,
    fill="#090909",
    outline=""
)


# ============================================================
# PANEL LATERAL
# ============================================================

sidebar = ctk.CTkFrame(
    app,
    width=280,
    fg_color="#090909",
    corner_radius=0
)

sidebar.place(
    x=0,
    y=0,
    relheight=1
)


# ============================================================
# LOGO
# ============================================================

logo_small = ctk.CTkLabel(
    sidebar,
    text="GZ",
    font=("Arial Black", 58),
    text_color=RED
)

logo_small.place(
    x=30,
    y=25
)


logo_text = ctk.CTkLabel(
    sidebar,
    text="GAMEZONE",
    font=("Arial Black", 25),
    text_color=WHITE
)

logo_text.place(
    x=105,
    y=35
)


logo_pro = ctk.CTkLabel(
    sidebar,
    text="PRO",
    font=("Arial Black", 16),
    text_color=RED
)

logo_pro.place(
    x=107,
    y=70
)


# ============================================================
# LÍNEA DECORATIVA
# ============================================================

tk.Canvas(
    sidebar,
    width=210,
    height=3,
    bg=RED,
    highlightthickness=0
).place(
    x=35,
    y=110
)


# ============================================================
# TÍTULO DEL MENÚ
# ============================================================

menu_label = ctk.CTkLabel(
    sidebar,
    text="PHANTOM MENU",
    font=("Arial Black", 13),
    text_color=GRAY
)

menu_label.place(
    x=38,
    y=145
)


# ============================================================
# FUNCIÓN VISUAL PARA BOTONES
# ============================================================

def crear_boton(
    texto,
    y,
    activo=False
):

    color = RED if activo else "#0f0f0f"

    boton = ctk.CTkButton(
        sidebar,

        text=texto,

        width=230,
        height=55,

        corner_radius=0,

        fg_color=color,

        hover_color=RED_BRIGHT,

        text_color=WHITE,

        font=("Arial Black", 15),

        anchor="w"
    )

    boton.place(
        x=25,
        y=y
    )

    return boton


# ============================================================
# BOTONES
# ============================================================

btn_inicio = crear_boton(
    "  ▶  HOME",
    185,
    True
)


btn_jugadores = crear_boton(
    "  ◆  PLAYERS",
    250
)


btn_ranking = crear_boton(
    "  ★  RANKING",
    315
)


btn_torneos = crear_boton(
    "  ▲  TOURNAMENTS",
    380
)


btn_resultados = crear_boton(
    "  ●  RESULTS",
    445
)


btn_estadisticas = crear_boton(
    "  ■  STATISTICS",
    510
)


# ============================================================
# ESTADO DEL SISTEMA
# ============================================================

system_label = ctk.CTkLabel(
    sidebar,
    text="SYSTEM STATUS",
    font=("Arial Black", 11),
    text_color=GRAY
)

system_label.place(
    x=38,
    rely=1.0,
    y=-100
)


online_label = ctk.CTkLabel(
    sidebar,
    text="●  ONLINE",
    font=("Arial Black", 13),
    text_color=RED
)

online_label.place(
    x=38,
    rely=1.0,
    y=-72
)


version_label = ctk.CTkLabel(
    sidebar,
    text="GAMEZONE PRO v1.0",
    font=("Arial", 10),
    text_color="#555555"
)

version_label.place(
    x=38,
    rely=1.0,
    y=-40
)


# ============================================================
# CONTENIDO PRINCIPAL
# ============================================================

content = ctk.CTkFrame(
    app,
    fg_color="transparent",
    corner_radius=0
)

content.place(
    x=280,
    y=0,
    relwidth=1,
    relheight=1
)


# ============================================================
# TEXTO SUPERIOR
# ============================================================

small_title = ctk.CTkLabel(
    content,
    text="WELCOME BACK, PLAYER",
    font=("Arial Black", 15),
    text_color=WHITE
)

small_title.place(
    x=55,
    y=40
)


# ============================================================
# TÍTULO PRINCIPAL
# ============================================================

main_title = ctk.CTkLabel(
    content,
    text="GAMEZONE",
    font=("Arial Black", 72),
    text_color=WHITE
)

main_title.place(
    x=45,
    y=75
)


main_title_2 = ctk.CTkLabel(
    content,
    text="PRO",
    font=("Arial Black", 75),
    text_color=RED
)

main_title_2.place(
    x=50,
    y=145
)


# ============================================================
# FRASE
# ============================================================

tagline = ctk.CTkLabel(
    content,
    text="YOUR BATTLE. YOUR RANK. YOUR LEGACY.",
    font=("Arial Black", 13),
    text_color=WHITE
)

tagline.place(
    x=58,
    y=245
)


# ============================================================
# RIBBON
# ============================================================

ribbon = ctk.CTkFrame(
    content,
    width=360,
    height=45,
    fg_color=RED,
    corner_radius=0
)

ribbon.place(
    x=55,
    y=285
)


ribbon_label = ctk.CTkLabel(
    ribbon,
    text="PHANTOM LEAGUE // MAIN HUB",
    font=("Arial Black", 12),
    text_color=WHITE
)

ribbon_label.pack(
    expand=True
)


# ============================================================
# TARJETA PLAYERS
# ============================================================

player_card = ctk.CTkFrame(
    content,
    width=240,
    height=170,
    fg_color="#111111",
    border_width=2,
    border_color=WHITE,
    corner_radius=0
)

player_card.place(
    x=55,
    y=355
)


ctk.CTkLabel(
    player_card,
    text="PLAYERS",
    font=("Arial Black", 15),
    text_color=RED
).place(
    x=20,
    y=18
)


ctk.CTkLabel(
    player_card,
    text="000",
    font=("Arial Black", 48),
    text_color=WHITE
).place(
    x=18,
    y=48
)


ctk.CTkLabel(
    player_card,
    text="REGISTERED PLAYERS",
    font=("Arial", 10),
    text_color=GRAY
).place(
    x=20,
    y=125
)


# ============================================================
# TARJETA RANKING
# ============================================================

ranking_card = ctk.CTkFrame(
    content,
    width=240,
    height=170,
    fg_color=RED,
    corner_radius=0
)

ranking_card.place(
    x=315,
    y=355
)


ctk.CTkLabel(
    ranking_card,
    text="RANKING",
    font=("Arial Black", 15),
    text_color=BLACK
).place(
    x=20,
    y=18
)


ctk.CTkLabel(
    ranking_card,
    text="#01",
    font=("Arial Black", 48),
    text_color=WHITE
).place(
    x=18,
    y=48
)


ctk.CTkLabel(
    ranking_card,
    text="CURRENT CHAMPION",
    font=("Arial", 10),
    text_color=BLACK
).place(
    x=20,
    y=125
)


# ============================================================
# TARJETA TORNEOS
# ============================================================

tournament_card = ctk.CTkFrame(
    content,
    width=240,
    height=170,
    fg_color="#111111",
    border_width=2,
    border_color=WHITE,
    corner_radius=0
)

tournament_card.place(
    x=575,
    y=355
)


ctk.CTkLabel(
    tournament_card,
    text="TOURNAMENTS",
    font=("Arial Black", 15),
    text_color=RED
).place(
    x=20,
    y=18
)


ctk.CTkLabel(
    tournament_card,
    text="000",
    font=("Arial Black", 48),
    text_color=WHITE
).place(
    x=18,
    y=48
)


ctk.CTkLabel(
    tournament_card,
    text="ACTIVE EVENTS",
    font=("Arial", 10),
    text_color=GRAY
).place(
    x=20,
    y=125
)


# ============================================================
# ACTIVIDAD
# ============================================================

activity = ctk.CTkFrame(
    content,
    width=500,
    height=170,
    fg_color="#080808",
    border_width=2,
    border_color=RED,
    corner_radius=0
)

activity.place(
    x=835,
    y=355
)


ctk.CTkLabel(
    activity,
    text="RECENT ACTIVITY",
    font=("Arial Black", 17),
    text_color=WHITE
).place(
    x=25,
    y=20
)


ctk.CTkLabel(
    activity,
    text="NO RECENT MATCHES",
    font=("Arial Black", 13),
    text_color=RED
).place(
    x=25,
    y=65
)


ctk.CTkLabel(
    activity,
    text="SYSTEM WAITING FOR DATA...",
    font=("Arial", 11),
    text_color=GRAY
).place(
    x=25,
    y=100
)


# ============================================================
# ELEMENTO DECORATIVO
# ============================================================

decorative = ctk.CTkLabel(
    content,
    text="01",
    font=("Arial Black", 110),
    text_color="#171717"
)

decorative.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-40,
    y=-5
)


# ============================================================
# BARRA INFERIOR
# ============================================================

bottom_bar = ctk.CTkFrame(
    content,
    height=35,
    fg_color="#0d0d0d",
    corner_radius=0
)

bottom_bar.place(
    x=0,
    rely=1.0,
    relwidth=1,
    y=-35
)


ctk.CTkLabel(
    bottom_bar,
    text="GAMEZONE PRO // PHANTOM EDITION",
    font=("Arial Black", 10),
    text_color=GRAY
).pack(
    side="left",
    padx=20
)


ctk.CTkLabel(
    bottom_bar,
    text="SYSTEM READY",
    font=("Arial Black", 10),
    text_color=RED
).pack(
    side="right",
    padx=20
)


# ============================================================
# EJECUCIÓN
# ============================================================

app.mainloop()