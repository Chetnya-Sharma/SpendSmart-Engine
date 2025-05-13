# SpendSmart-Engine

maxx-maicard/

├── cards.yaml

├── .env.example

├── requirements.txt

├── src/

│   ├── main.py

│   ├── models.py

│   ├── gmail_parser.py

│   └── config.py

└── README.md


# Maxx Mai Card - Mini POC

## Prerequisites

- Python 3.8+
- MongoDB running locally (or update `MONGODB_URI`)

## Setup

1. **Clone** (replace with your repo URL):

   ```bash
  git clone [https://github.com/yourusername/SpendWise-Recommender.git](https://github.com/Chetnya-Sharma/SpendSmart-Engine) \
  && cd SpendWise-Recommender
  
  
   

2. **Create `.env`** from `.env.example` and fill in your values.

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:

   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Gmail OAuth Flow

1. Visit `http://localhost:8000/auth/url` to get the consent link.
2. Log in with your test Gmail and allow readonly Gmail scope.
3. Callback will redirect to `/` and store data in MongoDB.

## Testing the API

### 1. /recommend

```bash
curl -X POST http://localhost:8000/recommend \
  -H 'Content-Type: application/json' \
  -d '{"groceries":2000, "fuel":1000, "dining":500, "travel":0}'
```

*Response*: `{ "card_name": "Platinum Plus" }`

### 2. Check MongoDB

```bash
mongo
use maxxmaicard
db.users.find().pretty()
db.preferences.find().pretty()
db.statements.find().pretty()
```

## Loom Video

- Show `/auth/url`, Gmail consent
- Display MongoDB collections with new docs
- Call `/recommend` and show JSON response
- Scroll README showing setup & curl examples

```

---

**That’s it!** Run a final end‑to‑end test, record your ≤ 3 min Loom, and submit your GitHub link.

```
