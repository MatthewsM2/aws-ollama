from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import ollama
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
app = FastAPI()

# Add CORS middleware to allow all requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

def verify_api(x_api_key: str = Header(None)):
    #print(API_KEY)
    #print(x_api_key)
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401,detail="Invalid Api request,")
    return x_api_key


@app.post("/generate")
def generate(prompt: str, x_api_key:str = Depends(verify_api)):
    response = ollama.chat(model="tinyllama", messages=[{"role":"user","content":prompt}])
    return {"response": response["message"]["content"]}
