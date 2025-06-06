from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plan_password, hashed_password):
    return pwd_context.verify(plan_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)