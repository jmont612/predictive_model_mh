import streamlit as st
import pickle
import numpy as np



st.title("Conoce tu estado de Salud Mental")
col1, col2 = st.columns(2)

# Cargar modelo
with open('XGBboost_model_salud_mental.pkl', 'rb') as f:
    model = pickle.load(f)

# Combo box para pat_suenio con valores internos numéricos
pat_suenio_opciones = {
    "Insomnio": 0,
    "Normal": 1,
    "Excesivo": 2
}

with col1:
    pat_suenio = st.selectbox(
        "Patrón de sueño",
        options=list(pat_suenio_opciones.keys())
    )
    peso = st.number_input("Peso (kg)", min_value=30, max_value=200, value=70)
    niv_col = st.number_input("Nivel de colesterol (mg/dL)", min_value=100, max_value=400, value=180)
    bmi = st.number_input("Índice de masa corporal (BMI)", min_value=10.0, max_value=60.0, value=25.0)
    niv_gluc = st.number_input("Nivel de glucosa (mg/dL)", min_value=50, max_value=400, value=100)
    dens_osea = st.number_input("Densidad ósea (g/cm²)", min_value=0.0, max_value=5.0, value=2.5)

with col2:
    vision = st.number_input("Agudeza visual", min_value=0.0, max_value=20.0, value=10.0)
    audicion = st.number_input("Nivel de audición (dB)", min_value=0.0, max_value=120.0, value=20.0)
    func_cogn = st.number_input("Función cognitiva", min_value=0.0, max_value=100.0, value=50.0)
    niv_estres = st.number_input("Nivel de estrés", min_value=0.0, max_value=10.0, value=5.0)
    contaminacion_expo = st.number_input("Exposición a contaminación", min_value=0.0, max_value=10.0, value=3.0)

pat_suenio_valor = pat_suenio_opciones[pat_suenio]

# Cuando el usuario hace clic en predecir:
if st.button("Predecir estado de salud mental"):
    X = np.array([
        pat_suenio_valor, peso, niv_col, bmi, niv_gluc,
        dens_osea, vision, audicion, func_cogn, niv_estres, contaminacion_expo
    ]).reshape(1, -1)

    pred = model.predict(X)
    estados = {0: "Excelente", 1: "Bueno", 2: "Regular", 3: "Deficiente"}
    estado_predicho = estados.get(pred[0], 'Desconocido')

    st.success(f"Predicción: {estado_predicho}")

    # Recomendaciones detalladas

    # Patrones de sueño
    if pat_suenio_valor == 0:
        st.warning("Patrón de sueño: Insomnio. Considera establecer rutinas regulares para dormir, evita pantallas antes de acostarte y consulta a un especialista si persiste.")
    elif pat_suenio_valor == 2:
        st.info("Patrón de sueño: Excesivo. Dormir demasiado puede afectar tu salud. Mantén un horario equilibrado y consulta si notas somnolencia diurna.")

    # Peso
    if peso > 100:
        st.info("Peso alto. Mantén una dieta equilibrada y realiza actividad física regularmente.")
    elif peso < 40:
        st.warning("Peso bajo. Evalúa tu alimentación y consulta a un nutricionista para asegurar un peso saludable.")

    # BMI
    if bmi >= 30:
        st.warning("Índice de masa corporal alto (obesidad). Esto puede afectar tu salud mental y física, busca asesoría médica.")
    elif bmi < 18.5:
        st.warning("Índice de masa corporal bajo (bajo peso). Puede afectar tu bienestar, considera consultar con un especialista.")

    # Nivel de colesterol
    if niv_col > 240:
        st.warning("Colesterol alto. Controla tu dieta y consulta con un médico para evitar riesgos cardiovasculares.")
    elif niv_col < 125:
        st.info("Colesterol bajo. Mantén una alimentación balanceada.")

    # Nivel de glucosa
    if niv_gluc > 126:
        st.warning("Nivel de glucosa alto. Podría indicar diabetes, consulta con un especialista.")
    elif niv_gluc < 70:
        st.warning("Nivel de glucosa bajo. Puede causar fatiga y mareos, mantén una alimentación adecuada.")

    # Densidad ósea
    if dens_osea < 2.0:
        st.warning("Densidad ósea baja. Considera ejercicios de fortalecimiento y consulta a un médico.")

    # Visión
    if vision < 6.0:
        st.info("Agudeza visual baja. Revisa tus hábitos visuales y considera una evaluación óptica.")

    # Audición
    if audicion > 40:
        st.info("Nivel de audición disminuido. Evita ruidos fuertes y consulta a un especialista si tienes problemas auditivos.")

    # Función cognitiva
    if func_cogn < 50:
        st.warning("Función cognitiva baja. Estimula tu mente con actividades, y consulta si notas deterioro progresivo.")

    # Nivel de estrés
    if niv_estres > 7:
        st.warning("Nivel de estrés alto. Practica técnicas de relajación, meditación y busca apoyo si es necesario.")

    # Exposición a contaminación
    if contaminacion_expo > 5:
        st.info("Alta exposición a contaminación. Busca ambientes con aire limpio y limita la exposición prolongada.")
