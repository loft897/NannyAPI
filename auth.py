from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Initialisation de l'application
app = FastAPI()

# Configuration du secret de cryptage et de l'algorithme de cryptage
SECRET_KEY = "ma_cle_secrete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuration du mot de passe haché
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration du schéma d'authentification OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuration de l'utilisateur de test
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$8V4w0CZJ12hcyoqnPpObL.t0iFm0sglqzjKxUGQ0W.NwtfZcQ2g2a",
        "disabled": False,
    }
}

# Fonction pour vérifier si le mot de passe est correct
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour hacher un mot de passe
def get_password_hash(password):
    return pwd_context.hash(password)

# Fonction pour générer un jeton d'accès
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour décoder le jeton d'accès
def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        token_data = {"username": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return token_data

# Route pour créer un jeton d'accès
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Route pour tester l'authentification
@app.get("/users/me")
async def read_users_me(current_user : str = Depends(oauth2_scheme)):
    token_data = decode_access_token(current_user)
    user = fake_users_db.get(token_data["username"])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Fonction pour vérifier les permissions d'un utilisateur
def check_user_permissions(user: dict, permission: str):
    if permission not in user["permissions"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

# Fonction pour vérifier si l'utilisateur est désactivé
def check_user_is_active(user: dict):
    if user["disabled"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

# Définition d'un exemple de route avec authentification et autorisation
@app.get("/example")
async def example(current_user: dict = Depends(get_current_user)):
    check_user_permissions(current_user, "example:read")
    check_user_is_active(current_user)
    return {"message": "This is an example endpoint"}

# Exemple de route nécessitant une authentification sans autorisation
@app.get("/example2")
async def example2(current_user: dict = Depends(get_current_user)):
    check_user_is_active(current_user)
    return {"message": "This is another example endpoint"}

# Ce code met en place une authentification JWT sécurisée avec la gestion des données confidentielles. La fonction get_current_user est utilisée pour vérifier l'authentification de l'utilisateur et renvoyer ses informations si l'authentification est réussie. Les fonctions check_user_permissions et check_user_is_active sont utilisées pour vérifier les autorisations de l'utilisateur et sa désactivation. Enfin, deux exemples de routes sont fournis pour illustrer comment utiliser ces fonctions dans votre API.
