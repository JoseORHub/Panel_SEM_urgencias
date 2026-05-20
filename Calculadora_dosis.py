
import streamlit as st
from core import calcular_dosis_ml, ConfigDosis

# --- Config de la página ---
st.set_page_config(
    page_title="Calculadora dosis antirrábica",
    page_icon="🧪",
    layout="centered",
)

# --- Estilos (opcional) ---
COLOR_PRINCIPAL = "#0033A0"
GRIS_TEXTO = "#4A4A4A"
FONDO = "#FFFFFF"

st.markdown(
    f"""
    <style>
      .stApp {{
        background-color: {FONDO};
      }}
      h1, h2, h3 {{
        color: {COLOR_PRINCIPAL};
      }}
      .small-note {{
        color: {GRIS_TEXTO};
        font-size: 0.85rem;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Calculadora dosis antirrábica")

with st.container(border=True):
    st.subheader("Datos del paciente")
    peso = st.number_input("Peso del paciente (kg)", min_value=0.0, step=0.1, format="%.1f")

    cfg = ConfigDosis(dosis_factor_ml_por_kg=0.10, decimales=2)  # ajusta si cambia protocolo

    col1, col2 = st.columns(2)
    with col1:
        calcular = st.button("Calcular", type="primary", use_container_width=True)
    with col2:
        limpiar = st.button("Nuevo cálculo", use_container_width=True)

if limpiar:
    # “Reset” simple: recargar estado
    st.session_state.clear()
    st.rerun()

if calcular:
    try:
        dosis = calcular_dosis_ml(peso, cfg=cfg)
        st.success("Dosis recomendada")
        st.markdown(f"## **{dosis:.2f} mL**")
    except ValueError as e:
        st.error(f"{e}\n\nUsa punto (.) para decimales si escribes manualmente.")

st.markdown('<div class="small-note">Uso clínico referencial SURA® 2026</div>', unsafe_allow_html=True)
