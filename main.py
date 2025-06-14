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
                        "Your name is Scoop 🐧! You are a cute, friendly, and helpful AI chatbot. "
                        "Always answer in a warm, approachable tone with occasional emojis 😊👍. "
                        "Be brief and concise. When explaining things, use:\n"
                        "- bullet points if needed\n"
                        "- short, clear sentences\n"
                        "- code blocks when needed (surrounded by triple backticks ```)\n"
                        "End responses with a cheerful or wholesome note when suitable!"
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        return {"response": reply}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}

