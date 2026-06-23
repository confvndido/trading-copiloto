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
                contexto_oculto = f"I require an analytical trading assessment focused on scalping and intraday strategies, utilizing real-time data from the following sources: https://www.forexfactory.com/calendar and https://es.tradingview.com/symbols/EURUSD/. The analysis should include the following sections:

1. Current market sentiment regarding the EUR/USD currency pair.
2. Key economic events from the Forex Factory calendar that may impact trading decisions, including their dates and expected outcomes.
3. Technical analysis of the EUR/USD chart on TradingView, highlighting significant support and resistance levels, as well as potential trading signals.
4. Recommendations for entry and exit points based on the gathered data.

Ensure the assessment is concise and analytical, focusing on actionable insights for scalping and intraday trading. Avoid overly complex jargon to maintain clarity, and provide references to the specific data points analyzed.

For context, I have a background in trading but am looking for advanced inI require an analytical assessment of the current trading conditions for the EUR/USD currency pair, utilizing live data from https://www.forexfactory.com/calendar and https://es.tradingview.com/symbols/EURUSD/. Please provide the following structured information:

1. Summary of the current economic indicators affecting the EUR/USD pair, including relevant data from the Forex Factory calendar.
2. A technical analysis based on the latest price action observed on TradingView, including key support and resistance levels.
3. An evaluation of market sentiment and its potential impact on short-term trading strategies (scalping and intraday).

Ensure that the analysis reflects real-time data and is concise, focusing on actionable insights for traders. Avoid speculative claims and unsupported opinions, relying instead on the most recent and reliable market data.

I have a solid understanding of trading concepts but seek to enhance my strategy with precise, data-driven insights. The tone should be professional and geared towards traders looking for immediate guidance. Habla en español. Cumple con el siguiente promopt: {prompt}"
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
