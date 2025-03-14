from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
app = FastAPI()

def verify_api(x_api_key: str = Header(None)):
    print(API_KEY)
    print(x_api_key)
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401,detail="Invalid Api request,")
    return x_api_key


@app.post("/generate")
def generate(prompt: str, x_api_key:str = Depends(verify_api)):
    response = ollama.chat(model="deepseek-coder:6.7b", messages=[{"role":"user","content":prompt}])
    return {"response": response["message"]["content"]}
