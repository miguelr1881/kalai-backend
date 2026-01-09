#!/usr/bin/env python3
"""
Script para crear la tabla de tratamientos y migrar los servicios actuales
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(supabase_url, supabase_key)

def migrate_services_to_treatments():
    print("🔄 Migrando servicios de products a treatments...\n")
    
    try:
        # 1. Obtener todos los productos actuales
        response = supabase.table('products').select('*').execute()
        current_products = response.data
        
        print(f"📦 Encontrados {len(current_products)} productos\n")
        
        # 2. Insertar en treatments
        migrated = 0
        for product in current_products:
            treatment = {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
                'category': product['category'],
                'image_url': product.get('image_url'),
                'is_active': product['is_active'],
                'stock': 999,  # Tratamientos siempre disponibles
                'duration': None  # Se puede actualizar después
            }
            
            try:
                supabase.table('treatments').insert(treatment).execute()
                print(f"✅ Migrado: {product['name']}")
                migrated += 1
            except Exception as e:
                print(f"❌ Error al migrar {product['name']}: {e}")
        
        print(f"\n🎉 Migración completada: {migrated}/{len(current_products)} tratamientos")
        
        # 3. Limpiar tabla products
        if migrated > 0:
            print("\n🧹 Limpiando tabla products...")
            supabase.table('products').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            print("✅ Tabla products limpiada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la migración: {e}")
        return False

if __name__ == "__main__":
    print("🌸 Kalai Medical Center - Migración de Servicios\n")
    print("="*50)
    migrate_services_to_treatments()
