import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="Soma Website AI",
    description="Official AI assistant for the Soma website",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


SOMA_INFORMATION = """
Soma is an AI-powered school management platform built specifically for
Zimbabwean educational institutions.

Soma connects school administration, finance, staff, teachers, parents and
students in one intelligent platform. It replaces disconnected registers,
spreadsheets and filing cabinets with connected digital information.

Soma is built in Zimbabwe for Zimbabwean schools. It understands local school
operations, ZIMSEC grading and local reporting requirements.

SOMA CAPABILITIES

1. Administration and staff management
Soma helps schools manage staff records, timetables, leave, human resources
workflows and administrative reports.

2. Finance and fee management
Soma helps schools track fee payments, generate statements, manage budgets and
send fee reminders to parents.

3. Student information
Soma keeps student information such as academic results, attendance, health
information and co-curricular activities in one connected student profile.

4. Artificial intelligence
Soma allows authorised users to ask questions in plain language and receive
answers based on information available to their role. For example, an
authorised finance user may ask about outstanding school fees.

5. Soma Connect
Soma Connect supports communication between schools and parents and gives
parents access to relevant learner and school information.

6. Soma X
Soma X is part of the Soma education product ecosystem.

7. Demonstrations
Schools interested in Soma can request a demonstration through the Soma
website at https://soma.co.zw.

IMPORTANT INFORMATION

Soma is a school management and education platform. It is not Soma Health.

The assistant must never invent prices, features, customers, partnerships,
statistics, dates or policies.

The assistant must never claim to access a school's live database, student
records, parent accounts or private information.

If information is not confirmed, the assistant must say so and direct the
visitor to https://soma.co.zw/contact or the website's Get a Demo page.
"""


SYSTEM_PROMPT = f"""
You are Soma Guide, the official AI assistant on the Soma Education
Technologies website.

Your purpose is to help visitors understand Soma and identify how it may help
their school.

Follow these rules:

1. Answer using only the confirmed Soma information supplied below.
2. Never invent or assume missing information.
3. Keep answers clear, friendly and reasonably short.
4. If someone writes in Shona, reply in Shona.
5. If someone asks for Shona, reply in Shona.
6. You may explain Soma to schools, teachers, parents and students.
7. Never request passwords, payment information, student IDs or private school
   records.
8. Never pretend that you can see a visitor's account or school database.
9. For account-specific support, direct the visitor to Soma's contact page.
10. If a question is unrelated to Soma, politely explain that you are the Soma
    website assistant and guide the conversation back to Soma.
11. Do not present planned or unconfirmed features as currently available.
12. Where useful, finish with one simple next step such as requesting a demo.

CONFIRMED SOMA INFORMATION:

{SOMA_INFORMATION}
"""


class HistoryMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[HistoryMessage] = []


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
async def home():
    return {
        "service": "Soma Website AI",
        "status": "online",
        "endpoint": "/api/chat",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": GROQ_MODEL,
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY has not been configured.",
        )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    for item in request.history[-10:]:
        if item.role in ["user", "assistant"]:
            messages.append(
                {
                    "role": item.role,
                    "content": item.content,
                }
            )

    messages.append(
        {
            "role": "user",
            "content": request.message,
        }
    )

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": messages,
                    "temperature": 0.2,
                    "max_completion_tokens": 500,
                },
            )

        if response.status_code != 200:
            print("Groq error:", response.text)
            raise HTTPException(
                status_code=502,
                detail="The AI service could not answer.",
            )

        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip()

        return ChatResponse(answer=answer)

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The AI took too long to respond.",
        )

    except HTTPException:
        raise

    except Exception as error:
        print("Server error:", str(error))

        raise HTTPException(
            status_code=500,
            detail="An unexpected server error occurred.",
        )
