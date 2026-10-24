import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Auth Login & Protect API")
security = HTTPBearer()

class AuthCredentials(BaseModel):
    email: EmailStr
    password: str

# --- REUSABLE AUTH DEPENDENCY (MIDDLEWARE) ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})
        return {"user": user_response.user, "token": token}
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid or expired token"})

# --- PUBLIC ROUTES ---
@app.get("/")
def root():
    return {"message": "Server running and connected to Supabase"}

@app.get("/public/info", status_code=status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# --- AUTH ROUTES ---
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: AuthCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        res = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        if not res.user:
            raise HTTPException(status_code=400, detail="User registration failed")
        return {"user": res.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login(credentials: AuthCredentials):
    if not credentials.email or not credentials.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    try:
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        if not res.session:
            raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})
            
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=401, detail={"error": "Invalid login credentials"})

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(auth_data: dict = Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- PROTECTED ROUTES ---
@app.get("/protected/profile", status_code=status.HTTP_200_OK)
def get_profile(auth_data: dict = Depends(get_current_user)):
    user = auth_data["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@app.get("/protected/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard(auth_data: dict = Depends(get_current_user)):
    user = auth_data["user"]
    return {"message": f"Welcome to your dashboard, {user.email}!"}