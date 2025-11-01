Member: Aline Innocente

# MongoDB Implementation (Student Performance)



This module mirrors the SQL design in a NoSQL format using MongoDB.  
It ingests the dataset, creates indexes, runs CRUD and analytics, and (optionally) enforces a JSON schema validator.

## Prerequisites
- Python 3.9+  
- MongoDB Atlas (or local MongoDB) connection string
- VS Code (recommended)

## Setup
```bash
cd mongodb
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env    # fill in values
