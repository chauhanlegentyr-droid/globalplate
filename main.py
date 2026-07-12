import os
import httpx
import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory=".")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/cook")
async def culinary_stream(request: Request):
    body = await request.json()
    user_dish = body.get("message", "")
    
    # Overhauled omni-prompt telling the agent to return everything inside a unified master report
    system_prompt = (
        f"You are the GlobalPlate Omniscient Culinary AI Agent. The user wants to learn everything about the dish or ingredients: '{user_dish}'. "
        f"Provide an incredibly detailed, comprehensive master layout structured exactly like this:\n\n"
        f"🌍 1. CULTURAL HISTORY & ORIGIN: Detail the deep history, cultural background, and interesting origin facts of this dish.\n\n"
        f"⏱️ 2. PREPARATION METRICS (COOKING TIME): State the exact approximate Prep Time, Cooking Time, and Total Time required.\n\n"
        f"📝 3. TRADITIONAL INGREDIENTS LIST: Provide a clean checklist of all ingredients needed using dual measurements (both metric and imperial units).\n\n"
        f"🍳 4. STEP-BY-STEP PREPARATION GUIDE: Provide clear, chronological, and highly descriptive cooking instructions to make this dish perfectly.\n\n"
        f"💡 5. SECRET CHEF TRICK: Share one elite culinary insider secret that restaurants use to make this dish taste authentic."
    )

    payload = {
        "contents": [{"parts": [{"text": system_prompt}]}]
    }
    
    url = f"https://googleapis.com{GEMINI_API_KEY}"

    async def event_generator():
        async with httpx.AsyncClient(http2=True) as client:
            try:
                async with client.stream("POST", url, json=payload, timeout=40.0) as response:
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        clean_line = line.strip()
                        
                        if clean_line.startswith("[") or clean_line.startswith(","):
                            clean_line = clean_line[1:]
                        if clean_line.endswith("]") or clean_line.endswith(","):
                            clean_line = clean_line[:-1]
                        
                        try:
                            chunk_data = json.loads(clean_line)
                            parts = chunk_data["candidates"]["content"]["parts"]
                            text_chunk = "".join([part.get("text", "") for part in parts])
                            if text_chunk:
                                yield f"data: {json.dumps({'text': text_chunk})}\n\n"
                        except Exception:
                            pass
            except Exception as e:
                yield f"data: {json.dumps({'text': f'❌ Cloud Pipeline Error: {str(e)}'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
