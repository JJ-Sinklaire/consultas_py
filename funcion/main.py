import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración del tema de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class GraficadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Generador de Funciones Lineales")
        self.geometry("800x550")
        self.minsize(800, 550)

        # --- Panel Izquierdo: Controles y Entradas ---
        self.frame_controles = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.frame_controles.pack(side="left", fill="y", padx=20, pady=20)

        self.label_titulo = ctk.CTkLabel(self.frame_controles, text="f(x) = mx + b",
                                         font=ctk.CTkFont(size=24, weight="bold"))
        self.label_titulo.pack(pady=(20, 30))

        # Entrada para la pendiente (m)
        self.label_m = ctk.CTkLabel(self.frame_controles, text="Pendiente (m):")
        self.label_m.pack(anchor="w", padx=20)
        self.entrada_m = ctk.CTkEntry(self.frame_controles, placeholder_text="Ej: 2")
        self.entrada_m.pack(fill="x", padx=20, pady=(0, 15))

        # Entrada para el término independiente (b)
        self.label_b = ctk.CTkLabel(self.frame_controles, text="Término independiente (b):")
        self.label_b.pack(anchor="w", padx=20)
        self.entrada_b = ctk.CTkEntry(self.frame_controles, placeholder_text="Ej: -5")
        self.entrada_b.pack(fill="x", padx=20, pady=(0, 20))

        # Botón para accionar la gráfica
        self.boton_graficar = ctk.CTkButton(self.frame_controles, text="Graficar", command=self.generar_grafica)
        self.boton_graficar.pack(fill="x", padx=20, pady=10)

        # Etiqueta para validación y errores
        self.label_error = ctk.CTkLabel(self.frame_controles, text="", text_color="red",
                                        font=ctk.CTkFont(weight="bold"))
        self.label_error.pack(pady=10)

        # --- Panel Derecho: Área de la Gráfica ---
        self.frame_grafica = ctk.CTkFrame(self, corner_radius=10)
        self.frame_grafica.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        # Inicialización del lienzo (canvas) de Matplotlib vacío
        self.figura, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Dibujar una gráfica vacía de inicio
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.canvas.draw()

    def generar_grafica(self):
        # 1. Extraer los datos de las entradas
        m_str = self.entrada_m.get()
        b_str = self.entrada_b.get()

        # 2. Validación: Intentar convertir a flotantes (números decimales)
        try:
            m = float(m_str)
            b = float(b_str)
            self.label_error.configure(text="")  # Limpiar mensaje de error si es correcto
        except ValueError:
            # Si no son números válidos (ej. letras o vacío), se muestra el error y se aborta
            self.label_error.configure(text="Datos incorrectos.\nIngresa solo números.")
            return

        # 3. Limpiar la gráfica anterior
        self.ax.clear()

        # 4. Generar los datos matemáticos usando numpy
        # Rango del eje x: de -10 a 10, con 100 puntos para una línea fluida
        x = np.linspace(-10, 10, 100)
        y = m * x + b  # Aplicamos la función lineal f(x) = mx + b

        # 5. Configurar y trazar la nueva gráfica
        self.ax.plot(x, y, color='blue', linestyle='-', linewidth=2, label=f'f(x) = {m}x + {b}')

        # Estética de la gráfica (Ejes, cuadrícula y leyendas)
        self.ax.axhline(0, color='black', linewidth=1)  # Eje X
        self.ax.axvline(0, color='black', linewidth=1)  # Eje Y
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.set_title("Gráfica de Función Lineal")
        self.ax.set_xlabel("Eje X")
        self.ax.set_ylabel("Eje Y")
        self.ax.legend(loc="upper left")

        # 6. Actualizar el lienzo en la interfaz gráfica
        self.canvas.draw()


# Ejecución principal de la aplicación
if __name__ == "__main__":
    app = GraficadorApp()
    app.mainloop()