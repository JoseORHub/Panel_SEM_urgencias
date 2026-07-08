"""
Panel SEM Urgencias — Ocupación, Saturación y Capacidad Instalada
==========================================================
Basado en el "ABC del Reporte en Plataforma SEM" (Alcaldía de Medellín):
  - Paso A: Capacidad instalada (sillas, camillas, reanimación)
  - Paso B: Ocupación = pacientes ubicados / capacidad instalada x 100
  - Paso C: Saturación = total pacientes en el servicio / capacidad instalada x 100

Estructura del archivo (para facilitar auditoría y mantenimiento):
  1. Constantes (diseño y protocolo)
  2. Lógica de negocio (funciones puras, sin dependencias de UI)
  3. Configuración de página y estilos
  4. Estado de la sesión
  5. Construcción de la UI
  6. Manejo de eventos
"""

from dataclasses import dataclass

import streamlit as st


# ===========================================================================
# 1. CONSTANTES
# ===========================================================================

# -- Colores corporativos SURA --
AZUL_SURA        = "#2D6DF6"   # Pantone 2727 C · RGB 45 109 246
AZUL_SURA_HOVER  = "#1A56D6"   # Variante oscura para hover
AZUL_OSCURO      = "#0033A0"   # Azul oscuro para títulos
GRIS_TEXTO       = "#4A4A4A"
GRIS_CLARO       = "#6B7280"
GRIS_SUAVE       = "#CCCCCC"
FONDO_APP        = "#F4F7FB"
BLANCO           = "#FFFFFF"

# -- Colores de estado (semáforo de indicadores) --
VERDE_OK    = "#1B8A3D"
NARANJA_ALT = "#C77700"
ROJO_CRIT   = "#C0272D"

# -- Capacidad instalada del servicio (Paso A - Capacidad) --
# Importante: debe coincidir con lo reportado en REPS.
SILLAS_HABILITADAS      = 20
CAMILLAS_HABILITADAS    = 20
REANIMACION_HABILITADAS = 2

CAPACIDAD_TOTAL = SILLAS_HABILITADAS + CAMILLAS_HABILITADAS + REANIMACION_HABILITADAS

# -- Umbrales de clasificación de indicadores --
UMBRAL_OCUPACION_ALTA    = 80   # % a partir del cual la ocupación se considera alta
UMBRAL_OCUPACION_CRITICA = 100  # % a partir del cual la ocupación se considera crítica
UMBRAL_SATURACION_SOBREDEMANDA = 100  # % a partir del cual hay sobredemanda
UMBRAL_SATURACION_CRITICA      = 120  # % a partir del cual el servicio está saturado


# ===========================================================================
# 2. LÓGICA DE NEGOCIO
# ===========================================================================

@dataclass(frozen=True)
class RegistroOperativo:
    """Datos operativos capturados en el formulario, ya validados."""
    pacientes_sillas: int
    pacientes_camillas: int
    pacientes_reanimacion: int
    pendientes_triage: int
    pendientes_atencion: int


@dataclass(frozen=True)
class IndicadoresSEM:
    """Resultado del cálculo de indicadores SEM para un registro dado."""
    pacientes_ubicados: int
    total_pacientes: int
    ocupacion: float
    saturacion: float


def validar_registro(
    pacientes_sillas: int,
    pacientes_camillas: int,
    pacientes_reanimacion: int,
    pendientes_triage: int,
    pendientes_atencion: int,
) -> RegistroOperativo:
    """
    Valida los datos operativos ingresados antes de calcular indicadores.

    Reglas de negocio:
        - Ningún valor puede ser negativo.
        - Los pacientes ubicados en sillas, camillas y reanimación no pueden
          superar la capacidad instalada de cada recurso (son espacios físicos).
        - Los pacientes pendientes de triage/atención no tienen tope físico,
          ya que aún no ocupan un recurso instalado.

    Raises:
        ValueError: Si algún valor incumple las reglas anteriores.
    """
    valores = {
        "Pacientes en sillas": pacientes_sillas,
        "Pacientes en camillas": pacientes_camillas,
        "Pacientes en reanimación": pacientes_reanimacion,
        "Pendientes de triage": pendientes_triage,
        "Pendientes de atención": pendientes_atencion,
    }
    for nombre, valor in valores.items():
        if valor < 0:
            raise ValueError(f"'{nombre}' no puede ser negativo (recibido: {valor}).")

    if pacientes_sillas > SILLAS_HABILITADAS:
        raise ValueError(
            f"Pacientes en sillas ({pacientes_sillas}) no puede superar la capacidad "
            f"instalada de sillas ({SILLAS_HABILITADAS})."
        )
    if pacientes_camillas > CAMILLAS_HABILITADAS:
        raise ValueError(
            f"Pacientes en camillas ({pacientes_camillas}) no puede superar la capacidad "
            f"instalada de camillas ({CAMILLAS_HABILITADAS})."
        )
    if pacientes_reanimacion > REANIMACION_HABILITADAS:
        raise ValueError(
            f"Pacientes en reanimación ({pacientes_reanimacion}) no puede superar la "
            f"capacidad instalada de reanimación ({REANIMACION_HABILITADAS})."
        )

    return RegistroOperativo(
        pacientes_sillas=pacientes_sillas,
        pacientes_camillas=pacientes_camillas,
        pacientes_reanimacion=pacientes_reanimacion,
        pendientes_triage=pendientes_triage,
        pendientes_atencion=pendientes_atencion,
    )


