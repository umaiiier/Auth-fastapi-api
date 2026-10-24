import os
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError('Missing Supabase environment variables.')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title='Auth Login & Protect API')

@app.get('/')
def root():
    return {'message': 'Server running and connected to Supabase'}
