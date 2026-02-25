from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_service import agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_history = []

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(msg: Message):
    global chat_history
    
    reply = agent(msg.text, chat_history)
    
    chat_history.append({"role": "user", "content": msg.text})
    chat_history.append({"role": "assistant", "content": reply})
    chat_history = chat_history[-8:] 
    
    return {"reply": reply}