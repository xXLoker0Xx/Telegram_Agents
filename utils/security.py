# utils/security.py
import os

def validate_user(user_id: int) -> bool:
    allowed_ids_str = os.getenv("ALLOWED_USER_IDS", "")
    
    if not allowed_ids_str:
        raise ValueError("❌ Variable ALLOWED_USER_IDS no definida en .env")
    
    allowed_ids = [int(id.strip()) for id in allowed_ids_str.split(",")]
    return user_id in allowed_ids