#!/bin/bash
# Script para hacer deploy a Render

echo "🚀 Preparando deploy para Render..."

# Ir al directorio del backend
cd "$(dirname "$0")"

# Verificar git
if [ ! -d ".git" ]; then
    echo "❌ Error: No hay repositorio git en kalai-backend"
    echo "Por favor, inicializa git en el directorio raíz del proyecto"
    exit 1
fi

# Agregar cambios
echo "📦 Agregando archivos..."
git add requirements.txt runtime.txt .python-version app/auth.py

# Commit
echo "💾 Haciendo commit..."
git commit -m "Fix: Actualizar dependencias para Render (Python 3.11.9)"

# Push
echo "⬆️  Subiendo a GitHub..."
git push

echo "✅ Deploy enviado! Render detectará los cambios automáticamente."
echo "📊 Monitorea el deploy en: https://dashboard.render.com"
