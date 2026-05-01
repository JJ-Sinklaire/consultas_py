import customtkinter as ctk
from views.Consulta01 import buildC1
from views.Consultas import buildC2, buildC3,buildC4,buildC5,buildC6,buildC7,buildC8,buildC9,buildC10
# ── Paleta Neobrutalist ──────────────────────────────────────────
BG          = "#F0EC3C"
TOPBAR_BG   = "#111111"
TOPBAR_TXT  = "#F0EC3C"
TAB_SEL     = "#111111"
TEXT        = "#111111"

FONT_TOP    = ("DM Mono", 11)
FONT_USER   = ("Syne", 12, "bold")

TAB_LABELS   = [f"Consulta {i:02d}" for i in range(1, 11)]
TAB_BUILDERS = [buildC1, buildC2, buildC3, buildC4, buildC5,
                buildC6, buildC7, buildC8, buildC9, buildC10]


def showHub(userData):
    win = ctk.CTk()
    win.title("Panel de Consultas CSV")
    win.geometry("1150x700")
    win.configure(fg_color=BG)

    # ── Topbar ───────────────────────────────────────────────────
    topbar = ctk.CTkFrame(win, height=52, fg_color=TOPBAR_BG, corner_radius=0)
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)

    ctk.CTkLabel(
        topbar, text="▶  CONSULTAS IA",
        font=("Syne", 14, "bold"), text_color=TOPBAR_TXT
    ).place(x=20, rely=0.5, anchor="w")

    ctk.CTkLabel(
        topbar, text=f"// usuario: {userData['name'].upper()}",
        font=FONT_TOP, text_color="#888888"
    ).place(relx=0.98, rely=0.5, anchor="e")

    # ── Borde inferior topbar (decorativo) ───────────────────────
    accent_bar = ctk.CTkFrame(win, height=4, fg_color="#F0EC3C", corner_radius=0)
    accent_bar.pack(side="top", fill="x")

    # ── TabView ──────────────────────────────────────────────────
    tabView = ctk.CTkTabview(
        win,
        fg_color="#FFFFFF",
        segmented_button_fg_color="#111111",
        segmented_button_selected_color="#F0EC3C",
        segmented_button_selected_hover_color="#d4d020",
        segmented_button_unselected_color="#111111",
        segmented_button_unselected_hover_color="#333333",
        text_color="#F0EC3C",
        text_color_disabled="#888888",
        border_width=3,
        border_color="#111111",
        corner_radius=0
    )
    tabView.pack(fill="both", expand=True, padx=14, pady=14)

    for i, label in enumerate(TAB_LABELS):
        tabView.add(label)
        TAB_BUILDERS[i](tabView.tab(label))

    win.mainloop()