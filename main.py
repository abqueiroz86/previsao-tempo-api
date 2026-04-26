from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import json
import requests
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI()

# Salva histórico de pesquisas no arquilo history.json
FILE = "history.json"

def load_history():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(FILE, "w") as f:
        json.dump(history, f)

origins = [
    "http://localhost:3000",  # seu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou ["*"] para liberar tudo (dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def get_weather(city: str = Query(...)):
    try:
        history = load_history()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
        
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Erro ao buscar clima"
            )

        data = response.json()

        return_weather = {
            "city": data.get("name"),
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "coord": data['coord']
        }

        history = [return_weather] + [h for h in history if h != return_weather]
        history = history[:10]

        save_history(history)

        return return_weather

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Erro de conexão com API externa"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/history")
def get_history():
    try:
        history = load_history()

        return history

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )