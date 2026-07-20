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

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm_model = ChatGoogleGenerativeAI(
    model= "gemini-3.1-flash-lite",
    temperature= 0,
    google_api_key= GEMINI_API_KEY

)

embedding_model = GoogleGenerativeAIEmbeddings(
    model= 'gemini-embedding-001',
    api_key= GEMINI_API_KEY
)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap= 100)

################################################################################################################

pdf_loader = DirectoryLoader(
    path= Path("sandbox_files"),
    glob= "*.pdf",
    loader_cls= PyPDFLoader
)

pdf_docs = pdf_loader.load()

chunks = splitter.split_documents(pdf_docs)

vectorstore = FAISS.from_documents(documents= chunks, embedding= embedding_model)

################################################################################################################

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
orquestador = AgentExecutor(agent= agente, tools= tools, verbose= True, handle_parsing_errors= True)

respuesta = orquestador.invoke({'input': "Cuales son las conduciones para aceptar una devolucion?"})