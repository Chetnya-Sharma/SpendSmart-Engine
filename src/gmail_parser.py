import io
import os
import base64
from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from pdfminer.high_level import extract_text

from config import settings

# Initialize MongoDB client
async def init_db():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    return client.maxxmaicard

# Step 1: OAuth URL

def get_auth_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uris": [settings.google_redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        redirect_uri=settings.google_redirect_uri
    )
    auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return auth_url

# Step 2: Exchange code for tokens

def fetch_tokens(code: str):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uris": [settings.google_redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        redirect_uri=settings.google_redirect_uri
    )
    flow.fetch_token(code=code)
    return flow.credentials

# Step 3: Fetch and parse latest e-statement

def parse_estatement(creds) -> str:
    service = build('gmail', 'v1', credentials=creds)
    # Search for PDF or text statements
    results = service.users().messages().list(userId='me', q='subject:(statement OR e-statement) ').execute()
    msgs = results.get('messages', [])
    if not msgs:
        raise ValueError("No statement email found.")
    msg_id = msgs[0]['id']
    data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    # Look for PDF attachment
    for part in data.get('payload', {}).get('parts', []):
        filename = part.get('filename', '')
        body = part.get('body', {})
        if filename.lower().endswith('.pdf') and 'data' in body:
            pdf_bytes = base64.urlsafe_b64decode(body['data'])
            return extract_text(io.BytesIO(pdf_bytes))
        # fallback to plain text body
        if part.get('mimeType') == 'text/plain' and 'data' in body:
            return base64.urlsafe_b64decode(body['data']).decode('utf-8')
    raise ValueError("No parsable content in recent email.")

# Helper: parse raw statement text into transactions

def parse_text_to_transactions(text: str) -> List[Dict]:
    transactions = []
    for line in text.splitlines():
        parts = line.split()
        # Expect: DATE DESCRIPTION AMOUNT
        if len(parts) >= 3:
            date = parts[0]
            amount = parts[-1].replace(',', '')
            try:
                amt = float(amount)
            except ValueError:
                continue
            desc = ' '.join(parts[1:-1])
            transactions.append({ 'date': date, 'amount': amt, 'description': desc })
    return transactions

# Step 4: Store in MongoDB

async def store_statement(user_info: Dict, prefs: Dict, statement_text: str):
    db = await init_db()
    parsed = parse_text_to_transactions(statement_text)
    await db.users.insert_one(user_info)
    await db.preferences.insert_one(prefs)
    await db.statements.insert_one({'transactions': parsed})
