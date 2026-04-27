from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

# ── Variáveis de ambiente ───────────────────────────────────────────────────
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY não encontrada. Verifique seu arquivo .env")

app = FastAPI()

# ── CORS ────────────────────────────────────────────────────────────────────
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Histórico ───────────────────────────────────────────────────────────────
FILE = "history.json"

def load_history() -> list:
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
    except json.JSONDecodeError:
        return []
    except OSError as e:
        return []

def save_history(history: list) -> None:
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except OSError as e:
        return []

# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/weather")
def get_weather(city: str = Query(..., min_length=1, max_length=100)):
    """Busca a previsão do tempo para uma cidade."""

    # Sanitiza entrada básica
    city = city.strip()

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
    )

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="A API de clima demorou demais para responder. Tente novamente.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Não foi possível conectar à API de clima. Verifique sua conexão.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Erro ao se comunicar com a API de clima.")

    # Trata erros específicos da API externa sem expor detalhes internos
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Cidade '{city}' não encontrada.")
    if response.status_code == 401:
        raise HTTPException(status_code=500, detail="Erro de configuração interna. Contate o suporte.")
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Limite de requisições atingido. Tente novamente em instantes.")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="A API de clima retornou uma resposta inesperada.")

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Resposta inválida da API de clima.")

    return_weather = {
        "city": data.get("name"),
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "coord": data["coord"],
    }

    # Não duplica as cidades no histórico ( chave nome da cidade )
    history = load_history()
    history = [return_weather] + [h for h in history if h.get("city") != return_weather["city"]]
    history = history[:20]
    save_history(history)

    return return_weather


@app.get("/history")
def get_history():
    """Busca o histórico de buscas do arquivo json."""
    return load_history()