# import os
# import ssl
# os.environ['CURL_CA_BUNDLE'] = ''
# os.environ['PYTHONHTTPSVERIFY'] = '0'

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# import asyncio
# from dotenv import load_dotenv
# import gradio as gr

# from llama_index.core import VectorStoreIndex, Settings, PromptTemplate, get_response_synthesizer
# from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.llms.groq import Groq
# from llama_index.vector_stores.pinecone import PineconeVectorStore
# from pinecone import Pinecone

# from workflow import ProjectRAGWorkflow

# load_dotenv()

# Settings.embed_model = CohereEmbedding(
#     api_key=os.getenv("COHERE_API_KEY"),
#     model_name="embed-multilingual-v3.0"
# )

# Settings.llm = Groq(
#     model="llama-3.1-8b-instant", 
#     api_key=os.getenv("GROQ_API_KEY")
# )

# print("Connecting to Pinecone...")
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index_name = "project-agent-index"
# vector_store = PineconeVectorStore(pinecone_index=pc.Index(index_name))
# index = VectorStoreIndex.from_vector_store(vector_store)

# prompt_file_path = os.path.join("prompts", "rag.md")
# with open(prompt_file_path, "r", encoding="utf-8") as file:
#     qa_prompt_tmpl_str = file.read()
# qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

# retriever = index.as_retriever(similarity_top_k=5)
# response_synthesizer = get_response_synthesizer(
#     response_mode="compact",
#     text_qa_template=qa_prompt_tmpl,
#     llm=Settings.llm
# )

# async def chat_function(message, history):
#     try:
#         flow = ProjectRAGWorkflow(
#             retriever=retriever, 
#             synthesizer=response_synthesizer,
#             timeout=60
#         )
        
#         result = await flow.run(query=message)
        
#         return str(result)
        
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return f"אופס, קרתה שגיאה בתהליך: {str(e)}"

# demo = gr.ChatInterface(
#     fn=chat_function,
#     title="Agent Analysis System (Event-Driven) 🤖",
#     description="מערכת RAG מבוססת Workflow שמנתחת את מסמכי הפרויקט עם בדיקות ולידציה.",
# )

# if __name__ == "__main__":
#     from llama_index.utils.workflow import draw_all_possible_flows
#     print("Generating workflow graph...")
#     workflow_instance = ProjectRAGWorkflow(
#         retriever=retriever, 
#         synthesizer=response_synthesizer
#     )
    
#     draw_all_possible_flows(workflow_instance, filename="workflow_graph.html")
    
#     print("✅ Workflow graph generated: workflow_graph.html")
#     demo.launch(server_port=5000)

import os
import ssl
import asyncio
from dotenv import load_dotenv
import gradio as gr

# --- הגדרות SSL והמערכת המקוריות שלך (ללא שינוי) ---
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from llama_index.core import VectorStoreIndex, Settings, PromptTemplate, get_response_synthesizer
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from workflow import ProjectRAGWorkflow

load_dotenv()

Settings.embed_model = CohereEmbedding(
    api_key=os.getenv("COHERE_API_KEY"),
    model_name="embed-multilingual-v3.0"
)

Settings.llm = Groq(
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,
    max_tokens=600,
    top_p=0.1
)

print("Connecting to Pinecone...")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "project-agent-index"
vector_store = PineconeVectorStore(pinecone_index=pc.Index(index_name))
index = VectorStoreIndex.from_vector_store(vector_store)

prompt_file_path = os.path.join("prompts", "rag.md")
with open(prompt_file_path, "r", encoding="utf-8") as file:
    qa_prompt_tmpl_str = file.read()
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

retriever = index.as_retriever(similarity_top_k=5)
response_synthesizer = get_response_synthesizer(
    response_mode="refine",
    text_qa_template=qa_prompt_tmpl,
    llm=Settings.llm
)

async def chat_function(message, history):
    try:
        flow = ProjectRAGWorkflow(
            retriever=retriever, 
            synthesizer=response_synthesizer,
            timeout=60
        )
        result = await flow.run(query=message)
        final_text = str(result)
        source_files = set()
        if hasattr(result, 'source_nodes') and result.source_nodes:
            for node in result.source_nodes:
                file_name = node.metadata.get('file_name', 'Unknown')
                source_files.add(file_name)
        if source_files:
            sources_str = ", ".join(source_files)
            return f"{final_text}\n\n<br><small style='color: gray; border-top: 1px solid #ddd; display: block; padding-top: 5px;'>🔍 המידע נשלף מתוך: {sources_str}</small>"
        return final_text
    except Exception as e:
        print(f"DEBUG: Error occurred: {e}")
        return f"אופס, קרתה שגיאה בתהליך: {str(e)}"
    
# --- CSS למרכוז מלא ותמונת רקע עובדת ---
custom_css = """
body, .gradio-container {
background-image: url('http://parashat.co.il/wp-content/uploads/2023/09/shlomo0355_Beautiful_sunset_backgrounds_colorful_watercolor_sty_2b834925-e8eb-4505-9091-b750f92740df.png') !important;    background-size: cover !important;
    height: 100vh !important;
    width: 100vw !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    direction: rtl !important;
}

#main-box {
    background: rgba(255, 255, 255, 0.4) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 30px !important;
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    padding: 40px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
    max-width: 850px !important;
    width: 90% !important;
    display: flex !important;
    flex-direction: column !important;
    align-self: center !important;
    margin-top:10vh !important;
}
.chatbot .message, .message-content {
    direction: rtl !important;
    text-align: right !important;
    unicode-bidi: plaintext !important; /* זה יגרום לכל פסקה להחליט על הכיוון לפי השפה שלה */
}
small {
    display: block;
    margin-top: 10px;
    font-size: 0.85em !important;
    opacity: 0.8;
    border-top: 1px solid rgba(0,0,0,0.1);
    padding-top: 5px;
}
.credit { text-align: center; color: #555; font-weight: 600; margin-bottom: 5px; }
h1 { text-align: center; color: #333; margin-top: 0; }
.chatbot .message { text-align: right !important; }
footer { display: none !important; }
"""

with gr.Blocks() as demo:
    # עטיפה של הכל בתוך Column אחד ממורכז
    with gr.Column(elem_id="main-box"):
        gr.Markdown("פותח ע\"י אילה אלבוגן", elem_classes="credit")
        gr.Markdown("# Agent Analysis System 🤖")
        
        gr.ChatInterface(
            fn=chat_function,
            chatbot=gr.Chatbot(height=450, show_label=False),
        )

if __name__ == "__main__":
    from llama_index.utils.workflow import draw_all_possible_flows
    workflow_instance = ProjectRAGWorkflow(retriever=retriever, synthesizer=response_synthesizer)
    draw_all_possible_flows(workflow_instance, filename="workflow_graph.html")
    
    # הרצה עם ה-CSS וה-Theme בתוך launch
    demo.launch(server_port=5000, css=custom_css, theme=gr.themes.Soft())