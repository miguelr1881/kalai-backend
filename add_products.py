#!/usr/bin/env python3
"""
Script para agregar productos de ejemplo (cremas, cosméticos, etc.)
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

# Productos de ejemplo
products = [
    {
        "name": "Crema Solar SPF 50+",
        "description": "Protección solar de amplio espectro. Ideal para uso diario, resistente al agua, no comedogénico.",
        "price": 15000,
        "category": "Protección Solar",
        "stock": 25,
        "is_active": True
    },
    {
        "name": "Sérum Vitamina C",
        "description": "Sérum antioxidante con vitamina C pura al 20%. Ilumina, unifica el tono y previene el envejecimiento.",
        "price": 22000,
        "category": "Sérums",
        "stock": 18,
        "is_active": True
    },
    {
        "name": "Crema Hidratante Ácido Hialurónico",
        "description": "Hidratación profunda con ácido hialurónico de bajo y alto peso molecular. Para todo tipo de piel.",
        "price": 18000,
        "category": "Hidratantes",
        "stock": 30,
        "is_active": True
    },
    {
        "name": "Limpiador Facial Suave",
        "description": "Gel limpiador sin sulfatos, pH balanceado. Remueve impurezas sin resecar la piel.",
        "price": 12000,
        "category": "Limpiadores",
        "stock": 35,
        "is_active": True
    },
    {
        "name": "Exfoliante Químico AHA/BHA",
        "description": "Tónico exfoliante con ácidos glicólico y salicílico. Mejora textura, poros y luminosidad.",
        "price": 20000,
        "category": "Exfoliantes",
        "stock": 15,
        "is_active": True
    },
    {
        "name": "Mascarilla Purificante Carbón",
        "description": "Mascarilla de arcilla con carbón activado. Limpia profundamente y minimiza poros.",
        "price": 14000,
        "category": "Mascarillas",
        "stock": 22,
        "is_active": True
    },
    {
        "name": "Contorno de Ojos Anti-edad",
        "description": "Crema específica para contorno de ojos con péptidos y cafeína. Reduce ojeras y líneas de expresión.",
        "price": 25000,
        "category": "Contorno de Ojos",
        "stock": 12,
        "is_active": True
    },
    {
        "name": "Crema Noche Retinol",
        "description": "Crema regeneradora nocturna con retinol encapsulado. Estimula renovación celular y producción de colágeno.",
        "price": 28000,
        "category": "Tratamientos Nocturnos",
        "stock": 10,
        "is_active": True
    },
    {
        "name": "Agua Micelar",
        "description": "Agua micelar 3 en 1: limpia, desmaquilla y tonifica. Sin necesidad de enjuague.",
        "price": 11000,
        "category": "Limpiadores",
        "stock": 40,
        "is_active": True
    },
    {
        "name": "Sérum Niacinamida 10%",
        "description": "Sérum con niacinamida al 10% y zinc. Controla sebo, minimiza poros y unifica el tono.",
        "price": 19000,
        "category": "Sérums",
        "stock": 20,
        "is_active": True
    }
]

def main():
    print("🧴 Agregando productos de skincare...\n")
    
    success_count = 0
    for product in products:
        try:
            response = supabase.table('products').insert(product).execute()
            print(f"✅ {product['name']} - ₡{product['price']:,} (Stock: {product['stock']})")
            success_count += 1
        except Exception as e:
            print(f"❌ Error al agregar {product['name']}: {e}")
    
    print(f"\n🎉 Proceso completado: {success_count}/{len(products)} productos agregados exitosamente")

if __name__ == "__main__":
    main()
