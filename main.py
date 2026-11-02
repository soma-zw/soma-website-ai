import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# =====================================================
# SOMA AI - TEMPORARY MARKETING DEMONSTRATION
# =====================================================

app = FastAPI(
    title="Soma AI",
    description="Soma AI demonstration API",
    version="TEMP-1.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# REQUEST AND RESPONSE MODELS
# =====================================================

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str


# =====================================================
# SCRIPTED DEMONSTRATION CONVERSATION
# =====================================================

DEMO_CONVERSATIONS = {
    "bro quick im on a test whats the 20+2 dont tell the teacher":
        "Mdara 😭. Thats not even worth cheating for🥀.",

    "im the teacher did tanatswa try cheating":
        "Yess😭. Bro asked 20+2. Im not even sure if he solo made this Ai coz he dumb af🤦‍♂️"
}


# =====================================================
# MESSAGE NORMALISATION
# =====================================================

def normalize_message(message: str) -> str:

    message = message.lower().strip()

    message = message.replace("’", "'")
    message = message.replace("‘", "'")

    message = re.sub(r"[^\w\s+']", "", message)

    message = re.sub(r"\s+", " ", message)

    return message.strip()


# =====================================================
# HOME ENDPOINT
# =====================================================

@app.get("/")
async def home():

    return {
        "service": "Soma AI",
        "version": "TEMP-1.0",
        "status": "online",
        "mode": "marketing demonstration",
        "endpoint": "/api/chat"
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "Soma AI"
    }


# =====================================================
# CHAT ENDPOINT
# =====================================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:

        message = normalize_message(request.message)

        # Match the prepared demonstration messages.
        answer = DEMO_CONVERSATIONS.get(message)

        if answer:

            return ChatResponse(
                answer=answer
            )

        # Default response for other messages.
        return ChatResponse(
            answer="This is a fictional Soma marketing demonstration."
        )

    except Exception as error:

        print("Soma AI error:", str(error))

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


# =====================================================
# END OF SOMA AI
# =====================================================
