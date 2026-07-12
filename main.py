import os
import httpx
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Point directly to root repository folder context for unified browser file reading
templates = Jinja2Templates(directory=".")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/cook")
async def culinary_stream(request: Request):
    body = await request.json()
    user_dish = body.get("message", "")
    feature_type = body.get("feature", "recipe") # Read multi-feature route variables dynamically
    
    # Establish dynamic agent system prompt profiles based on user interface clicks
    if feature_type == "history":
        system_prompt = f"You are the GlobalPlate Culture Agent. Detail the exact historical origin, ancient traditions, and deep cultural evolution of: '{user_dish}'. Avoid printing recipes here."
    elif feature_type == "nutrition":
        system_prompt = f"You are the GlobalPlate Nutrition Agent. Detail the estimated macro breakdown (Protein, Carbs, Fats) and holistic health benefits of standard: '{user_dish}'."
    else:
        system_prompt = (
            f"You are the GlobalPlate Head Master Chef Agent. For '{user_dish}', provide a clear response containing:\n"
            f"1. 📝 TRADITIONAL RECIPE: Organized ingredients using dual metrics (imperial & metric).\n"
            f"2. 🍳 COOKING INSTRUCTIONS: Chronological preparation steps.\n"
            f"3. 💡 INSIDER CHEF TRICK: A deep secret to make it authentic."
        )

    # Reconfigured robust payload structure matching standard Google API gateway models
    payload = {
        "contents": [{"parts": [{"text": system_prompt}]}]
    }
    
    url = f"https://googleapis.com{GEMINI_API_KEY}"

    async def event_generator():
        # Using structured text/event-stream chunks to bypass proxy buffer blocking
        async with httpx.AsyncClient(http2=True) as client:
            try:
                async with client.stream("POST", url, json=payload, timeout=30.0) as response:
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        clean_line = line.strip()
                        
                        # Process array boundary strings
                        if clean_line.startswith("[") or clean_line.startswith(","):
                            clean_line = clean_line[1:]
                        if clean_line.endswith("]") or clean_line.endswith(","):
                            clean_line = clean_line[:-1]
                        
                        try:
                            chunk_data = json.loads(clean_line)
                            parts = chunk_data["candidates"]["content"]["parts"]
                            text_chunk = "".join([part.get("text", "") for part in parts])
                            if text_chunk:
                                # Standard unified format wrapping strings inside clean JSON structures
                                yield f"data: {json.dumps({'text': text_chunk})}\n\n"
                        except Exception:
                            pass
            except Exception as e:
                yield f"data: {json.dumps({'text': f'❌ Cloud Pipeline Exception: {str(e)}'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
