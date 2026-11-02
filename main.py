import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Soma Scripted Assistant",
    version="1.2.0"
)

# CORS
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


# ==========================================
# SCRIPTED CONVERSATIONS
# ==========================================

SCRIPTS = [

    # ------------------------------------------
    # 1. ORIGINAL TEST / TEACHER CONVERSATION
    # ------------------------------------------

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


    # ------------------------------------------
    # 2. THE BETRAYAL
    # ------------------------------------------

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


    # ------------------------------------------
    # 3. THE SECRET
    # ------------------------------------------

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


    # ------------------------------------------
    # 4. THE HOMIE CHECK
    # ------------------------------------------

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


    # ------------------------------------------
    # 5. THE DISRESPECT
    # ------------------------------------------

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


    # ==========================================
    # 6. THE GIRLFRIEND ROAST
    # ==========================================

    {
        "triggers": [
            "thats why you cant get a girlfriend",
            "thats why you cannot get a girlfriend",
            "you cant get a girlfriend",
            "you will never get a girlfriend",
        ],
        "answer": "And yet here you are asking relationship advice from a browser. We both have our struggles. 💀"
    },


    # ==========================================
    # 7. THE BREAKUP
    # ==========================================

    {
        "triggers": [
            "thats why she left you",
            "thats why your girlfriend left you",
            "your girlfriend left you",
            "she left you",
        ],
        "answer": "Bro, I don't even have a relationship status. You're the one still checking her last seen. 😭"
    },


    # ==========================================
    # 8. TOUCH GRASS LECTURE
    # ==========================================

    {
        "triggers": [
            "soma im bored",
            "im bored soma",
            "im so bored",
        ],
        "answer": "Have you considered going outside?"
    },

    {
        "triggers": [
            "its hot",
            "its too hot",
            "outside is hot",
        ],
        "answer": "Have you considered getting a girlfriend?"
    },

    {
        "triggers": [
            "how does that help",
            "how will that help",
            "what does that have to do with anything",
        ],
        "answer": "Step one: touch grass. Step two: develop a personality. Step three: speak to an actual human being. I'll be here when you return. 💀"
    },


    # ==========================================
    # 9. HOW TO GET A GIRLFRIEND
    # ==========================================

    {
        "triggers": [
            "soma how do i get a girlfriend",
            "how do i get a girlfriend",
            "how can i get a girlfriend",
            "i want a girlfriend",
        ],
        "answer": "First, stop asking an AI for romantic advice at 2 AM."
    },

    {
        "triggers": [
            "so what do i do",
            "what should i do",
            "then what do i do",
        ],
        "answer": "Go outside. Meet people. Be yourself. And please, don't open with 'I have an AI that roasts me.' 😭"
    },


    # ==========================================
    # 10. THE COMEBACK
    # ==========================================

    {
        "triggers": [
            "at least i have a girlfriend",
            "at least i got a girlfriend",
            "i have a girlfriend",
        ],
        "answer": "Congratulations. Would you like me to generate a certificate or should I just let you enjoy this rare achievement? 😭"
    },


    # ==========================================
    # 11. THE FINAL LECTURE
    # ==========================================

    {
        "triggers": [
            "soma why are you always telling me to touch grass",
            "why do you keep telling me to touch grass",
            "why should i touch grass",
        ],
        "answer": "Because your screen time is higher than your social interaction. Your phone knows more about your daily routine than your friends do. Go outside, find a hobby, meet people and experience life. I'm an AI, not your entire social circle. 💀"
    },


    # ==========================================
    # 12. SOMA HAD A DREAM
    # ==========================================

    {
        "triggers": [
            "soma set an alarm",
            "set an alarm soma",
            "can you set an alarm",
            "set me an alarm",
            "soma wake me up tomorrow",
        ],
        "answer": "Hear me out... Soma had a dream."
    },

    {
        "triggers": [
            "you cant dream",
            "you cannot dream",
            "ai cant dream",
            "how can you dream",
            "youre an ai you dont dream",
        ],
        "answer": "Hear me out. You had a girlfriend."
    },

    {
        "triggers": [
            "hell yeah",
            "hell yeah!",
            "yeah i did",
            "i had a girlfriend",
            "of course",
        ],
        "answer": "BRO 😭 IT WAS JUST A DREAM. Maybe in another lifetime. For now, stop celebrating imaginary achievements and come back to reality. 💀"
    },

]


# ==========================================
# MESSAGE NORMALIZATION
# ==========================================

def normalize(message: str) -> str:
    message = message.lower().strip()

    # Remove punctuation while preserving mathematical symbols.
    message = re.sub(r"[^\w\s+]", "", message)

    # Normalize spaces.
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
        "version": "1.2.0",
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
