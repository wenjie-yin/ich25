import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent))


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import logging
import numpy as np
from model.main import MainLoop
from app import WorldState
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = "4816f065f929392e7d07bc03a581bf3d6332f8e943072b0f3aecd717a7318280"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize MainLoop with context manager
    main = MainLoop().__enter__()
    # Store the main instance in app.state
    app.state.main = main
    yield  # Just yield without any value
    # Cleanup
    main.__exit__(None, None, None)

app = FastAPI(
    title="My FastAPI App",
    description="A FastAPI application with user authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Get the MainLoop instance from the app state
def get_main():
    return app.state.main

# Add this after creating the FastAPI app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Less secure, but easier for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ChatMessage(BaseModel):
    message: str

# Simulated database - Replace with real database in production
fake_users_db = {}

# Add a test user to the fake database
fake_users_db["testuser"] = {
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "hashed_password": pwd_context.hash("password123")
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/register")
async def register(username: str, password: str, email: Optional[str] = None):
    if username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(password)
    user_dict = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password
    }
    fake_users_db[username] = user_dict
    logger.info(f"New user registered: {username}")
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/world", response_model=WorldState)
async def get_world_state(current_user: User = Depends(get_current_user)):
    """
    Retrieve the current state of the world matrix and last message
    """
    main = get_main()
    WORLD_STATE = main.get_world_state()
    return WORLD_STATE

@app.post("/chat")
async def send_chat(
    chat: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """ 
    Send a chat message that affects the world state
    """
    main = get_main()
    WORLD_STATE = main.get_world_state()
    # Log the chat message
    logger.info(f"User {current_user.username} sent message: {chat.message}")
    
    # Update the world state based on the chat message
    WORLD_STATE.current_message = chat.message
    await main.send_user_message(chat.message)
    
    # Example logic: Update belief vector based on message
    new_belief = np.array(WORLD_STATE.belief_vector)
    # Randomly modify one belief value (dummy example)
    i = np.random.randint(0, len(new_belief))
    new_belief[i] = max(0, min(1, new_belief[i] + np.random.uniform(-0.1, 0.1)))
    WORLD_STATE.belief_vector = new_belief.tolist()
    
    return {
        "message": "World state updated",
        "new_state": WORLD_STATE
    }

@app.get("/belief")
async def get_belief(current_user: User = Depends(get_current_user)):
    main = get_main()
    return main.network.belief

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
