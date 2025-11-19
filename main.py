from fastapi import FastAPI
import datetime
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("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")
WEATHER_API_KEY = os.getenv("c479459c42c9453cb0874154251811")

openai.api_key = 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

app = FastAPI()

# Allow all origins (for local/dev testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Root ---------
@app.get("/")
def home():
    return {"status": "Jarvis API running!"}

# --------- Weather ---------
@app.get("/weather")
def weather(city: str = "Durg"):
    url = f"http://api.weatherapi.com/v1/current.json?key={c479459c42c9453cb0874154251811}&q={city}"
    try:
        data = requests.get(url).json()
        temp = data["current"]["temp_c"]
        cond = data["current"]["condition"]["text"]
        return {"city": city, "temperature": f"{temp}°C", "condition": cond}
    except:
        return {"error": "Could not fetch weather. Check city or API key."}

# --------- Time ---------
@app.get("/time")
def get_time():
    return {"time": datetime.datetime.now().strftime("%I:%M %p")}

# --------- Date ---------
@app.get("/date")
def get_date():
    return {"date": datetime.datetime.now().strftime("%d %B %Y")}

# --------- ChatGPT Responses ---------
@app.get("/ask")
def ask(question: str):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=150,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        return {"question": question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
