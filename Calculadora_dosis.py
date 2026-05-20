"""
Calculadora de dosis de vacuna antirrábica — SURA® 2026
==========================================================
Estructura:
  1. Constantes (diseño y protocolo)
  2. Lógica de negocio (pura, sin dependencias de UI)
  3. Configuración de página y estilos
  4. Construcción de la UI
  5. Manejo de eventos
"""

import streamlit as st


# ===========================================================================
# 1. CONSTANTES
# ===========================================================================

# -- Colores corporativos SURA --
AZUL_SURA        = "#2D6DF6"   # Pantone 2727 C · RGB 45 109 246
AZUL_SURA_HOVER  = "#1A56D6"   # Variante oscura para hover
AZUL_OSCURO      = "#0033A0"   # Azul oscuro para títulos
GRIS_TEXTO       = "#4A4A4A"
GRIS_SUAVE       = "#CCCCCC"
BLANCO           = "#FFFFFF"

# -- Protocolo clínico --
DOSIS_FACTOR_ML_POR_KG: float = 0.1   # mL por kg — actualizar aquí si cambia el protocolo


# ===========================================================================
# 2. LÓGICA DE NEGOCIO  (sin dependencias de Streamlit → fácil de testear)
# ===========================================================================

def calcular_dosis_ml(peso_kg: float) -> float:
    """
    Calcula la dosis en mL según el peso del paciente.

    Args:
        peso_kg: Peso del paciente en kilogramos. Debe ser > 0.

    Returns:
        Dosis redondeada a 2 decimales en mL.

    Raises:
        ValueError: Si el peso no es un número positivo.
    """
    if peso_kg <= 0:
        raise ValueError(f"El peso debe ser mayor que 0 kg (recibido: {peso_kg})")
    return round(peso_kg * DOSIS_FACTOR_ML_POR_KG, 2)


def parsear_peso(texto: str) -> float:
    """
    Convierte el texto ingresado por el usuario a float.

    Raises:
        ValueError: Si el texto no representa un número válido.
    """
    texto = texto.strip().replace(",", ".")   # acepta coma o punto decimal
    if not texto:
        raise ValueError("El campo de peso está vacío.")
    return float(texto)


# ===========================================================================
# 3. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ===========================================================================

st.set_page_config(
    page_title="Calculadora vacuna antirrábica",
    layout="centered",
)

