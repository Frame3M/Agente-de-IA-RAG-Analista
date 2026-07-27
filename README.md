# Agente AI E-commerce

Agente de inteligencia artificial desarrollado como proyecto para el Challenge de Alura Agente 2026. 

---

## 📝 Descripcion

Este proyecto implementa un agente de Inteligencia Artificial avanzado (arquitectura ReAct) diseñado para responder consultas sobre e-commerce, políticas de devoluciones, productos e información general en tiempo real. 

El agente es capaz de razonar y decidir dinámicamente qué herramienta utilizar según la pregunta del usuario:
* **Base de datos de conocimiento (RAG):** Consulta documentos PDF internos subidos por el usuario.
* **Búsqueda Web en tiempo real:** Utiliza motores de búsqueda para responder sobre precios actuales, noticias o eventos actualizados.
* **Transparencia en respuestas:** Indica en la interfaz qué herramienta/fuente fue consultada para dar cada respuesta.

### 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python
* **Interfaz Gráfica:** Streamlit
* **Orquestación de IA:** LangChain / ReAct Agent
* **Modelos de Lenguaje:** Google Gemini API
* **Búsqueda Web:** SerpAPI / Tavily
* **Procesamiento de Documentos:** PyPDF / Vector Stores (FAISS)

### 🚀 Características Principales

- **Carga dinámica de PDFs:** Gestión e indexación de archivos locales desde la barra lateral con capacidad para agregar/eliminar documentos.
- **Razonamiento dinámico (ReAct):** El agente evalúa si necesita consultar documentos internos, buscar en la web o responder con su conocimiento general.
- **Identificación de Fuentes:** Renderizado visual de la herramienta utilizada en cada mensaje del chat.
- **Salida Formateada:** Genera respuestas automáticas en Markdown.

---

## ⚙️ Instalación y Configuración Local

### 🔧 Instalacion

**1. Clonar el repositorio**

```
git clone https://github.com/Frame3M/Agente-de-IA-RAG-Analista.git
```

**2. Instalar dependencias necesarias**

```
pip install -r requirements.txt
```

**3. Configurar variables de entorno**

Crea un archivo .env en la raíz del proyecto (o configura un `.streamlit/secrets.toml`) con tus credenciales:

```python
GEMINI_API_KEY=tu_api_key_aqui # (Obligatorio)
```

### ▶️ Comandos de uso

```python
# 1) Ejecutar mediante CLI
python app.py

# 2) Iniciar interfaz interactiva de streamlit (http://localhost:8501)
streamlit run streamlit_app.py
```

---

# Ejemplos de preguntas y respuestas

## Ejemplo 1

*Se utilizo documentos de politicas internas de empresa ficticia BimBam Buy para este ejemplo*

### Pregunta
> Cuales son las politicas de devolucion?

### Respuesta
> *Herramientas utilizadas:* **RAG**
>
> ¡Hola! Con gusto te informo sobre las políticas de devolución de BimBam Buy. Para que una devolución sea aceptada, el producto debe cumplir con los siguientes requisitos:
>
> * Documentación: Debes contar con el comprobante de compra o número de orden.
> * Plazos: La solicitud debe presentarse dentro del plazo establecido.
> * Estado del producto: El artículo debe estar completo, incluyendo todos sus accesorios, manuales y obsequios promocionales si los hubiera.
>
> Consideraciones importantes:
>
> * Canales oficiales: Las solicitudes deben gestionarse exclusivamente a través del Centro de ayuda en la web, el formulario de postventa, el chat de soporte o el correo de atención al cliente. No se aceptan solicitudes por redes sociales o canales no oficiales.
> * Excepciones: No aplican devoluciones para productos personalizados (salvo falla de fábrica), productos con sellos de seguridad o higiene alterados, casos fuera de plazo, o situaciones de fraude.
> * Reembolsos: Se procesan al mismo medio de pago utilizado originalmente, salvo que exista una imposibilidad técnica.
> * Garantías: Si el producto presenta una falla después de la entrega, primero se evaluará bajo el Manual de Garantía de Productos antes de proceder con una devolución.
>
> Si necesitas gestionar un caso específico, te recomiendo contactar a nuestro equipo a través de los canales oficiales mencionados. ¡Estamos aquí para ayudarte!

### Imagen prueba

<img width="1920" height="954" alt="ejemplo1" src="https://github.com/user-attachments/assets/8f462a06-dc7c-4467-882f-56997d5e030b" />

---

## Ejemplo 2

### Pregunta
> ¿Cuáles son las fechas confirmadas para el próximo Hot Sale o CyberMonday este año y qué tiendas principales van a participar?

### Respuesta
> *Herramientas utilizadas:* **Consultar en internet**
>
> ¡Hola! Como estamos en julio de 2026, te confirmo la información actualizada sobre los eventos de e-commerce más importantes:
> * Hot Sale 2026: Este evento ya ha tenido lugar este año; se llevó a cabo del 11 al 13 de mayo de 2026.
> * CyberMonday 2026: Las fechas oficiales ya han sido confirmadas por la CACE (Cámara Argentina de Comercio Electrónico). El evento se realizará los días 2, 3 y 4 de noviembre de 2026.
>
> Sobre las tiendas participantes: Aunque el listado oficial de marcas se publica más cerca de la fecha del evento en el sitio oficial de CyberMonday Argentina, históricamente participan las principales cadenas de retail, tecnología, indumentaria y servicios del país. Entre las tiendas que suelen
> liderar la participación se encuentran:
>
> * Retail y Electro: Mercado Libre, Frávega, Musimundo, Cetrogar, Samsung, Philips.
> * Moda y Deportes: Adidas, Nike, Puma, Dafiti.
> * Viajes y Servicios: Aerolíneas Argentinas, Despegar, Assist Card.
>
> Te recomiendo estar atento a partir del 19 de agosto, que es cuando se abre el proceso de inscripción para las empresas, lo que suele dar inicio a la comunicación oficial de las marcas que formarán parte de esta edición. ¡Espero que esta información te sea de gran utilidad para planificar tus
> compras!

### Imagen prueba

<img width="1920" height="954" alt="ejemplo2" src="https://github.com/user-attachments/assets/459de591-00ea-444b-9e26-931f528cb98e" />

