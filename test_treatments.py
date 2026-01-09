#!/usr/bin/env python3
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(supabase_url, supabase_key)

try:
    response = supabase.table('treatments').select('*').limit(5).execute()
    print(f"✅ Tratamientos encontrados: {len(response.data)}")
    if response.data:
        print("\nPrimer tratamiento:")
        print(response.data[0])
except Exception as e:
    print(f"❌ Error: {e}")
