from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import ollama
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_KEY = os.getenv("API_KEY")
app = FastAPI()

# Add CORS middleware to allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Explicitly allow localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def verify_api(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API request")
    return x_api_key

async def generate_response(prompt: str):
    # Assuming ollama.chat is a blocking call, you may need to run it in a thread
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, ollama.chat, "tinyllama", [{"role": "user", "content": prompt}])
    
    # If the response is a single message, yield it directly
    yield response["message"]["content"]

@app.post("/generate")
async def generate(request: dict, x_api_key: str = Depends(verify_api)):
    prompt = request.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # Use the same logic as in generate_response
    response = await generate_response(prompt)
    return {"response": response}

@app.post("/generate-live")
async def generate_live(request: dict, x_api_key: str = Depends(verify_api)):
    prompt = request.get("prompt", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    return StreamingResponse(generate_response(prompt), media_type="text/event-stream")

