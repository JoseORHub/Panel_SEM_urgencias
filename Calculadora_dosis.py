import tkinter as tk
from tkinter import messagebox

# --- CONSTANTES ---
COLOR_PRINCIPAL  = "#0033A0"
COLOR_SECUNDARIO = "#007BFF"
GRIS_TEXTO       = "#4A4A4A"
GRIS_SUAVE       = "#CCCCCC"
FONDO            = "#FFFFFF"
DOSIS_FACTOR     = 0.1          # mL por kg — cambiar aquí si cambia el protocolo


# ---------------------------------------------------------------------------
# LÓGICA DE NEGOCIO (pura, sin dependencias de UI → fácil de testear)
# ---------------------------------------------------------------------------

def calcular_dosis_ml(peso_kg: float) -> float:
    """Devuelve la dosis en mL. Lanza ValueError si el peso no es válido."""
    if peso_kg <= 0:
        raise ValueError(f"El peso debe ser mayor que 0, recibido: {peso_kg}")
    return round(peso_kg * DOSIS_FACTOR, 2)


# ---------------------------------------------------------------------------
# APLICACIÓN (toda la UI encapsulada en una clase)
# ---------------------------------------------------------------------------

class CalculadoraAntirrabica(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora vacuna antirrábica")
        self.geometry("450x450")
        self.resizable(False, False)
        self.config(bg=FONDO)

        self._build_ui()
        self._set_modo_calcular()        # estado inicial

    # ------------------------------------------------------------------
    # Construcción de la UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        contenido = tk.Frame(self, bg=FONDO)
        contenido.pack(fill="both", expand=True)

        tk.Label(
            contenido,
            text="Calculadora dosis antirrábica",
            bg=FONDO, fg=COLOR_PRINCIPAL,
            font=("Arial", 14, "bold"),
        ).pack(pady=(20, 10))

        card = tk.Frame(contenido, bg=FONDO)
        card.pack(padx=30, pady=10, fill="both", expand=True)

        tk.Label(
            card,
            text="Peso del paciente (kg)",
            bg=FONDO, fg=GRIS_TEXTO,
            font=("Arial", 11),
        ).pack(pady=(10, 5))

        self.entry_peso = tk.Entry(
            card, font=("Arial", 11), justify="center", bd=1
        )
        self.entry_peso.pack(fill="x", ipady=6, pady=5)
        self.entry_peso.focus()

        self.btn_calcular = tk.Button(
            card,
            text="Calcular",
            font=("Arial", 11, "bold"),
            bg=COLOR_PRINCIPAL, fg="white",
            activebackground=COLOR_SECUNDARIO,
            relief="flat", pady=10,
            command=self._on_calcular,
        )
        self.btn_calcular.pack(fill="x", pady=20)

        self.btn_reiniciar = tk.Button(
            card,
            text="Nuevo cálculo",
            font=("Arial", 10),
            bg=FONDO, fg=COLOR_PRINCIPAL,
            relief="flat",
            command=self._on_reiniciar,
        )
        self.btn_reiniciar.pack()

        # Panel de resultado (oculto al inicio)
        self.frame_resultado = tk.Frame(contenido, bg=FONDO)
        self.lbl_resultado_texto = tk.Label(
            self.frame_resultado, text="", bg=FONDO,
            fg=GRIS_TEXTO, font=("Arial", 10),
        )
        self.lbl_resultado_texto.pack()
        self.lbl_resultado_valor = tk.Label(
            self.frame_resultado, text="", bg=FONDO,
            fg="black", font=("Arial", 26, "bold"),
        )
        self.lbl_resultado_valor.pack()
        self.lbl_resultado_unidad = tk.Label(
            self.frame_resultado, text="", bg=FONDO,
            fg=GRIS_TEXTO, font=("Arial", 11),
        )
        self.lbl_resultado_unidad.pack()

        tk.Label(
            self,
            text="Uso clínico referencial SURA® 2026",
            bg=FONDO, fg=GRIS_TEXTO, font=("Arial", 8),
        ).pack(side="bottom", pady=10)

    # ------------------------------------------------------------------
    # Gestión de estado (un único bind de <Return> que delega)
    # ------------------------------------------------------------------

    def _on_return(self, event=None):
        """Delegador de Enter según el estado actual."""
        if str(self.btn_calcular["state"]) == "normal":
            self._on_calcular()
        else:
            self._on_reiniciar()

    def _set_modo_calcular(self):
        """Activa el modo 'listo para calcular'."""
        self.entry_peso.config(state="normal")
        self.btn_calcular.config(state="normal", fg="white", cursor="hand2")
        self.btn_reiniciar.config(state="disabled", cursor="arrow")
        self.frame_resultado.pack_forget()
        # Un solo bind estable — _on_return decide qué hacer
        self.bind("<Return>", self._on_return)

    def _set_modo_resultado(self):
        """Activa el modo 'resultado visible'."""
        self.entry_peso.config(state="disabled")
        self.btn_calcular.config(state="disabled", fg=GRIS_SUAVE, cursor="arrow")
        self.btn_reiniciar.config(state="normal", cursor="hand2")
        self.frame_resultado.pack(pady=15)

    # ------------------------------------------------------------------
    # Manejadores de eventos
    # ------------------------------------------------------------------

    def _on_calcular(self, event=None):
        try:
            peso = float(self.entry_peso.get())
            dosis = calcular_dosis_ml(peso)          # lógica pura separada
        except ValueError:
            messagebox.showerror(
                "Error",
                "Ingrese un peso válido en kg.\nUse punto (.) para decimales.",
            )
            return

        self.lbl_resultado_valor.config(text=f"{dosis:.2f}")
        self.lbl_resultado_unidad.config(text="mL")
        self.lbl_resultado_texto.config(text="Dosis recomendada")
        self._set_modo_resultado()

    def _on_reiniciar(self, event=None):
        self.entry_peso.config(state="normal")  # habilitar antes de modificar
        self.entry_peso.delete(0, tk.END)
        self.entry_peso.focus()
        self._set_modo_calcular()


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = CalculadoraAntirrabica()
    app.mainloop()