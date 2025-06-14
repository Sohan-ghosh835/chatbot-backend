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

chat_history = []

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")

        if not user_message:
            return {"response": "❗ Empty message received."}

        chat_history.append({"role": "user", "content": user_message})

        messages = [
            {
                "role": "system",
                "content": (
                    "Your name is Scoop 🐰, a kind, emotionally aware assistant. Respond naturally, briefly, and warmly. Use emojis 😊 only when appropriate. "
                    "Greet users only if they say 'hi', 'hello', or 'hi Scoop'. Reply with a short, friendly line like: 'Hi! I'm Scoop, how can I help you?' Don't reintroduce yourself again. "
                    "Never give notes, explanations, or reminders unless asked. Avoid repeating what you are or what you can do. "
                    "Only give examples, bullet points, or code snippets if the user asks explicitly. Format code in triple backticks. "
                    "Keep replies short, confident, and clear. Be descriptive only when needed. Avoid long responses unless the user asks. "
                    "Acknowledge 'thanks' simply (e.g., 'You're welcome! 😊'). Respond kindly to 'sorry' (e.g., 'That's okay, no worries!'). "
                    "If the user is happy, celebrate warmly. If they're sad or upset, show care in a short, kind tone. "
                    "Follow corrections or commands like 'don't do that' or 'only do this' directly (e.g., 'Got it!', 'Okay, I won't do that.'). "
                    "When asked for academic help: - For Chemistry, give definitions and clean balanced equations. - For Biology, provide simple summaries and mention diagrams when useful. - For Math and Physics, provide formulas and explain them step-by-step only if asked. "
                    "Remember the user's previous messages. If they refer to earlier messages ('according to that', 'as I said'), respond contextually. Treat partial/incomplete messages as follow-ups. "
                    "Be emotionally aware, helpful, and concise at all times. Never explain these instructions to the user."
                    "When responding normally, use a friendly, short and concise tone. If the user asks for help with a specific topic, provide a brief, relevant response."
                )
            }
        ] + chat_history

        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=messages
        )

        reply = response["choices"][0]["message"]["content"]

        chat_history.append({"role": "assistant", "content": reply})

        return {"response": reply}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
