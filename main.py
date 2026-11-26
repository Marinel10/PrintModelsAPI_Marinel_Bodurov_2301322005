
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import AppError
from routers import designer,category, material, print_model, print_model_material
app = FastAPI(title="3D Print Models API")

# Регистриране на Router
app.include_router(designer.router)
app.include_router(category.router)
app.include_router(material.router)
app.include_router(print_model.router)
app.include_router(print_model.designer_models_router)
app.include_router(print_model_material.router)


@app.exception_handler(AppError)
def handle_exception(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})
    #return HTMLResponse(status_code = exc.status_code, content=f"<html><b>Error message: {exc.message}</b></html>")



@app.get("/")
def root():
    return { "status": "ok" }
