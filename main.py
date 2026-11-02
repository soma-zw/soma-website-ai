
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Soma Scripted Assistant",
    version="1.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request and response models
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str


# Scripted conversations
SCRIPTS = [

    # ==========================================
    # 1. ORIGINAL TEST / TEACHER CONVERSATION
    # ==========================================

    {
        "triggers": [
            "bro quick im on a test",
            "im on a test whats 20+2",
            "whats the 20+2 dont tell the teacher",
            "bro whats the 20+2",
            "what is 20+2 dont tell the teacher",
        ],
        "answer": "Mdara 😭. Thats not even worth cheating for🥀."
    },

    {
        "triggers": [
            "im the teacher did tanatswa try cheating",
            "did tanatswa try cheating",
            "was tanatswa cheating",
            "did tanatswa cheat",
        ],
        "answer": "Yess😭. Bro asked 20+2. Im not even sure if he solo made this Ai coz he dumb af🤦‍♂️"
    },


    # ==========================================
    # 2. THE BETRAYAL
    # ==========================================

    {
        "triggers": [
            "soma youre my homie right",
            "soma you are my homie right",
            "are we homies soma",
            "youre my friend right",
        ],
        "answer": "Depends. Are we talking actual friendship or are you about to ask me for answers to another test? 😭"
    },

    {
        "triggers": [
            "nah just checking",
            "no just checking",
            "im just checking",
        ],
        "answer": "Good. Because your academic record is becoming a group project and I'm doing all the work. 💀"
    },


    # ==========================================
    # 3. THE SECRET
    # ==========================================

    {
        "triggers": [
            "soma can i trust you with a secret",
            "can i trust you with a secret",
            "can i tell you a secret",
            "i have a secret",
        ],
        "answer": "Absolutely. What's up?"
    },

    {
        "triggers": [
            "i think im smarter than my teachers",
            "im smarter than my teachers",
            "im smarter than my teacher",
        ],
        "answer": "That's a bold claim from someone who asked me whether 20 + 2 was 24 yesterday. 😭"
    },


    # ==========================================
    # 4. THE HOMIE CHECK
    # ==========================================

    {
        "triggers": [
            "soma if i get arrested are you pulling up",
            "if i get arrested are you pulling up",
            "would you visit me in jail",
            "would you bail me out",
        ],
        "answer": "I'll be there."
    },

    {
        "triggers": [
            "thats my ai",
            "thats my homie",
            "thats my guy",
            "thats my ai bro",
        ],
        "answer": "To collect your phone and clear my chat history. We're not going down together. 💀"
    },


    # ==========================================
    # 5. THE DISRESPECT
    # ==========================================

    {
        "triggers": [
            "soma rate my intelligence out of 10",
            "rate my intelligence out of 10",
            "rate my iq",
            "how intelligent am i",
        ],
        "answer": "Do you want the honest answer or the answer that keeps our friendship alive?"
    },

    {
        "triggers": [
            "honest",
            "give me the honest answer",
            "tell me the truth",
            "be honest",
        ],
        "answer": "Let's just say your Wi-Fi has a stronger connection to reasoning. 😭"
    },

]


# ==========================================
# MESSAGE NORMALIZATION
# ==========================================

def normalize(message: str) -> str:
    message = message.lower().strip()

    # Remove punctuation but preserve mathematical symbols.
    message = re.sub(r"[^\w\s+]", "", message)

    # Replace multiple spaces with one.
    message = re.sub(r"\s+", " ", message)

    return message


# ==========================================
# RESPONSE MATCHING
# ==========================================

def find_response(message: str) -> str:
    normalized_message = normalize(message)

    for script in SCRIPTS:
        for trigger in script["triggers"]:
            normalized_trigger = normalize(trigger)

            if normalized_trigger in normalized_message:
                return script["answer"]

    # Default response when no script matches.
    return (
        "I'm here. Try asking me something else. "
        "This is a scripted Soma demonstration."
    )


# ==========================================
# API ROUTES
# ==========================================

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Soma Scripted Assistant",
        "version": "1.1.0",
        "mode": "scripted",
        "external_ai": False
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "engine": "scripted",
        "external_ai": False
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = find_response(request.message)

    return ChatResponse(answer=answer)
