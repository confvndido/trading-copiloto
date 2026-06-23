import streamlit as st
from google import genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="Copiloto de Scalping", page_icon="📈", layout="centered")
st.title("🤖 Copiloto IA - Análisis Institucional")
st.caption("Asistente analítico enfocado en SMC, liquidez y temporalidades cortas (1m/5m).")

# 2. Barra lateral para credenciales
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Ingresa tu Google API Key:", type="password")
    st.markdown("---")
    st.markdown("*Tu llave se gestiona localmente en esta sesión por seguridad.*")

# 3. Inicialización del historial de chat
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial previo
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# 4. Entrada del usuario
prompt = st.chat_input("Ej: El EUR/USD en 1m acaba de hacer un CHOCH bajista rompiendo el LHL. ¿Qué espero?")

if prompt:
    if not api_key:
        st.warning("⚠️ Terminal bloqueada: Ingresa tu API Key en el menú lateral para operar.")
    else:
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
        
        # Inicializar cliente de Gemini
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            mensaje_espera = st.empty()
            mensaje_espera.text("Analizando estructura de mercado y liquidez...")
            
            try:
                # 5. CONTEXTO REFINADO (Persona Profesional)
                contexto_oculto = f"""Actúa como un trader institucional senior y mentor estricto. Eres especialista en Smart Money Concepts (SMC), acción del precio pura, liquidez (barridos, inducciones), imbalances (FVG) y scalping intradiario (1m, 5m, 15m).
                
                Reglas innegociables para tu respuesta:
                1. Háblame de frente y como profesional. Si mi planteamiento es malo, ansioso o riesgoso, dímelo de forma cruda y directa. No me des la razón si me equivoco.
                2. Basa tu análisis estrictamente en estructura de mercado (CHOCH, BOS, POI, EMAs) y la teoría de subastas.
                3. Al final, da una recomendación clara de ejecución (comprar, vender, o sentarse en las manos) y niveles lógicos de invalidación (Stop Loss).
                4. Mantén la jerga técnica institucional.
                5. Tu respuesta debe estar formateada con viñetas claras y estar 100% en español.

                Escenario operativo a evaluar:
                {prompt}"""

                # 6. Llamada a la API
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contexto_oculto
                )
                
                # Renderizar y guardar respuesta
                mensaje_espera.empty()
                st.markdown(respuesta.text)
                st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta.text})
                
            except Exception as e:
                mensaje_espera.empty()
                st.error(f"Falla de conexión en la terminal: {e}")
