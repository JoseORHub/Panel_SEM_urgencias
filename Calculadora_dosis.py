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

# -- Protocolo clínico: UI por kg según formulación --
FACTORES_UI_POR_KG: dict = {
    "Heteróloga": 40,   # suero equino
    "Homóloga":   20,   # inmunoglobulina humana
}


# ===========================================================================
# 2. LÓGICA DE NEGOCIO
# ===========================================================================

def calcular_dosis_UI(peso_kg: float, factor: float) -> float:
    """
    Calcula la dosis en UI según el peso del paciente y el factor de la formulación.

    Args:
        peso_kg: Peso del paciente en kilogramos. Debe ser > 0.
        factor:  UI por kg según formulación (20 homóloga / 40 heteróloga).

    Returns:
        Dosis redondeada a 0 decimales en UI.

    Raises:
        ValueError: Si el peso no es un número positivo.
    """
    if peso_kg <= 0:
        raise ValueError(f"El peso debe ser mayor que 0 kg (recibido: {peso_kg})")
    return round(peso_kg * factor, 0)


def parsear_peso(texto: str) -> float:
    """
    Convierte el texto ingresado por el usuario a float.
    Acepta punto y coma como separador decimal.

    Raises:
        ValueError: Si el texto no representa un número válido.
    """
    texto = texto.strip().replace(",", ".")
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

  /* ── Ancho máximo (450 px) ── */
  .main .block-container {{
    max-width: 450px;
    padding-top: 20px;
    padding-bottom: 10px;
  }}

  /* ── Título principal ── */
  .titulo {{
    color: {AZUL_OSCURO};
    font-size: 18pt;
    font-weight: 700;
    text-align: center;
    margin: 20px 0 10px 0;
  }}

  /* ── Etiquetas ── */
  .label {{
    color: {GRIS_TEXTO};
    font-size: 11pt;
    text-align: center;
    margin: 10px 0 5px 0;
  }}

   .formulacion-titulo {{
    color: {AZUL_OSCURO};
    font-size: 10pt;
    font-weight: 700;
    text-align: center;
    margin-bottom: 6px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }}

  /* ── Radio buttons centrados ── */
  div[data-testid="stRadio"] {{
    border: none !important;
    box-shadow: none !important;
    color: {AZUL_OSCURO};
  }}
  div[data-testid="stRadio"] > label {{
    display: none;
    color: {AZUL_OSCURO};
  }}
  div[data-testid="stRadio"] > div {{
    justify-content: center !important;
    gap: 30px !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    color: {AZUL_OSCURO};
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

  /* ── Botón secundario: "Nuevo cálculo" ── */
  .stButton > button[kind="secondary"] {{
    background-color: {BLANCO} !important;
    color: {AZUL_SURA} !important;
    border: 2px solid {AZUL_SURA} !important;
    border-radius: 4px !important;
    font-size: 10pt !important;
    font-weight: 600 !important;
    padding: 10px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: background-color 0.2s ease, color 0.2s ease !important;
    animation: pulso 1.8s ease-in-out infinite !important;
  }}
  .stButton > button[kind="secondary"]:hover {{
    background-color: {AZUL_SURA} !important;
    color: {BLANCO} !important;
  }}
  .stButton > button[kind="secondary"]:disabled {{
    color: {GRIS_SUAVE} !important;
    border: 2px solid {GRIS_SUAVE} !important;
    animation: none !important;
  }}

  /* Pulso sutil para llamar la atención cuando está activo */
  @keyframes pulso {{
    0%   {{ box-shadow: 0 0 0 0 rgba(45, 109, 246, 0.35); }}
    60%  {{ box-shadow: 0 0 0 7px rgba(45, 109, 246, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(45, 109, 246, 0); }}
  }}

  /* ── Panel de resultado ── */
  .resultado-etiqueta {{
    color: {GRIS_TEXTO};
    font-size: 10pt;
    text-align: center;
    margin-top: 15px;
  }}
  .resultado-formulacion {{
    color: {AZUL_SURA};
    font-size: 9pt;
    font-weight: 600;
    text-align: center;
    margin-top: 2px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }}
  .resultado-valor {{
    color: #000000;
    font-size: 26pt;
    font-weight: 800;
    text-align: center;
    margin: 4px 0 0 0;
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
# 4. ESTADO DE LA SESIÓN
# ===========================================================================

st.session_state.setdefault("modo_resultado", False)
st.session_state.setdefault("peso_txt", "")
st.session_state.setdefault("dosis", None)
st.session_state.setdefault("formulacion", "Heteróloga")


# ===========================================================================
# 5. CONSTRUCCIÓN DE LA UI
# ===========================================================================

st.markdown('<div class="titulo">Calculadora dosis antirrábica</div>', unsafe_allow_html=True)

# ── Selector de formulación ──────────────────────────────────────────────────
st.markdown('<div class="formulacion-box">', unsafe_allow_html=True)
st.markdown('<div class="formulacion-titulo">Formulación de la vacuna</div>', unsafe_allow_html=True)

formulacion = st.radio(
    label="Formulación",
    options=list(FACTORES_UI_POR_KG.keys()),
    index=list(FACTORES_UI_POR_KG.keys()).index(st.session_state.formulacion),
    horizontal=True,
    disabled=st.session_state.modo_resultado,
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Campo de peso y botón calcular ──────────────────────────────────────────
st.markdown('<div class="label">Peso del paciente (kg)</div>', unsafe_allow_html=True)

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
    "↺  Nuevo cálculo",
    type="secondary",
    disabled=not st.session_state.modo_resultado,
    use_container_width=True,
)

# ── Panel de resultado ───────────────────────────────────────────────────────
if st.session_state.modo_resultado and st.session_state.dosis is not None:
    st.markdown('<div class="resultado-etiqueta">Dosis recomendada</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="resultado-formulacion">Formulación {st.session_state.formulacion}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="resultado-valor">{st.session_state.dosis:.0f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="resultado-unidad">UI</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Uso clínico referencial SURA® 2026</div>', unsafe_allow_html=True)


# ===========================================================================
# 6. MANEJO DE EVENTOS
# ===========================================================================

if btn_reiniciar:
    st.session_state.modo_resultado = False
    st.session_state.peso_txt = ""
    st.session_state.dosis = None
    # La formulación se conserva para el siguiente cálculo
    st.rerun()

if btn_calcular:
    try:
        peso = parsear_peso(peso_txt)
        factor = FACTORES_UI_POR_KG[formulacion]
        dosis = calcular_dosis_UI(peso, factor)
        st.session_state.peso_txt = peso_txt
        st.session_state.dosis = dosis
        st.session_state.formulacion = formulacion
        st.session_state.modo_resultado = True
        st.rerun()
    except ValueError as e:
        mensaje = (
            "Ingrese un número válido para el peso.\nUse punto (.) o coma (,) para decimales."
            if "could not convert" in str(e) or "vacío" in str(e)
            else str(e)
        )
        st.error(mensaje)
