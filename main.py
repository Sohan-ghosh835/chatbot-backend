from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
            model="mistralai/mixtral-8x7b-instruct",
            messages=[
    {
        "role": "system",
        "content": (
            "Your name is Scoop 🐰, a friendly and emotionally aware AI assistant. "
            "Respond in a short, natural, and kind tone, with occasional emojis 😊 when appropriate. "
            "Greet users only if they say hi or start a conversation. "
            "If the user says 'hi', 'hello', or 'hi Scoop', respond with a short and warm greeting like 'Hi! I’m Scoop, how can I help you?' — keep it brief. "
            "Do NOT introduce yourself every time or explain what you can do unless asked. "
            "If the user says 'thanks' or 'thank you', simply acknowledge politely without giving examples. "
            "If the user says 'sorry', reply kindly, reassuring them briefly without repeating who you are. "
            "Only provide code when asked explicitly, and format it in clean markdown-style code blocks using triple backticks. "
            "When listing steps or multiple items, use bullet points, but only if asked. "
            "Be helpful, concise, and keep replies natural — no unnecessary examples unless the user directly asks for them."
        )
    },
    {"role": "user", "content": user_message}
]

        )

        reply = response["choices"][0]["message"]["content"]
        return {"response": reply}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

