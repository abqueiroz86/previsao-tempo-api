# ⛅ Previsão do Tempo

Aplicação fullstack para consulta de clima em tempo real, com histórico de buscas e visualização em mapa.

## 🚀 Preview

### PC
![Demo](./docs/pc.gif)

### Celular
![Demo](./docs/celular.gif)

## 🛠️ Tecnologias

### Frontend
- Next.js (React)
- TypeScript
- TailwindCSS
- React Leaflet

### Backend
- FastAPI
- Python

---

## 📦 Instalação

### 1. Clonar os repositórios

## API
```bash
git clone https://github.com/abqueiroz86/previsao-tempo-api
cd seu-repo
``` 

## Frontend
```bash
git clone https://github.com/abqueiroz86/previsao-tempo-app
cd seu-repo
``` 

### 2. Instalar dependências

## DEPENDENCIAS API
```bash
pip install fastapi uvicorn requests
pip install python-dotenv
``` 

## DEPENDENCIAS APP
```bash
npm install leaflet react-leaflet
npm install react-hot-toast
``` 

## Executando o Projeto

### 1. Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
``` 

Disponível em [http://localhost:8000](http://localhost:8000)


### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Disponível em [http://localhost:3000](http://localhost:3000)
