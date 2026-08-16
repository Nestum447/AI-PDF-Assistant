import streamlit as st
from pypdf import PdfReader
from openai import OpenAI

st.set_page_config(page_title="AI PDF Assistant", page_icon="📄")

st.title("📄 AI PDF Assistant")
st.write("Sube un PDF y haz preguntas sobre su contenido.")

# API key stored in Streamlit Secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("No se encontró OPENAI_API_KEY en Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

archivo = st.file_uploader("Sube un PDF", type=["pdf"])

if archivo is not None:
    reader = PdfReader(archivo)

    paginas = []
    texto_total = ""

    for numero, pagina in enumerate(reader.pages, start=1):
        texto = pagina.extract_text() or ""
        texto = texto.strip()

        if texto:
            paginas.append((numero, texto))
            texto_total += f"\n\n--- Página {numero} ---\n{texto}"

    if not texto_total:
        st.error(
            "No se encontró texto en el PDF. "
            "Puede ser un PDF escaneado y esta versión todavía no tiene OCR."
        )
        st.stop()

    st.success(f"PDF leído correctamente: {len(reader.pages)} páginas.")

    with st.expander("Ver texto extraído"):
        st.text_area("Texto del PDF", texto_total, height=350)

    pregunta = st.text_input(
        "Haz una pregunta sobre el PDF:",
        placeholder="Ejemplo: ¿Cuál es el procedimiento de devolución?"
    )

    if st.button("🔎 Preguntar", type="primary"):
        if not pregunta.strip():
            st.warning("Escribe una pregunta.")
            st.stop()

        # Esta versión usa el texto completo del PDF como contexto.
        # Más adelante la convertiremos en RAG con embeddings y búsqueda.
        contexto = texto_total[:100000]

        prompt = f"""
Eres un asistente que responde preguntas sobre un documento PDF.

REGLAS:
- Utiliza únicamente la información del CONTEXTO.
- No inventes información.
- Si la respuesta no aparece en el CONTEXTO, responde exactamente:
  "No encontré esa información en el documento."
- Cuando sea posible, indica la página donde encontraste la información.
- Responde en español.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}
"""

      try:
            with st.spinner("Analizando el documento..."):
                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

            st.subheader("Respuesta")
            st.write(response.output_text)

        except Exception as e:
            st.error(f"Error al consultar OpenAI: {e}")

