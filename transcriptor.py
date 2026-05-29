import streamlit as st
import whisper
import os
import tempfile
from datetime import timedelta

st.set_page_config(page_title="Transcriptor IA - Anderson", page_icon="🎙️", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #2E86AB;'>🎙️ Transcriptor Inteligente con IA</h1>
    <p style='text-align: center; color: gray;'>Transcribe, traduce y analiza cualquier audio automáticamente</p>
    <hr>
""", unsafe_allow_html=True)

idiomas = {
    "Detección automática": None,
    "Español": "es",
    "Inglés": "en",
    "Portugués": "pt",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it"
}

traducciones = {
    "No traducir": None,
    "Traducir a Español": "es",
    "Traducir a Inglés": "en",
    "Traducir a Portugués": "pt",
    "Traducir a Francés": "fr"
}

col1, col2 = st.columns(2)
with col1:
    idioma = st.selectbox("🌎 Idioma del audio", list(idiomas.keys()))
with col2:
    traduccion = st.selectbox("🔄 Traducción", list(traducciones.keys()))

modelo = st.radio("⚙️ Precisión del modelo", ["base", "small", "medium"], horizontal=True)
timestamps = st.checkbox("⏱️ Mostrar timestamps por segmento")

audio = st.file_uploader("📂 Sube tu audio aquí", type=["mp3", "wav", "m4a", "ogg", "mp4"])

if audio:
    st.audio(audio, format="audio/mp3")

    if st.button("🚀 Transcribir Audio"):
        with st.spinner("⏳ La IA está procesando tu audio..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(audio.read())
                tmp_path = tmp.name

            model = whisper.load_model(modelo)

            opciones = {}
            if idiomas[idioma]:
                opciones["language"] = idiomas[idioma]
            if traducciones[traduccion]:
                opciones["task"] = "translate"

            result = model.transcribe(tmp_path, **opciones)
            os.unlink(tmp_path)

        st.success("✅ Transcripción completada")
        st.markdown("---")

        col3, col4, col5 = st.columns(3)
        palabras = len(result["text"].split())
        tiempo_lectura = round(palabras / 200)
        col3.metric("📝 Palabras", palabras)
        col4.metric("📖 Tiempo de lectura", f"{tiempo_lectura} min")
        col5.metric("🌎 Idioma detectado", result.get("language", "desconocido").upper())

        st.subheader("📝 Texto transcrito:")
        st.text_area("Resultado", result["text"], height=300)

        if timestamps and "segments" in result:
            st.subheader("⏱️ Transcripción por segmentos:")
            for seg in result["segments"]:
                inicio = str(timedelta(seconds=int(seg["start"])))
                fin = str(timedelta(seconds=int(seg["end"])))
                st.markdown(f"**[{inicio} → {fin}]** {seg['text']}")

        st.markdown("---")
        st.subheader("⬇️ Descargar transcripción")
        col6, col7 = st.columns(2)
        with col6:
            st.download_button(
                label="📄 Descargar como TXT",
                data=result["text"],
                file_name="transcripcion.txt",
                mime="text/plain"
            )
        with col7:
            contenido_word = f"TRANSCRIPCIÓN DE AUDIO\n{'='*40}\n\n{result['text']}\n\n{'='*40}\nDesarrollado por Anderson Ayala | 2026"
            st.download_button(
                label="📝 Descargar como Word",
                data=contenido_word,
                file_name="transcripcion.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Desarrollado por Anderson Ayala | 2026</p>", unsafe_allow_html=True)