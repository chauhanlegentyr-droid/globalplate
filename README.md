GlobalPlate AI

GlobalPlate AI is an AI-powered international culinary assistant designed to help users discover recipes, explore dishes, and interact with an AI cooking assistant.

Features

Live Gemini-powered recipe generation

Streaming AI responses

Multi-turn conversation memory

Saved dish conversations in browser storage

Dynamic dish images using Pexels

Nutrition summary card

Ingredient checklist

Voice input where supported

Copy, download, and print/PDF tools

Dark mode and responsive design

Docker-ready FastAPI deployment

Health and API information endpoints

Local Setup

Copy .env.example to .env.

Add your Gemini and Pexels API keys.

Install dependencies:

py -m pip install -r requirements.txt


Run the application:

py -m uvicorn main:app --reload


Open http://127.0.0.1:8000 in your browser.

Useful Endpoints

/ — Web application

/health — Deployment health check

/api/info — Public project information

/docs — FastAPI documentation

Security

Never commit .env files or API keys to GitHub.

Developer

Developed by Nirbhaysingh A. Chauhan.