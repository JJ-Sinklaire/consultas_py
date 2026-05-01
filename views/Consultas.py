import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.styles import *

try:
    df = pd.read_csv("datos.csv")
except Exception:
    df = pd.DataFrame()


def _layout(frame, num_str, titulo, descripcion):
    izq = ctk.CTkFrame(frame, fg_color="transparent")
    izq.pack(side="left", fill="both", expand=False, padx=(18, 8), pady=18)
    izq.configure(width=220)

    der_wrap = ctk.CTkFrame(frame, fg_color=BORDER, corner_radius=0)
    der_wrap.pack(side="right", fill="both", expand=True, padx=(8, 18), pady=18)
    der = ctk.CTkFrame(der_wrap, fg_color=PANEL_BG, corner_radius=0)
    der.pack(fill="both", expand=True, padx=3, pady=3)

    tag = ctk.CTkFrame(izq, fg_color=BTN_BG, corner_radius=0, height=22)
    tag.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(tag, text=f"▶  CONSULTA {num_str}", font=FONT_LABEL, text_color=BTN_TXT).pack(side="left", padx=8, pady=2)

    ctk.CTkLabel(izq, text=titulo, font=FONT_TITLE, text_color=TEXT, wraplength=200, justify="left").pack(anchor="w", pady=(0, 6))
    ctk.CTkFrame(izq, fg_color=BORDER, height=3, corner_radius=0).pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(izq, text=descripcion, font=FONT_BODY, text_color=SUBTEXT, wraplength=200, justify="left").pack(anchor="w", pady=(0, 14))

    lbl = ctk.CTkLabel(izq, text="", font=FONT_STATUS, text_color=SUCCESS_TXT, wraplength=200)
    lbl.pack(anchor="w", pady=(0, 12))
    return izq, der, lbl


def _btn(izq, cmd):
    ctk.CTkButton(
        izq, text="→  EJECUTAR", height=42, corner_radius=0,
        fg_color=BTN_BG, hover_color=BTN_HOVER, text_color=BTN_TXT,
        font=FONT_BTN, command=cmd
    ).pack(fill="x", pady=(4, 0))


def _apply_mpl_style(ax, title, xlabel, ylabel):
    ax.set_facecolor(MPL_BG)
    ax.set_title(title, color=MPL_TEXT, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, color=MPL_TEXT, fontsize=9)
    ax.set_ylabel(ylabel, color=MPL_TEXT, fontsize=9)
    ax.tick_params(colors=MPL_TEXT, labelsize=7)
    ax.spines[:].set_color(BORDER)
    ax.spines[:].set_linewidth(1.5)
    ax.yaxis.grid(True, color=MPL_GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _embed(fig, der):
    canvas = FigureCanvasTkAgg(fig, master=der)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)


