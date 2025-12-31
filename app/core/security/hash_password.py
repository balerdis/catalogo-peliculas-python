from passlib.context import CryptContext

# Configuración del contexto de hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """
    Genera un hash seguro a partir de una contraseña en texto plano.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash.
    """
    return pwd_context.verify(plain_password, hashed_password)