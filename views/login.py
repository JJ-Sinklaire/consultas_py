import json
import customtkinter as ctk
from pathlib import Path
from views.hub import showHub

# ── Paleta Neobrutalist ──────────────────────────────────────────
BG          = "#F0EC3C"   # amarillo principal
PANEL       = "#FFFFFF"   # blanco para el card
BORDER      = "#111111"   # negro duro
TEXT        = "#111111"
SUBTEXT     = "#555555"
ACCENT      = "#111111"   # botón negro
ACCENT_TXT  = "#F0EC3C"   # texto amarillo sobre botón
ERROR       = "#CC0000"
ENTRY_BG    = "#FFFFFF"

FONT_TITLE  = ("Syne", 28, "bold")
FONT_LABEL  = ("DM Mono", 10, "bold")
FONT_BODY   = ("DM Mono", 13)
FONT_BTN    = ("Syne", 13, "bold")
FONT_ERR    = ("DM Mono", 11)
FONT_FOOT   = ("DM Mono", 9)

usersFilePath = Path(__file__).parent.parent / "users.json"


def validateUser(username, password):
    if not usersFilePath.exists():
        return None
    with open(usersFilePath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for user in data.get("users", []):
        if user["username"] == username and user["password"] == password:
            return user
    return None


def showLogin():
    win = ctk.CTk()
    win.title("Consultas IA")
    win.geometry("460x520")
    win.resizable(False, False)
    win.configure(fg_color=BG)

    # ── Card principal ───────────────────────────────────────────
    card = ctk.CTkFrame(
        win, fg_color=PANEL,
        corner_radius=0,
        border_width=3, border_color=BORDER
    )
    card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.84, relheight=0.88)

    # Sombra desplazada (frame decorativo negro detrás)
    shadow = ctk.CTkFrame(win, fg_color=BORDER, corner_radius=0)
    shadow.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.84, relheight=0.88)
    shadow.lower()
    card.lift()
    # Desplazamos el shadow manualmente
    card.place(relx=0.5, rely=0.49, anchor="center", relwidth=0.84, relheight=0.88)
    shadow.place(relx=0.513, rely=0.503, anchor="center", relwidth=0.84, relheight=0.88)

    # ── Tag superior ─────────────────────────────────────────────
    tag = ctk.CTkFrame(card, fg_color=BORDER, corner_radius=0, height=28)
    tag.place(relx=0.08, rely=0.07, relwidth=0.52)
    ctk.CTkLabel(
        tag, text="▶  ACCESO AL SISTEMA",
        font=FONT_LABEL, text_color=ACCENT_TXT
    ).place(relx=0.08, rely=0.5, anchor="w")

    # ── Título ───────────────────────────────────────────────────
    ctk.CTkLabel(
        card, text="CONSULTAS", font=FONT_TITLE, text_color=TEXT
    ).place(relx=0.08, rely=0.195, anchor="w")

    ctk.CTkLabel(
        card, text="IA", font=("Syne", 28, "bold"), text_color=BORDER
    ).place(relx=0.73, rely=0.195, anchor="w")

    ctk.CTkLabel(
        card, text="Identifíquese para continuar",
        font=("DM Mono", 10), text_color=SUBTEXT
    ).place(relx=0.08, rely=0.27, anchor="w")

    # ── Separador ────────────────────────────────────────────────
    sep = ctk.CTkFrame(card, fg_color=BORDER, height=3, corner_radius=0)
    sep.place(relx=0.08, rely=0.33, relwidth=0.84)

    # ── Label + Entry: Usuario ───────────────────────────────────
    ctk.CTkLabel(
        card, text="USUARIO", font=FONT_LABEL, text_color=TEXT
    ).place(relx=0.08, rely=0.40, anchor="w")

    entryUser = ctk.CTkEntry(
        card, placeholder_text="tu_usuario",
        height=40, corner_radius=0,
        fg_color=ENTRY_BG, text_color=TEXT,
        border_width=2, border_color=BORDER,
        font=FONT_BODY
    )
    entryUser.place(relx=0.08, rely=0.47, relwidth=0.84)

    # ── Label + Entry: Contraseña ─────────────────────────────────
    ctk.CTkLabel(
        card, text="CONTRASEÑA", font=FONT_LABEL, text_color=TEXT
    ).place(relx=0.08, rely=0.575, anchor="w")

    entryPass = ctk.CTkEntry(
        card, placeholder_text="••••••••••",
        show="●", height=40, corner_radius=0,
        fg_color=ENTRY_BG, text_color=TEXT,
        border_width=2, border_color=BORDER,
        font=FONT_BODY
    )
    entryPass.place(relx=0.08, rely=0.645, relwidth=0.84)

    # ── Error ─────────────────────────────────────────────────────
    lblError = ctk.CTkLabel(
        card, text="", font=FONT_ERR, text_color=ERROR
    )
    lblError.place(relx=0.08, rely=0.75, anchor="w")

    # ── Botón ─────────────────────────────────────────────────────
    def onLogin():
        u, p = entryUser.get().strip(), entryPass.get().strip()
        if not u or not p:
            lblError.configure(text="! campos requeridos vacíos")
            return
        userData = validateUser(u, p)
        if userData:
            win.destroy()
            showHub(userData)
        else:
            lblError.configure(text="! credenciales incorrectas")

    btn = ctk.CTkButton(
        card, text="→  ENTRAR",
        height=44, corner_radius=0,
        fg_color=ACCENT, hover_color="#333333",
        text_color=ACCENT_TXT, font=FONT_BTN,
        command=onLogin
    )
    btn.place(relx=0.08, rely=0.855, relwidth=0.84)

    # ── Pie ───────────────────────────────────────────────────────
    ctk.CTkLabel(
        card, text="// sistema cifrado · solo acceso autorizado",
        font=FONT_FOOT, text_color=SUBTEXT
    ).place(relx=0.5, rely=0.95, anchor="center")

    win.bind("<Return>", lambda e: onLogin())
    win.mainloop()