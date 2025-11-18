from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Jarvis API running!"}

@app.get("/weather")
def weather(city: str = "Delhi"):
    return {
        "city": city,
        "weather": "Sunny",
        "temp": "30°C",
        "note": "This is a sample. We will add real weather API soon."
    }
