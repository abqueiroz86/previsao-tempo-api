from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import requests

app = FastAPI()

API_KEY = ""

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
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
        
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Erro ao buscar clima"
            )

        data = response.json()
        

        return {
            "city": data.get("name"),
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            'coord': data['coord']
        }

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