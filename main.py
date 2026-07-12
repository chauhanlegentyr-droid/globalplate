import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Point cleanly to the root folder configuration
templates = Jinja2Templates(directory=".")

@app.get("/")
async def read_root(request: Request):
    # Pass the server-side key variable into the index template safely
    api_key = os.getenv("GEMINI_API_KEY", "")
    return templates.TemplateResponse("index.html", {"request": request, "gemini_key": api_key})
