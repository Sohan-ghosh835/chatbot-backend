from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Enable CORS for frontend (e.g., GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your GitHub Pages domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")

        if not user_message:
            return {"response": "❗ Empty message received."}

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response['choices'][0]['message']['content']
        return {"response": reply}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
