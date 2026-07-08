import streamlit as st

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

st.set_page_config(
    page_title="Panel SEM Urgencias",
    page_icon="🏥",
    layout="wide"
)

# =============================================================================
# CONSTANTES
# =============================================================================

SILLAS_HABILITADAS = 20
CAMILLAS_HABILITADAS = 20
REANIMACION_HABILITADAS = 2

CAPACIDAD_TOTAL = (
    SILLAS_HABILITADAS
    + CAMILLAS_HABILITADAS
    + REANIMACION_HABILITADAS
)

# =============================================================================
# ESTILOS
# =============================================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background-color:#F4F7FB;
}

.titulo-sura{
    color:#0033A0;
    text-align:center;
    font-size:42px;
    font-weight:800;
}

.subtitulo-sura{
    color:#6B7280;
    text-align:center;
    font-size:16px;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNCIONES
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
        (pacientes_ubicados / CAPACIDAD_TOTAL) * 100, 1
    )

    saturacion = round(
        (total_pacientes / CAPACIDAD_TOTAL) * 100, 1
    )

    return (
        pacientes_ubicados,
        total_pacientes,
        ocupacion,
        saturacion,
    )

# =============================================================================
# ENCABEZADO
# =============================================================================

st.markdown(
    '<div class="titulo-sura">Panel SEM Urgencias</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo-sura">Ocupación • Saturación • Capacidad Instalada</div>',
    unsafe_allow_html=True
)

# =============================================================================
# CAPACIDAD INSTALADA
# =============================================================================

st.info(
    f"""
### Capacidad instalada: {CAPACIDAD_TOTAL}

🔹 Sillas habilitadas: {SILLAS_HABILITADAS}

🔹 Camillas habilitadas: {CAMILLAS_HABILITADAS}

🔹 Camillas de reanimación: {REANIMACION_HABILITADAS}
"""
)

# =============================================================================
# FORMULARIO
# =============================================================================

st.subheader("Registro Operativo")

with st.form("formulario"):

    col1, col2, col3 = st.columns(3)

    with col1:
        pacientes_sillas = st.number_input(
            "Pacientes en sillas",
            min_value=0,
            value=0
        )

    with col2:
        pacientes_camillas = st.number_input(
            "Pacientes en camillas",
            min_value=0,
            value=0
        )

    with col3:
        pacientes_reanimacion = st.number_input(
            "Pacientes en reanimación",
            min_value=0,
            value=0
        )

    col4, col5 = st.columns(2)

    with col4:
        pendientes_triage = st.number_input(
            "Pendientes de triage",
            min_value=0,
            value=0
        )

    with col5:
        pendientes_atencion = st.number_input(
            "Pendientes de atención médica",
            min_value=0,
            value=0
        )

    calcular = st.form_submit_button(
        "Calcular indicadores",
        use_container_width=True
    )

# =============================================================================
# RESULTADOS
# =============================================================================

if calcular:

    (
        pacientes_ubicados,
        total_pacientes,
        ocupacion,
        saturacion
    ) = calcular_indicadores(
        pacientes_sillas,
        pacientes_camillas,
        pacientes_reanimacion,
        pendientes_triage,
        pendientes_atencion
    )

    st.divider()

    st.subheader("Indicadores SEM")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Pacientes ubicados",
        pacientes_ubicados
    )

    col2.metric(
        "Total pacientes servicio",
        total_pacientes
    )

    col3.metric(
        "Ocupación",
        f"{ocupacion}%"
    )

    col4.metric(
        "Saturación",
        f"{saturacion}%"
    )

    st.divider()

    if ocupacion <= 80:
        st.success(f"✅ Ocupación normal ({ocupacion}%)")

    elif ocupacion <= 100:
        st.warning(f"⚠️ Ocupación alta ({ocupacion}%)")

    else:
        st.error(f"🚨 Ocupación crítica ({ocupacion}%)")

    if saturacion <= 100:
        st.success(f"✅ Saturación normal ({saturacion}%)")

    elif saturacion <= 120:
        st.warning(f"⚠️ Sobredemanda ({saturacion}%)")

    else:
        st.error(f"🚨 Servicio saturado ({saturacion}%)")

st.divider()

st.caption("Salud SURA • Indicadores SEM de Urgencias")
