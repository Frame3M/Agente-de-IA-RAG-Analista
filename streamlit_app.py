import os
from pathlib import Path
import streamlit as st
from app import PROJECT_ROOT

DEFAULT_TEMPFILES_DIR = PROJECT_ROOT / "temp_files"

def _get_pdfs_dir() -> Path:

    configured = os.getenv("PDF_DIR")
    pdf_dir = Path(configured) if configured else DEFAULT_TEMPFILES_DIR
    
    if not pdf_dir.is_absolute():
        pdf_dir = (PROJECT_ROOT / pdf_dir).resolve()

    pdf_dir.mkdir(parents=True, exist_ok=True)

    return pdf_dir

def save_file(uploadedfile, destination_path: Path) -> Path:
    
    file_path = destination_path / uploadedfile.name

    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())

################################################################################################################

def main() -> None:
    st.set_page_config(page_title="Agente IA e-commerce", layout="centered")

    st.title("Agente de IA para E-commerce")
    st.caption("Consulta documentos internos (RAG) y WEB")


    pregunta = st.chat_input("Haz una pregunta sobre e-commerce...")

    with st.sidebar:
        st.header("Configuracion")

        st.info("Para poder realizar consultas deberas tener correctamente configuradas las variables de entorno en tu archivo .env ")

        if st.button("Limpiar chat"):
            pass

        st.markdown("---")

        st.header("Documentos")

        st.info("Suba los archivos PDF's a continuacion para construir la base de conocimientos")

        #########################
        
        pdf_dir = _get_pdfs_dir()

        #########################

        uploaded_files = st.file_uploader(label='' ,type=["pdf"], accept_multiple_files=True)
        submitted = st.button("Construir indice")

        if uploaded_files and submitted:
            unique_files = {}

            for file in uploaded_files:
                if file.name not in unique_files:
                    unique_files[file.name] = file
                else:
                    st.warning(f"El archivo '{file.name}' se econtraba duplicado en la seccion y fue ignorado.")

            for file in unique_files.values():
                
                file_path = pdf_dir / file.name
                
                if not file_path.exists():
                    save_file(file, pdf_dir)
                    st.success(f"Guardado '{file.name}.'")

                else:
                    st.info(f"'{file.name}' ya existia en el sistema.")


if __name__ == "__main__":
    main()