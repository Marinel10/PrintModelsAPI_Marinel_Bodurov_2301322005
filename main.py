from fastapi import FastAPI

app = FastAPI(title="3D Print Models API")


@app.get("/")
def root():
    return { "status": "ok" }
