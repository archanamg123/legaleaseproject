# LegalEase

LegalEase is an AI-powered legal document drafting application built using:

- Python
- Streamlit
- FastAPI
- Google Gemini
- python-docx
- fpdf2

## Features

- AI-assisted legal document generation
- Employment contracts
- NDAs
- Lease agreements
- Freelance contracts
- Service agreements
- Partnership agreements
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Demo mode
- FastAPI REST API

## Project Structure

LegalEase/
│
├── app.py
├── main.py
├── requirements.txt
├── .env
│
├── api/
│   ├── routes.py
│   └── schemas.py
│
├── ai_core/
│   └── gemini_generator.py
│
├── services/
│   └── exporters.py
│
└── tests/

## Installation

Create a virtual environment:

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Configuration

Create .env:

GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.8-flash
DEMO_MODE=true
BACKEND_URL=http://127.0.0.1:8000

## Demo Mode

Set:

DEMO_MODE=true

This allows the complete application to run without Gemini.

## Gemini Mode

Set:

DEMO_MODE=false

Then add a valid Gemini API key:

GEMINI_API_KEY=your_api_key

## Start Backend

uvicorn main:app --reload --port 8000

## Start Frontend

streamlit run app.py

## API Documentation

After starting FastAPI:

http://127.0.0.1:8000/docs

## Run Tests

pytest -q