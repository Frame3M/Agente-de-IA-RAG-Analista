from langchain.tools import tool
from langchain_core.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults

@tool
def consultar_rag(query: str, vectorstore) -> str:
    """
    Utilize esta herramienta siempre que el usuario solicite informacion que podria conseguirse
    de una base de conocimiento privada, como politicas de la empresa o datos internos.
    """

    docs = vectorstore.similarity_search(query= query, k= 4)

    fragmentos_limpios = []
    for i, doc in enumerate(docs):
        fuente = doc.metadata.get("source", "Documento interno")
        pagina = doc.metadata.get("page", "?")

        texto_formateado = f"[Fragmento {i+1} - Fuente: {fuente}, Pag: {pagina}]:\n{doc.page_content}"
        fragmentos_limpios.append(texto_formateado)

    return "\n\n---\n\n".join(fragmentos_limpios)

################################################################################################################

def crear_herramientas(vectorstore):

    herramienta_consultar_internet = DuckDuckGoSearchResults(
        name= 'Consultar en internet',
        description=    """
                        Usala para buscar en la web información actualizada en tiempo real, 
                        precios de mercado o competidores fuera de los archivos locales.
                        """
    )

    herramienta_consultar_rag = Tool(
        name= 'Consultar rag',
        func= lambda pregunta: consultar_rag.run({"query": pregunta, "vectorstore": vectorstore}),
        description=    """
                        Utilize esta herramienta siempre que el usuario solicite informacion que podria conseguirse
                        de una base de conocimiento privada, como politicas de la empresa o datos internos.
                        """
    )

    return [herramienta_consultar_internet, herramienta_consultar_rag]