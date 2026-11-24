# GlobalPlate AI

GlobalPlate AI is an AI-powered international culinary assistant built with FastAPI and Google Gemini. It helps users discover dishes, generate complete recipes, ask cooking follow-up questions, and explore ingredients and nutrition in an accessible, responsive web interface.

## Features

- Live, streaming recipe responses powered by Google Gemini
- Multi-turn conversational memory for dish and cooking questions
- Complete recipe formatting with origin, timing, ingredients, steps, nutrition, substitutions, and chef tips
- Dynamic dish images through Pexels with built-in Unsplash fallbacks
- Nutrition estimate cards and interactive ingredient checklists
- Browser storage for saved dish conversations
- Voice input and text-to-speech support where available
- Copy, download, and print/PDF tools
- Responsive light and dark themes
- Docker-ready deployment
- Health, version, project information, media, and AI API endpoints

## Technology Stack

- **Backend:** FastAPI, Uvicorn
- **AI:** Google Gen AI SDK / Gemini
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Images:** Pexels API with built-in fallback images
- **Container:** Docker
- **Deployment targets:** AWS / Render

## API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.1-flash-lite
PEXELS_API_KEY=your_pexels_api_key
```

- `GEMINI_API_KEY` is required.
- `GEMINI_MODEL` is optional and defaults to `gemini-3.1-flash-lite`.
- `PEXELS_API_KEY` is optional. If omitted or unavailable, the app uses built-in fallback dish images.

> Never commit API keys or `.env` files to the repository.

## Local Setup

Requires Python 3.12 or a compatible Python version.

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Add environment variables

Create `.env` and add `GEMINI_API_KEY`. Optionally add `GEMINI_MODEL` and `PEXELS_API_KEY` as shown above.

### 4. Run the application

```bash
python -m uvicorn main:app --reload
```

Open <http://127.0.0.1:8000> in your browser.

## Docker

Build and run the image:

```bash
docker build -t globalplate-ai .
docker run --env-file .env -p 8000:8000 globalplate-ai
```

The container serves the app on port `8000`. You can also set the container `PORT` environment variable.

## Application Routes

| Route | Method | Description |
| --- | --- | --- |
| `/` | GET | Web application |
| `/health` | GET | Deployment health check |
| `/version` | GET | Application version |
| `/api/info` | GET | Public application information |
| `/api/image?query=dish-name` | GET | Dish image lookup |
| `/api/cook` | POST | Streaming Gemini cooking assistant response |
| `/docs` | GET | Interactive FastAPI documentation |

## Project Structure

```text
.
├── main.py          # FastAPI application and API routes
├── requirements.txt # Python dependencies
├── Dockerfile       # Container configuration
├── .gitignore       # Local and generated file exclusions
└── templates/
    └── index.html   # GlobalPlate AI web interface
```

## Security

- Keep `GEMINI_API_KEY` and `PEXELS_API_KEY` private.
- Store secrets through environment variables or your deployment provider's secret manager.
- Do not place credentials in source code, client-side JavaScript, or the repository.

## Developer

Developed by Nirbhaysingh A. Chauhan.
