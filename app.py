import streamlit as st
from pypdf import PdfReader
from openai import OpenAI

st.set_page_config(page_title="AI PDF Assistant", page_icon="📄", layout="wide")

st.title("📄 AI PDF Assistant")
st.caption("Pregunta sobre un PDF usando un LLM. La respuesta se basa únicamente en el texto extraído del documento.")

api_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY")) if False else None

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.warning("Configura OPENAI_API_KEY en Streamlit Secrets o como variable de entorno.")
    st.stop()

client = OpenAI(api_key=api_key)

archivo = st.file_uploader("Sube un PDF", type=["pdf"])

if archivo:
    try:
        reader = PdfReader(archivo)
        paginas = []
        texto_total = ""

        for numero, pagina in enumerate(reader.pages, start=1):
            texto = pagina.extract_text() or ""
            texto = texto.strip()
            paginas.append({"pagina": numero, "texto": texto})
            if texto:
                texto_total += f"\n\n--- Página {numero} ---\n{texto}"

        st.success(f"PDF leído correctamente: {len(reader.pages)} páginas.")

        paginas_con_texto = [p for p in paginas if p["texto"]]

        if not paginas_con_texto:
            st.error(
                "No se encontró texto en este PDF. Puede ser un PDF escaneado; "
                "esta primera versión todavía no incluye OCR."
            )
            st.stop()

        with st.expander("Ver texto extraído"):
            st.text_area("Texto", texto_total, height=400)

        pregunta = st.text_input(
            "Haz una pregunta sobre el PDF:",
            placeholder="Ejemplo: ¿Cuál es el procedimiento de devolución?"
        )

        if st.button("🔎 Preguntar", type="primary") and pregunta.strip():
            # Esta primera versión envía el texto completo al LLM.
            # Después podemos convertirla en RAG con embeddings/vector DB.
            limite_caracteres = 100_000
            contexto = texto_total[:limite_caracteres]

            prompt = f"""
Eres un asistente especializado en responder preguntas sobre documentos.

REGLAS:
1. Utiliza únicamente la información contenida en el CONTEXTO.
2. No inventes datos.
3. Si la respuesta no aparece claramente en el CONTEXTO, responde:
   "No encontré esa información en el documento."
4. Si es posible, indica la página donde encontraste la información.
5. Responde en español de forma clara y concisa.

CONTEXTO DEL PDF:
{contexto}

PREGUNTA DEL USUARIO:
{pregunta}
"""

            with st.spinner("Analizando el documento..."):
                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

            st.subheader("Respuesta")
            st.write(response.output_text)

            st.info(
                "Nota: esta versión usa el PDF completo como contexto. "
                "El siguiente paso sería convertirla en RAG, para buscar solo "
                "los fragmentos relevantes antes de llamar al LLM."
            )

else:
    st.info("Sube un PDF para comenzar.")