# ── Consulta 02: Tamaño vs Precio ───────────────────────────────
def buildC2(frame):
    izq, der, lbl = _layout(frame, "02", "TAMAÑO\nVS PRECIO",
                             "Correlación entre pies cuadrados y precio de venta.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        datos = df.query("sq__ft > 0")
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.scatter(datos["sq__ft"], datos["price"], color=COLORS[1],
                   alpha=0.6, edgecolors=BORDER, linewidths=0.4, s=18)
        _apply_mpl_style(ax, "Pies cuadrados vs Precio", "Pies Cuadrados", "Precio ($)")
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada con éxito", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 03: Distribución de Precios ────────────────────────
def buildC3(frame):
    izq, der, lbl = _layout(frame, "03", "DISTRIBUCIÓN\nDE PRECIOS",
                             "Histograma de frecuencias de los precios de venta.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.hist(df["price"].dropna(), bins=30, color=COLORS[2],
                edgecolor=BORDER, linewidth=1)
        _apply_mpl_style(ax, "Frecuencia de precios en el mercado", "Precio ($)", "Frecuencia")
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ histograma generado", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 04: Tipos de Propiedad ─────────────────────────────
def buildC4(frame):
    izq, der, lbl = _layout(frame, "04", "TIPOS DE\nPROPIEDAD",
                             "Distribución porcentual por categoría de propiedad.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        conteo = df["type"].value_counts()
        pie_colors = ["#111111", "#E05A1A", "#1A4D8B", "#8B1A1A"]
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        wedges, texts, autotexts = ax.pie(
            conteo.values, labels=conteo.index, autopct="%1.1f%%",
            startangle=90, colors=pie_colors,
            textprops={"color": MPL_TEXT, "fontsize": 8},
            wedgeprops={"edgecolor": BORDER, "linewidth": 2}
        )
        for at in autotexts:
            at.set_color("#F0EC3C")
            at.set_fontweight("bold")
        ax.set_title("Distribución por tipo de propiedad", color=MPL_TEXT,
                     fontsize=11, fontweight="bold", pad=10)
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfico generado", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 05: Precio por Habitaciones ────────────────────────
def buildC5(frame):
    izq, der, lbl = _layout(frame, "05", "PRECIO POR\nHABITACIONES",
                             "Precio promedio de venta según número de dormitorios.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        promedios = df.query("beds > 0").groupby("beds")["price"].mean()
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.bar(promedios.index.astype(str), promedios.values,
               color=COLORS[4], edgecolor=BORDER, linewidth=1.5)
        _apply_mpl_style(ax, "Precio promedio vs número de habitaciones",
                         "Habitaciones", "Precio promedio ($)")
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 06: Zonas Más Caras ────────────────────────────────
def buildC6(frame):
    izq, der, lbl = _layout(frame, "06", "ZONAS\nMÁS CARAS",
                             "Top 5 códigos postales con mayor precio promedio de venta.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        top_zips = df.groupby("zip")["price"].mean().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.barh(top_zips.index.astype(str), top_zips.values,
                color=COLORS[5], edgecolor=BORDER, linewidth=1.5)
        _apply_mpl_style(ax, "Top 5 códigos postales más caros",
                         "Precio promedio ($)", "Código Postal")
        ax.xaxis.grid(True, color=MPL_GRID, linewidth=0.8)
        ax.yaxis.grid(False)
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 07: Distribución de Baños ──────────────────────────
def buildC7(frame):
    izq, der, lbl = _layout(frame, "07", "DISTRIBUCIÓN\nDE BAÑOS",
                             "Cantidad de propiedades agrupadas por número de baños.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        conteo = df["baths"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.bar(conteo.index.astype(str), conteo.values,
               color=COLORS[6], edgecolor="#F0EC3C", linewidth=2)
        _apply_mpl_style(ax, "Propiedades según cantidad de baños",
                         "Número de baños", "Cantidad")
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 08: Tamaño por Tipo ────────────────────────────────
def buildC8(frame):
    izq, der, lbl = _layout(frame, "08", "TAMAÑO\nPOR TIPO",
                             "Espacio promedio en pies cuadrados según el tipo de propiedad.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        tamano = df.groupby("type")["sq__ft"].mean()
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.bar(tamano.index, tamano.values,
               color=COLORS[7], edgecolor=BORDER, linewidth=1.5)
        _apply_mpl_style(ax, "Tamaño promedio por tipo de propiedad",
                         "Tipo de propiedad", "Pies cuadrados")
        ax.set_xticklabels(tamano.index, rotation=15, ha="right")
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 09: Calles Populares ───────────────────────────────
def buildC9(frame):
    izq, der, lbl = _layout(frame, "09", "CALLES\nPOPULARES",
                             "Top 10 calles con mayor número de propiedades en venta.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        df_copy = df.copy()
        df_copy["street_name"] = df_copy["street"].str.split(" ", n=1).str[1]
        calles = df_copy["street_name"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.bar(calles.index, calles.values,
               color=COLORS[8], edgecolor=BORDER, linewidth=1.5)
        _apply_mpl_style(ax, "Top 10 calles con más propiedades",
                         "Nombre de calle", "Cantidad")
        ax.set_xticklabels(calles.index, rotation=40, ha="right", fontsize=6)
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)


# ── Consulta 10: Ciudades con Casas Grandes ──────────────────────
def buildC10(frame):
    izq, der, lbl = _layout(frame, "10", "CASAS\nGRANDES",
                             "Top 5 ciudades con mayor promedio de espacio en pies cuadrados.")

    def ejecutar():
        if df.empty: return
        for w in der.winfo_children(): w.destroy()
        ciudades = df.query("sq__ft > 0").groupby("city")["sq__ft"].mean()\
                     .sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.barh(ciudades.index, ciudades.values,
                color=COLORS[9], edgecolor=BORDER, linewidth=1.5)
        _apply_mpl_style(ax, "Top 5 ciudades con casas más grandes",
                         "Pies cuadrados promedio", "Ciudad")
        ax.xaxis.grid(True, color=MPL_GRID, linewidth=0.8)
        ax.yaxis.grid(False)
        fig.tight_layout()
        _embed(fig, der)
        lbl.configure(text="✔ gráfica generada", text_color=SUCCESS_TXT)

    _btn(izq, ejecutar)