CSS = f"""
<style>
  /* ── Tipografía base ── */
  html, body, [class*="css"] {{
    font-family: Arial, sans-serif !important;
  }}

  /* ── Fondo de la app ── */
  .stApp {{
    background-color: {BLANCO};
  }}

  /* ── Ancho máximo similar a la ventana original (450 px) ── */
  .main .block-container {{
    max-width: 450px;
    padding-top: 20px;
    padding-bottom: 10px;
  }}

  /* ── Título principal ── */
  .titulo {{
    color: {AZUL_OSCURO};
    font-size: 14pt;
    font-weight: 700;
    text-align: center;
    margin: 20px 0 10px 0;
  }}

  /* ── Etiqueta sobre el input ── */
  .label {{
    color: {GRIS_TEXTO};
    font-size: 11pt;
    text-align: center;
    margin: 10px 0 5px 0;
  }}

  /* ── Input centrado ── */
  input {{
    text-align: center !important;
    font-size: 11pt !important;
    padding: 10px !important;
  }}

  /* ── Botón principal: AZUL SURA ── */
  .stButton > button[kind="primary"],
  div[data-testid="stFormSubmitButton"] > button {{
    background-color: {AZUL_SURA} !important;
    color: {BLANCO} !important;
    border: none !important;
    padding: 12px 10px !important;
    font-weight: 700 !important;
    font-size: 11pt !important;
    width: 100% !important;
    border-radius: 4px !important;
    transition: background-color 0.2s ease !important;
  }}
  div[data-testid="stFormSubmitButton"] > button:hover {{
    background-color: {AZUL_SURA_HOVER} !important;
    color: {BLANCO} !important;
  }}
  div[data-testid="stFormSubmitButton"] > button:disabled {{
    background-color: {GRIS_SUAVE} !important;
    color: {BLANCO} !important;
    cursor: not-allowed !important;
  }}

  /* ── Botón secundario: "Nuevo cálculo" (plano, sin borde) ── */
  .stButton > button[kind="secondary"] {{
    background-color: {BLANCO} !important;
    color: {AZUL_SURA} !important;
    border: none !important;
    font-size: 10pt !important;
    padding: 10px !important;
    width: 100% !important;
  }}
  .stButton > button[kind="secondary"]:disabled {{
    color: {GRIS_SUAVE} !important;
  }}

  /* ── Panel de resultado ── */
  .resultado-etiqueta {{
    color: {GRIS_TEXTO};
    font-size: 10pt;
    text-align: center;
    margin-top: 15px;
  }}
  .resultado-valor {{
    color: #000000;
    font-size: 26pt;
    font-weight: 800;
    text-align: center;
    margin: 0;
    line-height: 1.1;
  }}
  .resultado-unidad {{
    color: {GRIS_TEXTO};
    font-size: 11pt;
    text-align: center;
    margin-top: 0;
  }}

  /* ── Pie de página ── */
  .footer {{
    color: {GRIS_TEXTO};
    font-size: 8pt;
    text-align: center;
    margin-top: 10px;
    padding-bottom: 10px;
  }}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ===========================================================================
# 4. ESTADO DE LA SESIÓN  (inicialización segura con .setdefault)
# ===========================================================================

st.session_state.setdefault("modo_resultado", False)
st.session_state.setdefault("peso_txt", "")
st.session_state.setdefault("dosis", None)


# ===========================================================================
# 5. CONSTRUCCIÓN DE LA UI
# ===========================================================================

st.markdown('<div class="titulo">Calculadora dosis antirrábica</div>', unsafe_allow_html=True)
st.markdown('<div class="label">Peso del paciente (kg)</div>', unsafe_allow_html=True)

# Formulario: permite enviar con la tecla Enter
with st.form("form_calculo", clear_on_submit=False):
    peso_txt = st.text_input(
        label="Peso del paciente",
        value=st.session_state.peso_txt,
        disabled=st.session_state.modo_resultado,
        label_visibility="collapsed",
        placeholder="Ej: 70.5",
    )
    btn_calcular = st.form_submit_button(
        "Calcular",
        type="primary",
        disabled=st.session_state.modo_resultado,
        use_container_width=True,
    )

btn_reiniciar = st.button(
    "Nuevo cálculo",
    type="secondary",
    disabled=not st.session_state.modo_resultado,
    use_container_width=True,
)

# Panel de resultado (visible solo en modo resultado)
if st.session_state.modo_resultado and st.session_state.dosis is not None:
    st.markdown('<div class="resultado-etiqueta">Dosis recomendada</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="resultado-valor">{st.session_state.dosis:.2f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="resultado-unidad">mL</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Uso clínico referencial SURA® 2026</div>', unsafe_allow_html=True)


# ===========================================================================
# 6. MANEJO DE EVENTOS
# ===========================================================================

if btn_reiniciar:
    st.session_state.modo_resultado = False
    st.session_state.peso_txt = ""
    st.session_state.dosis = None
    st.rerun()

if btn_calcular:
    try:
        peso = parsear_peso(peso_txt)
        dosis = calcular_dosis_ml(peso)
        st.session_state.peso_txt = peso_txt
        st.session_state.dosis = dosis
        st.session_state.modo_resultado = True
        st.rerun()
    except ValueError as e:
        # Distingue entre error de formato y error de dominio
        mensaje = (
            "Ingrese un número válido para el peso.\nUse punto (.) o coma (,) para decimales."
            if "could not convert" in str(e) or "vacío" in str(e)
            else str(e)
        )
        st.error(mensaje)
