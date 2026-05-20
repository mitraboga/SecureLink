def require_strong_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
