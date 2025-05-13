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


 Maxx Mai Card - Mini POC

## Prerequisites

- Python 3.8+
- MongoDB running locally (or update `MONGODB_URI`)

## Setup

1. Clone:
   ```bash
git clone <repo_url> && cd maxx-maicard

2. Create .env from .env.example and fill in your values.

3. Install:
 pip install -r requirements.txt

4. Run the server: 
 ```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
