import os
from pathlib import Path
import streamlit as st
from app import PROJECT_ROOT, build_agent

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

@st.cache_resource
def get_agent():
    return build_agent(rebuild_index=False)

def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.agent_blocked = False

def extract_tools_used(intermediate_steps) -> str:
    if not intermediate_steps:
        return "Conocimiento general (LLM)"
    
    # Extraemos los nombres de todas las herramientas ejecutadas en la consulta
    tools_used = set(action.tool for action, _ in intermediate_steps)
    
    # Mapeamos los nombres de las herramientas
    tools = []
    for tool_name in tools_used:
        if "rag" in tool_name.lower() or "pdf" in tool_name.lower() or "vector" in tool_name.lower():
            tools.append("RAG")
        elif "search" in tool_name.lower() or "web" in tool_name.lower() or "google" in tool_name.lower():
            tools.append("WEB")
        else:
            tools.append(tool_name) # Nombre por defecto si es otra herramienta
    
    # Se devuelve una unica cadena con todas las herramientas
    return ", ".join(tools)

def run_cache_agent(agent, question: str) -> str:
    output_dict = agent.invoke({'input': question})

    response = output_dict["output"]
    steps = output_dict.get("intermediate_steps", [])

    tools = extract_tools_used(steps)

    return {
        "response": response,
        "tools": tools
    }

################################################################################################################

def main() -> None:

    st.set_page_config(page_title="Agente IA e-commerce", layout="centered")

    st.title("Agente de IA para E-commerce")
    st.caption("Consulta documentos internos (RAG) y WEB")
    st.markdown("---")

    with st.sidebar:
        st.header("Configuracion")

        st.info("Para poder realizar consultas deberas tener correctamente configuradas las variables de entorno en tu archivo .env ")

        if st.button("Limpiar chat"):
            reset_chat()
            st.rerun()

        st.markdown("---")

        st.header("Documentos")

        st.info("Suba los archivos PDF's a continuacion para construir la base de conocimientos")

        #########################
        
        pdf_dir = _get_pdfs_dir()

        #########################

        uploaded_files = st.file_uploader(label='' ,type=["pdf"], accept_multiple_files=True)
        submitted = st.button("Construir indice")

        st.markdown("---")

        st.header("Avisos")

        if uploaded_files and submitted:
            new_files = False
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
                    new_files = True

                else:
                    st.info(f"'{file.name}' ya existia en el sistema.")

            if new_files:
                with st.spinner("Construyendo indice..."):
                    build_agent(rebuild_index=True)
                st.cache_resource.clear()
                st.rerun()

            else:
                st.warning(f"No se agrego ningun archivo nuevo")

    ######################################################################################
    
    # Variable de sesion de historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial de chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):

            if message["role"] == "assistant" and "tools_used" in message:
                st.success(f"*Herramientas utilizadas*: **{message['tools_used']}**")
                st.markdown(message['content'])

            else:
                st.markdown(message['content'])

    if prompt := st.chat_input("Haz una pregunta sobre e-commerce..."):
        
        # Mostrar nuevo mensaje en pantalla
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Agregar nuevo mensaje en historial
        st.session_state.messages.append({"role": "user", "content": prompt})


        with st.chat_message("ai"):
            with st.spinner("Pensando..."):
                try:
                    # Generar respuesta IA
                    agent = get_agent()
                    result = run_cache_agent(agent, question= prompt)

                    tools_used = result.get("tools", "N/D") # Herramientas usadas para responder
                    response = result.get("response", "") # Respuesta final generada
                    
                    st.success(f"*Herramientas utilizadas*: **{tools_used}**")
                    st.markdown(response)

                    # Agregar respuesta en el historial
                    st.session_state.messages.append({
                        "role": "assistant",
                        "tools_used": tools_used,
                        "content": response
                    })

                except Exception as exc:
                    # Mostrar error ocurrido en la generacion de respuesta
                    error_msg = f"Error ejecutando el agente: {exc}"
                    st.error(error_msg)

                    # Guardar mensaje de error en el historial de chat
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

                    

if __name__ == "__main__":
    main()