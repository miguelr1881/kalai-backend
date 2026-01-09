from supabase import create_client, Client
from app.config import settings

supabase: Client = None


async def init_db():
    """Initialize Supabase client"""
    global supabase
    supabase = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )
    return supabase


def get_db() -> Client:
    """Get Supabase client instance"""
    return supabase
