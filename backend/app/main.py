from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import logging
import numpy as np

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

app = FastAPI(
    title="My FastAPI App",
    description="A FastAPI application with user authentication",
    version="1.0.0"
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

class WorldState(BaseModel):
    matrix: List[List[int]]
    current_message: str = ""

class ChatMessage(BaseModel):
    message: str

# Simulated database - Replace with real database in production
fake_users_db = {}

# Initialize a dummy world state
WORLD_STATE = WorldState(
    matrix=[[0, 1, 0], 
            [1, 0, 1], 
            [0, 1, 0]],
    current_message=""
)

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

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int, 
    q: Optional[str] = None, 
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} accessed item {item_id}")
    return {"item_id": item_id, "query": q, "owner": current_user.username}

@app.post("/items/")
async def create_item(
    name: str, 
    price: float, 
    is_offer: bool = False,
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} created item: {name}")
    return {
        "item_name": name, 
        "price": price, 
        "is_offer": is_offer,
        "owner": current_user.username
    }

@app.get("/world", response_model=WorldState)
async def get_world_state(current_user: User = Depends(get_current_user)):
    """
    Retrieve the current state of the world matrix and last message
    """
    logger.info(f"User {current_user.username} requested world state")
    return WORLD_STATE

@app.post("/chat")
async def send_chat(
    chat: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """
    Send a chat message that affects the world state
    """
    global WORLD_STATE
    
    # Log the chat message
    logger.info(f"User {current_user.username} sent message: {chat.message}")
    
    # Update the world state based on the chat message (dummy logic)
    # This is where you'd put your actual world-changing logic
    WORLD_STATE.current_message = chat.message
    
    # Randomly modify the matrix (dummy example)
    new_matrix = np.array(WORLD_STATE.matrix)
    i, j = np.random.randint(0, len(new_matrix), 2)
    new_matrix[i][j] = 1 if new_matrix[i][j] == 0 else 0
    WORLD_STATE.matrix = new_matrix.tolist()
    
    return {
        "message": "World state updated",
        "new_state": WORLD_STATE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
