from fastapi import FastAPI
import datetime
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

openai.api_key = OPENAI_API_KEY

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
def weather(city: str = "Delhi"):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
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
