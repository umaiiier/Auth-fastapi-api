# FastAPI + Supabase Auth API

A secure RESTful API built with **FastAPI** and **Supabase Auth** as the Identity Provider (IdP).

## ?? How to Run

1. Clone repository & install dependencies:
   `ash
   pip install -r requirements.txt
   ``n2. Configure .env file from template:
   `ash
   cp .env.example .env
   ``n3. Run the application:
   `ash
   uvicorn main:app --reload --port 8000
   ``n4. Open Swagger Docs at http://localhost:8000/docs.

## ?? API Reference

| Endpoint | Method | Purpose | Auth Required |
| :--- | :--- | :--- | :--- |
| /auth/signup | POST | Register new user | No |
| /auth/login | POST | Authenticate & get JWT | No |
| /auth/logout | POST | Invalidate session | Yes (Bearer) |
| /public/info | GET | View public data | No |
| /protected/profile | GET | View user profile | Yes (Bearer) |
| /protected/dashboard| GET | View dashboard info| Yes (Bearer) |
