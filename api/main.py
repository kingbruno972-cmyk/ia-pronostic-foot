from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "API pronostic foot en ligne 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}