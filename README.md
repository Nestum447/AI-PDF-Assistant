# AI PDF Assistant

Aplicación Streamlit que permite subir un PDF y hacer preguntas sobre su contenido usando un LLM.

## Ejecutar localmente

```bash
pip install -r requirements.txt
```

Configura tu API key:

```bash
export OPENAI_API_KEY="tu_api_key"
```

En Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="tu_api_key"
```

Luego:

```bash
streamlit run app.py
```

## Desplegar en Streamlit Community Cloud

1. Sube estos archivos a un repositorio de GitHub.
2. En Streamlit Community Cloud selecciona el repositorio y `app.py`.
3. En **Settings > Secrets**, agrega:

```toml
OPENAI_API_KEY = "tu_api_key"
```

No subas la API key a GitHub.

## Importante

Esta es la versión 1: extrae el texto del único PDF y lo envía como contexto al LLM.

Para PDFs grandes, la siguiente versión debe usar RAG:
PDF -> chunks -> embeddings -> vector database -> búsqueda -> LLM.
