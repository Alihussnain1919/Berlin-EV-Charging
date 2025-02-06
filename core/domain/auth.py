import bcrypt

def hash_password(password):
    """Hash a plain-text password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verify if a password matches the hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
