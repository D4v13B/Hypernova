from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/clientes/{id}/timeline")
async def getHistoryClient():
    return [{"Historial"}]

@app.get("/agentes/{id}/efectividad")
async def getHistoryClient():
    return [{"Efectividad"}]

@app.get("/analytics/promesas-incumplidas")
async def getHistoryClient():
    return [{"Promesas"}]

@app.get("/analytics/mejores-horarios")
async def getHistoryClient():
    return [{"Analiticas"}]