def calcular_indicadores(registro: RegistroOperativo, capacidad_total: int = CAPACIDAD_TOTAL) -> IndicadoresSEM:
    """
    Calcula los indicadores SEM de Ocupación y Saturación (Pasos B y C del ABC).

    Args:
        registro:        Datos operativos ya validados (ver validar_registro).
        capacidad_total: Capacidad instalada total (sillas + camillas + reanimación).

    Returns:
        IndicadoresSEM con pacientes ubicados, total de pacientes en el servicio,
        porcentaje de ocupación y porcentaje de saturación.

    Raises:
        ValueError: Si la capacidad total es menor o igual a 0 (evita división por cero).
    """
    if capacidad_total <= 0:
        raise ValueError("La capacidad total debe ser mayor que 0 para calcular indicadores.")

    pacientes_ubicados = (
        registro.pacientes_sillas
        + registro.pacientes_camillas
        + registro.pacientes_reanimacion
    )
    total_pacientes = (
        pacientes_ubicados
        + registro.pendientes_triage
        + registro.pendientes_atencion
    )

    ocupacion = round((pacientes_ubicados / capacidad_total) * 100, 1)
    saturacion = round((total_pacientes / capacidad_total) * 100, 1)

    return IndicadoresSEM(
        pacientes_ubicados=pacientes_ubicados,
        total_pacientes=total_pacientes,
        ocupacion=ocupacion,
        saturacion=saturacion,
    )


def clasificar_ocupacion(ocupacion: float) -> tuple[str, str]:
    """Devuelve (nivel, color) según el porcentaje de ocupación."""
    if ocupacion <= UMBRAL_OCUPACION_ALTA:
        return "Normal", VERDE_OK
    if ocupacion <= UMBRAL_OCUPACION_CRITICA:
        return "Alta", NARANJA_ALT
    return "Crítica", ROJO_CRIT


def clasificar_saturacion(saturacion: float) -> tuple[str, str]:
    """Devuelve (nivel, color) según el porcentaje de saturación."""
    if saturacion <= UMBRAL_SATURACION_SOBREDEMANDA:
        return "Normal", VERDE_OK
    if saturacion <= UMBRAL_SATURACION_CRITICA:
        return "Sobredemanda", NARANJA_ALT
    return "Saturado", ROJO_CRIT


# ===========================================================================
# 3. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ===========================================================================

st.set_page_config(
    page_title="Panel SEM Urgencias",
    page_icon="🏥",
    layout="wide",
)

CSS = f"""
<style>
  #MainMenu {{visibility: hidden;}}
  footer {{visibility: hidden;}}
  header {{visibility: hidden;}}

  html, body, [class*="css"] {{
    font-family: Arial, sans-serif !important;
  }}

  .stApp {{
    background-color: {FONDO_APP};
  }}

  /* ── Encabezado ── */
  .titulo-sura {{
    color: {AZUL_OSCURO};
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 4px;
  }}
  .subtitulo-sura {{
    color: {GRIS_CLARO};
    text-align: center;
    font-size: 15px;
    margin-bottom: 20px;
  }}

  /* ── Botón principal: AZUL SURA ── */
  div[data-testid="stFormSubmitButton"] > button {{
    background-color: {AZUL_SURA} !important;
    color: {BLANCO} !important;
    border: none !important;
    padding: 12px 10px !important;
    font-weight: 700 !important;
    font-size: 11pt !important;
    border-radius: 4px !important;
    transition: background-color 0.2s ease !important;
  }}
  div[data-testid="stFormSubmitButton"] > button:hover {{
    background-color: {AZUL_SURA_HOVER} !important;
    color: {BLANCO} !important;
  }}

  /* ── Tarjetas de métricas ── */
  div[data-testid="stMetric"] {{
    background-color: {BLANCO};
    border: 1px solid #E3E8F0;
    border-radius: 8px;
    padding: 12px 10px;
  }}
  div[data-testid="stMetricLabel"] {{
    color: {GRIS_TEXTO} !important;
  }}
  div[data-testid="stMetricValue"] {{
    color: {AZUL_OSCURO} !important;
  }}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ===========================================================================
# 4. ESTADO DE LA SESIÓN
# ===========================================================================

st.session_state.setdefault("indicadores", None)
st.session_state.setdefault("error_validacion", None)


# ===========================================================================
# 5. CONSTRUCCIÓN DE LA UI
# ===========================================================================

# -- Encabezado --
st.markdown('<div class="titulo-sura">Panel SEM Urgencias</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitulo-sura">Ocupación • Saturación • Capacidad Instalada</div>',
    unsafe_allow_html=True,
)

# -- Capacidad instalada (Paso A, valores constantes y auditable) --
st.info(
    f"""
