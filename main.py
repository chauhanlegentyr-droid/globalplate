import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONEncoder
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Point to root folder for clean deployment tracking
templates = Jinja2Templates(directory=".")

@app.get("/")
async def read_root(request: Request):
    # Pass the server-side API Key to the template securely
    api_key = os.getenv("GEMINI_API_KEY", "")
    return templates.TemplateResponse("index.html", {"request": request, "gemini_key": api_key})

