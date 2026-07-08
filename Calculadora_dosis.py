"""
Panel SEM - Servicio de Urgencias
=================================

Indicadores calculados:

1. Capacidad instalada
2. Pacientes ubicados
3. Total pacientes en servicio
4. Ocupación (%)
5. Saturación (%)

Fórmulas SEM

Ocupación (%) =
(Pacientes en sillas + camillas + reanimación)
/
Capacidad instalada
x 100

Saturación (%) =
Total pacientes en servicio
/
Capacidad instalada
x 100
"""

import streamlit as st


# =============================================================================
# 1. CONSTANTES
# =============================================================================

AZUL_SURA = "#2D6DF6"
AZUL_OSCURO = "#0033A0"
BLANCO = "#FFFFFF"
GRIS = "#666666"

# Capacidad instalada

SILLAS_HABILITADAS = 20
CAMILLAS_HABILITADAS = 20
REANIMACION_HABILITADAS = 2

CAPACIDAD_TOTAL = (
    SILLAS_HABILITADAS
    + CAMILLAS_HABILITADAS
    + REANIMACION_HABILITADAS
)


# =============================================================================
# 2. LOGICA DE NEGOCIO
# =============================================================================

def calcular_indicadores(
    pacientes_sillas,
    pacientes_camillas,
    pacientes_reanimacion,
    pendientes_triage,
    pendientes_atencion,
):

    pacientes_ubicados = (
        pacientes_sillas
        + pacientes_camillas
        + pacientes_reanimacion
    )

    total_pacientes = (
        pacientes_ubicados
        + pendientes_triage
        + pendientes_atencion
    )

    ocupacion = round(
        (pacientes_ubicados / CAPACIDAD_TOTAL) * 100,
        1,
    )

    saturacion = round(
        (total_pacientes / CAPACIDAD_TOTAL) * 100,
        1,
    )

    return {
        "pacientes_ubicados": pacientes_ubicados,
        "total_pacientes": total_pacientes,
        "ocupacion": ocupacion,
        "saturacion": saturacion,
    }


def nivel_ocupacion(valor):

    if valor <= 80:
        return "NORMAL", "#1B8A3D"

    if valor <= 100:
        return "ALTA", "#E67E22"

    return "CRÍTICA", "#C0392B"


def nivel_saturacion(valor):

    if valor <= 100:
        return "NORMAL", "#1B8A3D"

    if valor <= 120:
        return "SOBREDEMANDA", "#E67E22"

    return "SATURADO", "#C0392B"


# =============================================================================
# 3. CONFIGURACION
# =============================================================================

st.set_page_config(
    page_title="Panel SEM Urgencias",
    layout="centered",
)

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color:{BLANCO};
    }}

    .titulo {{
        color:{AZUL_OSCURO};
        text-align:center;
        font-size:28px;
        font-weight:bold;
        margin-bottom:5px;
    }}

    .subtitulo {{
        text-align:center;
        color:{GRIS};
        margin-bottom:20px;
    }}

    .card {{
        border:1px solid #EAEAEA;
        border-radius:10px;
        padding:16px;
        text-align:center;
        margin-top:10px;
        box-shadow:0 1px 3px rgba(0,0,0,.08);
    }}

    .etiqueta {{
        color:{GRIS};
        font-size:12px;
        text-transform:uppercase;
    }}

    .valor {{
        font-size:30px;
        font-weight:bold;
        color:{AZUL_OSCURO};
    }}

    .badge {{
        padding:6px 14px;
        border-radius:20px;
        font-weight:bold;
        display:inline-block;
        margin-top:8px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 4. CABECERA
# =============================================================================

st.markdown(
    '<div class="titulo">Panel SEM de Urgencias</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitulo">Indicadores de ocupación y saturación</div>',
    unsafe_allow_html=True,
)


st.info(
    f"""
Capacidad instalada: {CAPACIDAD_TOTAL}

• Sillas: {SILLAS_HABILITADAS}
• Camillas: {CAMILLAS_HABILITADAS}
• Reanimación: {REANIMACION_HABILITADAS}
"""
)


# =============================================================================
# 5. ENTRADAS
# =============================================================================

with st.form("formulario"):

    st.subheader("Pacientes ubicados")

    pacientes_sillas = st.number_input(
        "Pacientes en sillas",
        min_value=0,
        value=0,
    )

    pacientes_camillas = st.number_input(
        "Pacientes en camillas",
        min_value=0,
        value=0,
    )

    pacientes_reanimacion = st.number_input(
        "Pacientes en reanimación",
        min_value=0,
        value=0,
    )

    st.subheader("Pacientes pendientes")

    pendientes_triage = st.number_input(
        "Pendientes de triage",
        min_value=0,
        value=0,
    )

    pendientes_atencion = st.number_input(
        "Pendientes de atención médica",
        min_value=0,
        value=0,
    )

    calcular = st.form_submit_button(
        "Calcular indicadores",
        use_container_width=True,
    )


# =============================================================================
# 6. RESULTADOS
# =============================================================================

if calcular:

    indicadores = calcular_indicadores(
        pacientes_sillas,
        pacientes_camillas,
        pacientes_reanimacion,
        pendientes_triage,
        pendientes_atencion,
    )

    nivel_ocu, color_ocu = nivel_ocupacion(
        indicadores["ocupacion"]
    )

    nivel_sat, color_sat = nivel_saturacion(
        indicadores["saturacion"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="etiqueta">Pacientes ubicados</div>
                <div class="valor">
                    {indicadores["pacientes_ubicados"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="etiqueta">Total pacientes servicio</div>
                <div class="valor">
                    {indicadores["total_pacientes"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            f"""
            <div class="card">
                <div class="etiqueta">Ocupación</div>
                <div class="valor">
                    {indicadores["ocupacion"]}%
                </div>
                <span
                    class="badge"
                    style="
                    background:{color_ocu}22;
                    color:{color_ocu};
                    ">
                    {nivel_ocu}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            f"""
            <div class="card">
                <div class="etiqueta">Saturación</div>
                <div class="valor">
                    {indicadores["saturacion"]}%
                </div>
                <span
                    class="badge"
                    style="
                    background:{color_sat}22;
                    color:{color_sat};
                    ">
                    {nivel_sat}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.success(
        f"""
Pacientes ubicados: {indicadores['pacientes_ubicados']}

Total pacientes servicio: {indicadores['total_pacientes']}

Ocupación: {indicadores['ocupacion']}%

Saturación: {indicadores['saturacion']}%
"""
    )
