import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.styles import *

try:
    df = pd.read_csv("datos.csv")
except Exception:
    df = pd.DataFrame()


def _make_layout(frame, titulo, descripcion):
    """Crea el layout izq/der neobrutalist y devuelve (izq, der, lbl_status)."""
    izq = ctk.CTkFrame(frame, fg_color="transparent")
    izq.pack(side="left", fill="both", expand=False, padx=(18, 8), pady=18, ipadx=4)
    izq.configure(width=220)

    # Panel der con borde grueso
    der_wrap = ctk.CTkFrame(frame, fg_color=BORDER, corner_radius=0)
    der_wrap.pack(side="right", fill="both", expand=True, padx=(8, 18), pady=18)

    der = ctk.CTkFrame(der_wrap, fg_color=PANEL_BG, corner_radius=0)
    der.pack(fill="both", expand=True, padx=3, pady=3)

    # Tag
    tag = ctk.CTkFrame(izq, fg_color=BTN_BG, corner_radius=0, height=22)
    tag.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(tag, text="▶  CONSULTA 01", font=FONT_LABEL, text_color=BTN_TXT).pack(side="left", padx=8, pady=2)

    ctk.CTkLabel(izq, text=titulo, font=FONT_TITLE, text_color=TEXT,
                 wraplength=200, justify="left").pack(anchor="w", pady=(0, 6))

    # Separador
    ctk.CTkFrame(izq, fg_color=BORDER, height=3, corner_radius=0).pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(izq, text=descripcion, font=FONT_BODY, text_color=SUBTEXT,
                 wraplength=200, justify="left").pack(anchor="w", pady=(0, 14))

    lbl_status = ctk.CTkLabel(izq, text="", font=FONT_STATUS, text_color=SUCCESS_TXT, wraplength=200)
    lbl_status.pack(anchor="w", pady=(0, 12))

    return izq, der, lbl_status


def buildC1(frame):
    izq, der, lbl_status = _make_layout(
        frame,
        "TOP 10\nCIUDADES",
        "Ciudades con mayor número de propiedades vendidas en el dataset."
    )

    def ejecutar():
        if df.empty:
            lbl_status.configure(text="! CSV no cargado", text_color=ERROR_TXT)
            return
        for w in der.winfo_children():
            w.destroy()

        conteo = df["city"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(6, 4.5), facecolor=MPL_BG)
        ax.set_facecolor(MPL_BG)
        bars = ax.bar(conteo.index, conteo.values, color=COLORS[0], edgecolor=BORDER, linewidth=1.5)

        ax.set_title("Top 10 ciudades con más propiedades", color=MPL_TEXT, fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Ciudad", color=MPL_TEXT, fontsize=9)
        ax.set_ylabel("Cantidad", color=MPL_TEXT, fontsize=9)
        ax.tick_params(colors=MPL_TEXT, labelsize=7)
        ax.set_xticklabels(conteo.index, rotation=35, ha="right")
        ax.spines[:].set_color(BORDER)
        ax.spines[:].set_linewidth(1.5)
        ax.yaxis.grid(True, color=MPL_GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=der)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)
        lbl_status.configure(text="✔ gráfica generada con éxito", text_color=SUCCESS_TXT)

    ctk.CTkButton(
        izq, text="→  EJECUTAR", height=42, corner_radius=0,
        fg_color=BTN_BG, hover_color=BTN_HOVER, text_color=BTN_TXT,
        font=FONT_BTN, command=ejecutar
    ).pack(fill="x", pady=(4, 0))