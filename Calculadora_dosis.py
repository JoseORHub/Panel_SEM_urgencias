"""
PANEL SEM URGENCIAS
===================

Indicadores calculados:

1. Capacidad instalada
2. Pacientes ubicados
3. Total pacientes en servicio
4. Ocupación (%)
5. Saturación (%)

Definiciones SEM

Ocupación (%) =
Pacientes ubicados /
Capacidad instalada * 100

Saturación (%) =
Total pacientes servicio /
Capacidad instalada * 100
"""

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
# ESTILOS SURA
# =============================================================================

st.markdown(
    """
<style>

/* ==========================================================
   PALETA SURA
========================================================== */

:root{
    --sura-blue:#0033A0;
    --sura-light:#2D6DF6;
    --text:#4B5563;
    --success:#16A34A;
    --warning:#D97706;
    --danger:#DC2626;
}

/* ==========================================================
   LIMPIEZA STREAMLIT
========================================================== */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* ==========================================================
   FONDO
========================================================== */

.stApp{
    background:#F4F7FB;
}

.main .block-container{
    max-width:1200px;
    padding-top:20px;
}

/* ==========================================================
   HERO
========================================================== */

.hero{
    background:linear-gradient(
        135deg,
        #0033A0 0%,
        #2D6DF6 100%
    );

    border-radius:24px;

    padding:35px;

    text-align:center;

    margin-bottom:25px;

    box-shadow:
        0px 10px 35px rgba(0,51,160,.25);
}

.hero-title{
    color:white;
    font-size:40px;
    font-weight:800;
    line-height:1;
}

.hero-subtitle{
    color:rgba(255,255,255,.92);
    margin-top:10px;
    font-size:15px;
}

/* ==========================================================
   CAPACIDAD
========================================================== */

.capacity-card{

    background:white;

    border-radius:22px;

    padding:25px;

    text-align:center;

    margin-bottom:25px;

    box-shadow:
        0px 4px 20px rgba(0,0,0,.05);
}

.capacity-title{

    color:#6B7280;

    text-transform:uppercase;

    letter-spacing:1px;

    font-size:12px;

    font-weight:700;
}

.capacity-value{

    color:#0033A0;

    font-size:62px;

    font-weight:800;

    line-height:1;
}

.capacity-detail{

    margin-top:10px;

    color:#6B7280;

    font-size:14px;
}

/* ==========================================================
   TITULOS
========================================================== */

.section-title{
    color:#0033A0;
    font-size:20px;
    font-weight:700;
    margin-bottom:10px;
}

/* ==========================================================
   INPUTS
========================================================== */

[data-testid="stNumberInput"]{

    background:white;

    border-radius:14px;

    padding:8px;

    box-shadow:
        0px 2px 8px rgba(0,0,0,.04);
}

input{
    text-align:center !important;
    font-size:20px !important;
    font-weight:600 !important;
}

/* ==========================================================
   BOTON
========================================================== */

div[data-testid="stFormSubmitButton"] button{

    background:#0033A0 !important;

    color:white !important;

    border:none !important;

    border-radius:12px !important;

    height:50px !important;

    font-size:15px !important;

    font-weight:700 !important;

    width:100%;
}

div[data-testid="stFormSubmitButton"] button:hover{

    background:#2D6DF6 !important;
}

/* ==========================================================
   KPI
========================================================== */

.kpi{

    background:white;

    border-radius:20px;

    padding:24px;

    text-align:center;

    box-shadow:
        0px 4px 18px rgba(0,0,0,.05);
}

.kpi-label{

    color:#6B7280;

    font-size:12px;

    font-weight:700;

    text-transform:uppercase;

    letter-spacing:1px;
}

.kpi-value{

    color:#0033A0;

    font-size:46px;

    font-weight:800;

    margin-top:8px;
}

/* ==========================================================
   RESULTADOS
========================================================== */

.result-card{

    background:white;

    border-left:6px solid #0033A0;

    border-radius:20px;

    padding:25px;

    text-align:center;

    box-shadow:
        0px 6px 20px rgba(0,0,0,.05);
}

.result-label{

    color:#6B7280;

    text-transform:uppercase;

    letter-spacing:1px;

    font-size:12px;

    font-weight:700;
}

.result-value{

    color:#0033A0;

    font-size:58px;

    font-weight:900;

    line-height:1;

    margin-top:10px;
}

.badge-green{

    background:#DCFCE7;

    color:#15803D;

    border-radius:30px;

    padding:7px 18px;

    font-size:12px;

    font-weight:700;
}

.badge-yellow{

    background:#FEF3C7;

    color:#B45309;

    border-radius:30px;

    padding:7px 18px;

    font-size:12px;

    font-weight:700;
}

.badge-red{

    background:#FEE2E2;

    color:#B91C1C;

    border-radius:30px;

    padding:7px 18px;

    font-size:12px;

    font-weight:700;
}

/* ==========================================================
   FOOTER
========================================================== */

.footer{

    text-align:center;

    color:#94A3B8;

    margin-top:35px;

    font-size:12px;
}

</style>
""",
    unsafe_allow_html=True,
)


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


