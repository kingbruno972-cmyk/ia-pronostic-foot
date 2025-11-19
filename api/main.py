from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "API en ligne ! 🚀"}

# IMPORTANT : NE RIEN METTRE D'AUTRE