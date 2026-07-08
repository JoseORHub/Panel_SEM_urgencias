"""
Calculadora de Ocupación — Servicio de Urgencias (Plataforma SEM)
==========================================================
Estructura:
  1. Constantes (diseño y protocolo)
  2. Lógica de negocio (pura, sin dependencias de UI)
  3. Configuración de página y estilos
  4. Estado de sesión
  5. Construcción de la UI
  6. Manejo de eventos

Fórmula (Paso B - Ocupación, ABC del reporte en Plataforma SEM):
  Ocupación (%) = (Total pacientes en camas y sillas / Total camas y sillas
                    habilitadas disponibles) x 100
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

# -- Capacidad instalada (constantes del servicio, Paso A - Capacidad) --
SILLAS_HABILITADAS   = 20
CAMILLAS_HABILITADAS = 20
CAPACIDAD_TOTAL       = SILLAS_HABILITADAS + CAMILLAS_HABILITADAS


# ===========================================================================
# 2. LÓGICA DE NEGOCIO
# ===========================================================================

def calcular_ocupacion(sillas_ocupadas: int, camillas_ocupadas: int, capacidad_total: int) -> float:
    """
    Calcula el porcentaje de ocupación del servicio de urgencias.

    Ocupación (%) = (pacientes en sillas + pacientes en camillas) / capacidad total * 100

    Args:
        sillas_ocupadas:   Número de sillas ocupadas por pacientes. Debe ser >= 0.
        camillas_ocupadas: Número de camillas ocupadas por pacientes. Debe ser >= 0.
        capacidad_total:   Total de sillas + camillas habilitadas (capacidad instalada).

    Returns:
        Porcentaje de ocupación, redondeado a 1 decimal.

    Raises:
        ValueError: Si algún valor es negativo o excede la capacidad habilitada de su tipo.
    """
    if sillas_ocupadas < 0 or camillas_ocupadas < 0:
        raise ValueError("Las cantidades ocupadas no pueden ser negativas.")
    if sillas_ocupadas > SILLAS_HABILITADAS:
        raise ValueError(
            f"Sillas ocupadas ({sillas_ocupadas}) no puede superar la capacidad instalada "
            f"de sillas ({SILLAS_HABILITADAS})."
        )
    if camillas_ocupadas > CAMILLAS_HABILITADAS:
        raise ValueError(
            f"Camillas ocupadas ({camillas_ocupadas}) no puede superar la capacidad instalada "
            f"de camillas ({CAMILLAS_HABILITADAS})."
        )

    total_pacientes = sillas_ocupadas + camillas_ocupadas
    return round((total_pacientes / capacidad_total) * 100, 1)


def parsear_entero(texto: str, nombre_campo: str) -> int:
    """
    Convierte el texto ingresado por el usuario a entero no negativo.

    Args:
        texto:        Valor ingresado en el campo de texto.
        nombre_campo: Nombre descriptivo del campo, usado en mensajes de error.

    Raises:
        ValueError: Si el texto está vacío o no representa un entero válido.
    """
    texto = texto.strip()
    if not texto:
        raise ValueError(f"El campo '{nombre_campo}' está vacío.")
    try:
        valor = int(texto)
    except ValueError:
        raise ValueError(f"Ingrese un número entero válido para '{nombre_campo}'.")
    return valor


# ===========================================================================
# 3. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ===========================================================================

st.set_page_config(
    page_title="Calculadora de ocupación - Urgencias",
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
    padding-top: 10px;
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

  .subtitulo {{
    color: {AZUL_OSCURO};
    font-size: 10pt;
    font-weight: 700;
    text-align: center;
    margin-bottom: 6px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }}

  /* ── Panel de capacidad instalada (constantes) ── */
  .capacidad-box {{
    background-color: #F2F6FF;
    border: 1px solid #DCE6FB;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 10px 0 14px 0;
    text-align: center;
  }}
  .capacidad-item {{
    color: {GRIS_TEXTO};
    font-size: 10pt;
    display: inline-block;
    margin: 0 12px;
  }}
  .capacidad-item b {{
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
  .resultado-detalle {{
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

  /* ── Etiqueta de nivel de ocupación ── */
  .nivel-badge {{
    display: inline-block;
    margin-top: 10px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 0.3px;
    text-transform: uppercase;
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
st.session_state.setdefault("sillas_txt", "")
st.session_state.setdefault("camillas_txt", "")
st.session_state.setdefault("ocupacion", None)
st.session_state.setdefault("sillas_ocupadas", None)
st.session_state.setdefault("camillas_ocupadas", None)


# ===========================================================================
# 5. CONSTRUCCIÓN DE LA UI
# ===========================================================================

st.markdown('<div class="titulo">Calculadora de Ocupación<br>Servicio de Urgencias</div>', unsafe_allow_html=True)

# ── Panel de capacidad instalada (constantes, Paso A) ───────────────────────
st.markdown(
    f'''
    <div class="capacidad-box">
        <span class="capacidad-item">Sillas habilitadas: <b>{SILLAS_HABILITADAS}</b></span>
        <span class="capacidad-item">Camillas habilitadas: <b>{CAMILLAS_HABILITADAS}</b></span>
    </div>
    ''',
    unsafe_allow_html=True,
)

# ── Campos de entrada y botón calcular ──────────────────────────────────────
with st.form("form_ocupacion", clear_on_submit=False):
    st.markdown('<div class="label">Sillas ocupadas</div>', unsafe_allow_html=True)
    sillas_txt = st.text_input(
        label="Sillas ocupadas",
        value=st.session_state.sillas_txt,
        disabled=st.session_state.modo_resultado,
        label_visibility="collapsed",
        placeholder=f"Ej: 15 (máx. {SILLAS_HABILITADAS})",
    )

    st.markdown('<div class="label">Camillas ocupadas</div>', unsafe_allow_html=True)
    camillas_txt = st.text_input(
        label="Camillas ocupadas",
        value=st.session_state.camillas_txt,
        disabled=st.session_state.modo_resultado,
        label_visibility="collapsed",
        placeholder=f"Ej: 18 (máx. {CAMILLAS_HABILITADAS})",
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
if st.session_state.modo_resultado and st.session_state.ocupacion is not None:
    ocupacion = st.session_state.ocupacion
    total_pacientes = st.session_state.sillas_ocupadas + st.session_state.camillas_ocupadas

    # Nivel de saturación visual, alineado con el criterio de "Saturación" del PDF
    if ocupacion < 80:
        color_nivel, texto_nivel = "#1B8A3D", "Normal"
    elif ocupacion < 100:
        color_nivel, texto_nivel = "#C77700", "Alta"
    else:
        color_nivel, texto_nivel = "#C0272D", "Saturado"

    st.markdown('<div class="resultado-etiqueta">Ocupación del servicio</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="resultado-detalle">{total_pacientes} pacientes / {CAPACIDAD_TOTAL} capacidad instalada</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="resultado-valor">{ocupacion:.1f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="resultado-unidad">%</div>', unsafe_allow_html=True)
    st.markdown(
        f'''
        <div style="text-align:center;">
            <span class="nivel-badge" style="background-color:{color_nivel}22; color:{color_nivel};">
                {texto_nivel}
            </span>
        </div>
        ''',
        unsafe_allow_html=True,
    )

st.markdown('<div class="footer">Uso institucional referencial · ABC del reporte en Plataforma SEM</div>', unsafe_allow_html=True)


# ===========================================================================
# 6. MANEJO DE EVENTOS
# ===========================================================================

if btn_reiniciar:
    st.session_state.modo_resultado = False
    st.session_state.sillas_txt = ""
    st.session_state.camillas_txt = ""
    st.session_state.ocupacion = None
    st.session_state.sillas_ocupadas = None
    st.session_state.camillas_ocupadas = None
    st.rerun()

if btn_calcular:
    try:
        sillas_ocupadas = parsear_entero(sillas_txt, "Sillas ocupadas")
        camillas_ocupadas = parsear_entero(camillas_txt, "Camillas ocupadas")
        ocupacion = calcular_ocupacion(sillas_ocupadas, camillas_ocupadas, CAPACIDAD_TOTAL)

        st.session_state.sillas_txt = sillas_txt
        st.session_state.camillas_txt = camillas_txt
        st.session_state.sillas_ocupadas = sillas_ocupadas
        st.session_state.camillas_ocupadas = camillas_ocupadas
        st.session_state.ocupacion = ocupacion
        st.session_state.modo_resultado = True
        st.rerun()
    except ValueError as e:
        st.error(str(e))
