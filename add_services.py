#!/usr/bin/env python3
"""
Script para agregar todos los servicios de Kalai Medical Center a la base de datos
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

# Servicios a agregar
services = [
    {
        "name": "Asesoría Rutina de Skincare",
        "description": "Diseñamos tu rutina ideal según tu tipo de piel, necesidades y presupuesto. Resultados reales, sin complicarte.",
        "price": 30000,
        "category": "Consultoría",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Valoración Médica Integral",
        "description": "Tu piel, profundamente analizada. Incluye: Rutina personalizada, Hydrafacial durante la cita y Plan personalizado.",
        "price": 40000,
        "category": "Consultoría",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Hydrafacial",
        "description": "Limpieza profunda + hidratación avanzada + glow inmediato. Requiere valoración previa si es tu primera sesión.",
        "price": 35000,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Radiofrecuencia Facial (5 Sesiones)",
        "description": "Reafirma, mejora textura y estimula colágeno para una piel más firme y luminosa.",
        "price": 125000,
        "category": "Paquetes",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Hydra Premium",
        "description": "Hydrafacial + Radiofrecuencia + Ultrasonido. Una experiencia completa para hidratación profunda y efecto lifting inmediato.",
        "price": 40000,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Peelings Químicos",
        "description": "Protocolos médicos para: manchas, acné, rosácea y envejecimiento. Mejora textura, tono y luminosidad.",
        "price": 40000,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Relleno de Labios",
        "description": "Reafirma, mejora textura y estimula colágeno para una piel más firme y luminosa.",
        "price": 350,
        "category": "Tratamientos Estéticos",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Facial Coreano",
        "description": "Aprende a utilizar productos coreanos mientras te realizamos una limpieza facial con productos personalizados a tu tipo de piel.",
        "price": 35000,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Toxina Botulínica - Full Face",
        "description": "Rejuvenecimiento natural, sin perder expresión. Tratamiento completo para rostro.",
        "price": 300,
        "category": "Tratamientos Estéticos",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Toxina Botulínica - Por Zona",
        "description": "Rejuvenecimiento natural, sin perder expresión. Tratamiento por zona específica.",
        "price": 150,
        "category": "Tratamientos Estéticos",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Enzimas Recombinantes - Paquete Papada (3 Sesiones)",
        "description": "Incluye sesión de radiofrecuencia de regalo. Reduce grasa localizada y define contornos.",
        "price": 600,
        "category": "Paquetes",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Enzimas Recombinantes - Paquete Abdomen (3 Sesiones + 3 Masajes)",
        "description": "Incluye sesión de radiofrecuencia de regalo. Reduce grasa localizada y define contornos.",
        "price": 600,
        "category": "Paquetes",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Microagujas",
        "description": "Incluye anestesia, procedimiento y mascarilla domiciliaria. Para cicatrices, poros, manchas y firmeza.",
        "price": 65000,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "Microagujas con Exosomas",
        "description": "Regeneración celular avanzada para resultados superiores. Incluye tratamiento de microagujas + exosomas.",
        "price": 200,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "IPL - Por Zona",
        "description": "Manchas | Acné | Rosácea. Zonas: rostro, espalda, escote y manos.",
        "price": 250,
        "category": "Tratamientos Faciales",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "IPL - Paquete Acné (5 Sesiones)",
        "description": "Tratamiento completo para acné con IPL. 5 sesiones.",
        "price": 500,
        "category": "Paquetes",
        "stock": 999,
        "is_active": True
    },
    {
        "name": "IPL - Paquete Manchas (3 Sesiones)",
        "description": "Tratamiento completo para manchas con IPL. 3 sesiones.",
        "price": 600,
        "category": "Paquetes",
        "stock": 999,
        "is_active": True
    }
]

def main():
    print("🌸 Agregando servicios de Kalai Medical Center...\n")
    
    # Primero, eliminar los productos de ejemplo anteriores (opcional)
    try:
        response = supabase.table('products').delete().in_('name', [
            'Limpieza Facial Profunda',
            'Masaje Relajante',
            'Tratamiento Anti-Edad',
            'Hydrafacial Premium'
        ]).execute()
        print(f"✅ Productos de ejemplo eliminados\n")
    except Exception as e:
        print(f"⚠️  Error al eliminar productos anteriores: {e}\n")
    
    # Agregar nuevos servicios
    success_count = 0
    for service in services:
        try:
            response = supabase.table('products').insert(service).execute()
            print(f"✅ {service['name']} - ${service['price']} ({service['category']})")
            success_count += 1
        except Exception as e:
            print(f"❌ Error al agregar {service['name']}: {e}")
    
    print(f"\n🎉 Proceso completado: {success_count}/{len(services)} servicios agregados exitosamente")

if __name__ == "__main__":
    main()
