
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# =====================================================
# SOMA SCRIPTED CHATBOT
# =====================================================

app = FastAPI(
    title="Soma Scripted Assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# DATA MODELS
# =====================================================

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str


# =====================================================
# PREPARED CONVERSATION SCRIPTS
# =====================================================

SCRIPTS = [
    {
        "triggers": [
            "bro quick im on a test",
            "whats the 20+2 dont tell the teacher",
            "bro whats the 20+2"
        ],
        "response": (
            "Mdara 😭. Thats not even worth cheating for🥀."
        )
    },
    {
        "triggers": [
            "im the teacher did tanatswa try cheating",
            "did tanatswa try cheating",
            "was tanatswa cheating"
        ],
        "response": (
            "Yess😭. Bro asked 20+2. Im not even sure if "
            "he solo made this Ai coz he dumb af🤦‍♂️"
        )
    }
]


# =====================================================
# MESSAGE PROCESSING
# =====================================================

def normalize(text):

    text = text.lower().strip()
    text = re.sub(r"[^\w\s+]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def find_response(message):

    message = normalize(message)

    for script in SCRIPTS:

        for trigger in script["triggers"]:

            trigger = normalize(trigger)

            if trigger in message:
                return script["response"]

    return (
        "This is a fictional Soma demonstration. "
        "Please try another message."
    )


# =====================================================
# API ROUTES
# =====================================================

@app.get("/")
async def home():

    return {
        "service": "Soma Scripted Chatbot",
        "status": "online",
        "version": "1.0.0",
        "ai_required": False
    }


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "engine": "script-based",
        "external_ai": False
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    answer = find_response(request.message)

    return ChatResponse(answer=answer)


# =====================================================
# END
# =====================================================