### Capacidad instalada: {CAPACIDAD_TOTAL}

🔹 Sillas habilitadas: {SILLAS_HABILITADAS}

🔹 Camillas habilitadas: {CAMILLAS_HABILITADAS}

🔹 Camillas de reanimación: {REANIMACION_HABILITADAS}

*Importante: debe coincidir con lo reportado en REPS.*
"""
)

# -- Formulario de registro operativo --
st.subheader("Registro Operativo")

with st.form("formulario_registro_operativo"):
    col1, col2, col3 = st.columns(3)

    with col1:
        pacientes_sillas = st.number_input(
            "Pacientes en sillas", min_value=0, max_value=SILLAS_HABILITADAS, value=0,
        )
    with col2:
        pacientes_camillas = st.number_input(
            "Pacientes en camillas", min_value=0, max_value=CAMILLAS_HABILITADAS, value=0,
        )
    with col3:
        pacientes_reanimacion = st.number_input(
            "Pacientes en reanimación", min_value=0, max_value=REANIMACION_HABILITADAS, value=0,
        )

    col4, col5 = st.columns(2)

    with col4:
        pendientes_triage = st.number_input(
            "Pendientes de triage", min_value=0, value=0,
        )
    with col5:
        pendientes_atencion = st.number_input(
            "Pendientes de atención médica", min_value=0, value=0,
        )

    btn_calcular = st.form_submit_button(
        "Calcular indicadores", use_container_width=True,
    )

# -- Panel de resultados --
if st.session_state.error_validacion:
    st.error(st.session_state.error_validacion)

if st.session_state.indicadores is not None:
    indicadores: IndicadoresSEM = st.session_state.indicadores

    st.divider()
    st.subheader("Indicadores SEM")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pacientes ubicados", indicadores.pacientes_ubicados)
    col2.metric("Total pacientes servicio", indicadores.total_pacientes)
    col3.metric("Ocupación", f"{indicadores.ocupacion}%")
    col4.metric("Saturación", f"{indicadores.saturacion}%")

    st.divider()

    nivel_ocupacion, _ = clasificar_ocupacion(indicadores.ocupacion)
    nivel_saturacion, _ = clasificar_saturacion(indicadores.saturacion)

    mensajes_ocupacion = {
        "Normal":  ("success", f"✅ Ocupación normal ({indicadores.ocupacion}%)"),
        "Alta":    ("warning", f"⚠️ Ocupación alta ({indicadores.ocupacion}%)"),
        "Crítica": ("error",   f"🚨 Ocupación crítica ({indicadores.ocupacion}%)"),
    }
    tipo, texto = mensajes_ocupacion[nivel_ocupacion]
    getattr(st, tipo)(texto)

    mensajes_saturacion = {
        "Normal":       ("success", f"✅ Saturación normal ({indicadores.saturacion}%)"),
        "Sobredemanda": ("warning", f"⚠️ Sobredemanda ({indicadores.saturacion}%)"),
        "Saturado":     ("error",   f"🚨 Servicio saturado ({indicadores.saturacion}%)"),
    }
    tipo, texto = mensajes_saturacion[nivel_saturacion]
    getattr(st, tipo)(texto)

st.divider()
st.caption("Salud SURA • Indicadores SEM de Urgencias")


# ===========================================================================
# 6. MANEJO DE EVENTOS
# ===========================================================================

if btn_calcular:
    try:
        registro = validar_registro(
            pacientes_sillas=pacientes_sillas,
            pacientes_camillas=pacientes_camillas,
            pacientes_reanimacion=pacientes_reanimacion,
            pendientes_triage=pendientes_triage,
            pendientes_atencion=pendientes_atencion,
        )
        st.session_state.indicadores = calcular_indicadores(registro)
        st.session_state.error_validacion = None
    except ValueError as e:
        st.session_state.indicadores = None
        st.session_state.error_validacion = str(e)
    st.rerun()
