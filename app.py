import streamlit as st
from google import genai

st.set_page_config(page_title="Copiloto de Scalping", page_icon="📈", layout="centered")
st.title("🤖 Copiloto IA - Análisis en Vivo")
st.caption("Asistente analítico enfocado en acción del precio, liquidez y temporalidades cortas.")

with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Ingresa tu Google API Key:", type="password")
    st.markdown("---")
    st.markdown("*Tu llave no se guarda en ningún servidor, solo se usa en esta sesión por seguridad.*")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

prompt = st.chat_input("Ej: EUR/USD en 5m. El RSI bajó de 30 y la EMA 9 cruzó la 21. ¿Qué opinas?")

if prompt:
    if not api_key:
        st.warning("⚠️ Por favor, ingresa tu API Key en el menú lateral izquierdo primero.")
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
        
        client = genai.Client(api_key=api_key)
        
        with st.chat_message("assistant"):
            mensaje_espera = st.empty()
            mensaje_espera.text("Analizando confluencias...")
            
            try:
                contexto_oculto = f"Eres un experto en scalping. Responde a esto de forma analítica y concisa: {prompt}"
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contexto_oculto
                )
                mensaje_espera.empty()
                st.markdown(respuesta.text)
                st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta.text})
                
            except Exception as e:
                mensaje_espera.empty()
                st.error(f"Hubo un error de conexión: {e}")
