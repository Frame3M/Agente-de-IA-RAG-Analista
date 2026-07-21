import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate 
from datetime import datetime
from langchain_classic.agents import AgentExecutor, create_react_agent
from herramientas import crear_herramientas

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_PDF_DIR = PROJECT_ROOT / "sandbox_files"
DEFAULT_INDEX_DIR = PROJECT_ROOT / "data" / "faiss_index"

load_dotenv()

################################################################################################################

def _get_gemini_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY")

def _load_pdfs(pdf_dir: Path):

    pdf_files = sorted(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        raise RuntimeError(f"No se encontraron archivos PDF en {pdf_dir}")
    
    docs = []

    for pdf in pdf_files:
        loader = PyPDFLoader(file_path= str(pdf))
        docs.extend(loader.load())

    return docs

def _get_index_dir() -> Path:

    configured = os.getenv("FAISS_INDEX_DIR")

    index_dir = Path(configured) if configured else DEFAULT_INDEX_DIR

    if not index_dir.is_absolute():
        
        index_dir = (PROJECT_ROOT / index_dir).resolve()

    return index_dir

def _get_pdfs_dir() -> Path:

    configured = os.getenv("PDFS_DIR")

    pdfs_dir = Path(configured) if configured else DEFAULT_PDF_DIR

    if not pdfs_dir.is_absolute():

        pdfs_dir = (PROJECT_ROOT / pdfs_dir).resolve()

    if not pdfs_dir.exists():

        raise FileNotFoundError(f"No existe la carpeta para archivos pdf: {pdfs_dir}")
    
    return pdfs_dir


def _build_or_load_vectorstore(embedding_model: GoogleGenerativeAIEmbeddings, rebuild: bool = False):

    index_dir = _get_index_dir()
    index_faiss = index_dir / "index.faiss"
    index_pkl = index_dir / "index.pkl"

    if not rebuild and index_faiss.exists() and index_pkl.exists():
        
        return FAISS.load_local(
            folder_path= index_dir,
            embeddings= embedding_model,
            allow_dangerous_deserialization= True
        )
    
    print("Reconstruyendo Vectorstore...\n")
    
    pdfs_dir = _get_pdfs_dir()
    pdf_docs = _load_pdfs(pdfs_dir)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap= 100
    )

    chunks = splitter.split_documents(pdf_docs)

    vectorstore = FAISS.from_documents(documents= chunks, embedding= embedding_model)
    vectorstore.save_local(index_dir)

    return vectorstore


################################################################################################################

def build_agent(rebuild_index: bool = False):

    gemini_api_key = _get_gemini_api_key()
    llm_model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    embedding_model_name = os.getenv("EMBEDDING_GEMINI_MODEL", "gemini-embedding-001")

    llm_model = ChatGoogleGenerativeAI(
        model= llm_model_name,
        temperature= 0,
        google_api_key= gemini_api_key,
        max_retries=0
    )

    embedding_model = GoogleGenerativeAIEmbeddings(
        model= embedding_model_name,
        api_key= gemini_api_key
    )

    vectorstore = _build_or_load_vectorstore(embedding_model= embedding_model, rebuild= rebuild_index)

    tools = crear_herramientas(vectorstore)
    fecha_actual = datetime.now().strftime("%B %Y")

    template_prompt =   """
                        Eres un asistente analítico y experto en E-commerce que responde en castellano. 
                        Tu objetivo es responder las dudas del usuario con la mayor precisión posible.

                        NOTA IMPORTANTE: La fecha actual es {fecha_actual} asi que si necesitas responder preguntas
                        basadas en el tiempo debes tener en cuenta esto.

                        Para responder la pregunta del usuario, tienes acceso a las siguientes herramientas:

                        {tools}

                        Usa el siguiente formato de manera obligatoria y estricta:
                        Question: La pregunta de entrada que debes responder.
                        Thought: Debes siempre pensar en lo que debes hacer.
                        Action: La acción que será ejecutada, debe ser una de las siguientes opciones exactas: [{tool_names}]
                        Action Input: La entrada exacta para la acción.
                        Observation: El resultado devuelto por la herramienta.
                        ... (este ciclo se puede repetir)
                        Thought: Ahora sé la respuesta final.
                        Final Answer: La respuesta final redactada de forma amigable en castellano.

                        ¡Comienza!
                        Question: {input}
                        Thought: {agent_scratchpad}
                        """

    prompt_react = PromptTemplate(
        input_variables= ['input', 'agent_scratchpad', 'tools', 'tool_names'],
        partial_variables= {'fecha_actual': fecha_actual},
        template= template_prompt
    )

    agente = create_react_agent(llm= llm_model, tools= tools, prompt= prompt_react)
    orquestador = AgentExecutor(agent= agente, tools= tools, verbose= False, handle_parsing_errors= True)

    return orquestador

################################################################################################################

def run_agent(question: str) -> str:
    agent = build_agent(rebuild_index= False)

    output_dict = agent.invoke({'input': question})

    final_answer = output_dict["output"]

    return final_answer

################################################################################################################

def main() -> None:

    #print(run_agent("Cuales son las conduciones para aceptar una devolucion?"))

    question = input("Ingresa una pregunta: ").strip().lower()

    if question != 'exit':
        result = run_agent(question)
        print("=" * 50)
        print(result)
        print("=" * 50)

    while True:
        question = input("Ingresa una pregunta: ").strip().lower()

        if question == 'exit':
            break

        result = run_agent(question)
        print("=" * 50)
        print(result)
        print("=" * 50)

    return

################################################################################################################

if __name__ == "__main__":
    main()