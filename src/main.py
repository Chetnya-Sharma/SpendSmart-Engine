from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import yaml
import jwt
from typing import Dict
from models import SpendProfile, Recommendation
from config import settings
from gmail_parser import get_auth_url, fetch_tokens, parse_estatement, store_statement

app = FastAPI()

# Load cards
try:
    with open('cards.yaml') as f:
        cards = yaml.safe_load(f)['cards']
except Exception as e:
    raise RuntimeError("Failed to load cards.yaml: " + str(e))

# Gmail OAuth URL
@app.get('/auth/url')
def auth_url():
    return { 'url': get_auth_url() }

# OAuth callback
@app.get('/auth/callback')
def auth_callback(code: str = None, error: str = None):
    if error:
        raise HTTPException(status_code=400, detail="OAuth denied: " + error)
    if not code:
        raise HTTPException(status_code=400, detail="No code in callback.")
    creds = fetch_tokens(code)
    try:
        text = parse_estatement(creds)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    user_info = {'email': 'user@example.com'}    # replace with real from creds
    prefs: Dict = {}
    import asyncio
    asyncio.create_task(store_statement(user_info, prefs, text))
    return RedirectResponse(url='/')

# Recommendation endpoint
@app.post('/recommend', response_model=Recommendation)
def recommend(spend: SpendProfile):
    best = None
    best_score = float('-inf')
    total_spend = spend.groceries + spend.fuel + spend.dining + spend.travel
    for c in cards:
        score = (c['cashback']/100)*total_spend + (c['welcome_bonus']/1000)
        if score > best_score:
            best_score = score
            best = c['name']
    if not best:
        raise HTTPException(status_code=500, detail="No cards available.")
    return { 'card_name': best }