def badge_ocupacion(valor):

    if valor <= 80:
        return "NORMAL", "badge-green"

    if valor <= 100:
        return "ALTA", "badge-yellow"

    return "CRÍTICA", "badge-red"


def badge_saturacion(valor):

    if valor <= 100:
        return "NORMAL", "badge-green"

    if valor <= 120:
        return "SOBREDEMANDA", "badge-yellow"

    return "SATURADO", "badge-red"


# =============================================================================
# ENCABEZADO
# =============================================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            Panel SEM Urgencias
        </div>

        <div class="hero-subtitle">
            Ocupación · Saturación · Capacidad Instalada
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="capacity-card">

        <div class="capacity-title">
            Capacidad Instalada
        </div>

        <div class="capacity-value">
            {CAPACIDAD_TOTAL}
        </div>

        <div class="capacity-detail">
            {SILLAS_HABILITADAS} Sillas ·
            {CAMILLAS_HABILITADAS} Camillas ·
            {REANIMACION_HABILITADAS} Reanimación
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# FORMULARIO
# =============================================================================

st.markdown(
    '<div class="section-title">Registro de pacientes</div>',
    unsafe_allow_html=True,
)

with st.form("formulario"):

    col1, col2, col3 = st.columns(3)

    with col1:
        pacientes_sillas = st.number_input(
            "Pacientes en sillas",
            min_value=0,
            value=0,
        )

    with col2:
        pacientes_camillas = st.number_input(
            "Pacientes en camillas",
            min_value=0,
            value=0,
        )

    with col3:
        pacientes_reanimacion = st.number_input(
            "Pacientes en reanimación",
            min_value=0,
            value=0,
        )

    col4, col5 = st.columns(2)

    with col4:
        pendientes_triage = st.number_input(
            "Pendientes de triage",
            min_value=0,
            value=0,
        )

    with col5:
        pendientes_atencion = st.number_input(
            "Pendientes de atención médica",
            min_value=0,
            value=0,
        )

    calcular = st.form_submit_button(
        "Calcular Indicadores"
    )


# =============================================================================
# RESULTADOS
# =============================================================================

if calcular:

    (
        pacientes_ubicados,
        total_pacientes,
        ocupacion,
        saturacion,
    ) = calcular_indicadores(
        pacientes_sillas,
        pacientes_camillas,
        pacientes_reanimacion,
        pendientes_triage,
        pendientes_atencion,
    )

    texto_ocu, clase_ocu = badge_ocupacion(ocupacion)
    texto_sat, clase_sat = badge_saturacion(saturacion)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">
                    Pacientes Ubicados
                </div>

                <div class="kpi-value">
                    {pacientes_ubicados}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">
                    Total Pacientes Servicio
                </div>

                <div class="kpi-value">
                    {total_pacientes}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    Ocupación
                </div>

                <div class="result-value">
                    {ocupacion}%
                </div>

                <span class="{clase_ocu}">
                    {texto_ocu}
                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    Saturación
                </div>

                <div class="result-value">
                    {saturacion}%
                </div>

                <span class="{clase_sat}">
                    {texto_sat}
                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.success(
        f"""
✅ Pacientes ubicados: {pacientes_ubicados}

✅ Total pacientes servicio: {total_pacientes}

✅ Ocupación: {ocupacion}%

✅ Saturación: {saturacion}%
"""
    )

st.markdown(
    """
    <div class="footer">
        Salud SURA · Panel SEM de Urgencias
    </div>
    """,
    unsafe_allow_html=True,
)
