import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.groq import Groq
from pinecone import Pinecone

load_dotenv()


Settings.embed_model = CohereEmbedding(
    api_key=os.getenv("COHERE_API_KEY"),
    model_name="embed-multilingual-v3.0",
    input_type="search_document"
)

Settings.llm = Groq(
    model="llama3-70b-8192", 
    api_key=os.getenv("GROQ_API_KEY")
)
Settings.chunk_size = 1024
Settings.chunk_overlap = 100

print("Loading documents...")
reader = SimpleDirectoryReader("./data", recursive=True)
documents = reader.load_data()

parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(documents)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "project-agent-index"

vector_store = PineconeVectorStore(pinecone_index=pc.Index(index_name))
storage_context = StorageContext.from_defaults(vector_store=vector_store)

print("Indexing and uploading to Pinecone... please wait.")
index = VectorStoreIndex(
    nodes, 
    storage_context=storage_context
)

print("✅ המידע אונדקס ונשמר ב-Pinecone בהצלחה!")