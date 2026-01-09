# 🏥 Kalai Medical Center - Backend API

API REST desarrollada con FastAPI para la gestión de productos y servicios de Kalai Medical Center.

## 🚀 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Supabase** - Base de datos PostgreSQL y storage
- **Python 3.11+** - Lenguaje de programación
- **JWT** - Autenticación para panel admin

## 📋 Prerequisitos

- Python 3.11 o superior
- Cuenta de Supabase
- pip o pipenv

## 🔧 Instalación Local

1. **Clonar el repositorio**
```bash
cd kalai-backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. **Ejecutar la base de datos**
- Ve a tu proyecto en Supabase
- SQL Editor → ejecuta el archivo `database/schema.sql`

6. **Iniciar el servidor**
```bash
uvicorn main:app --reload
```

El servidor estará corriendo en `http://localhost:8000`

## 📚 Documentación API

Una vez el servidor esté corriendo:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔑 Endpoints Principales

### Públicos (sin autenticación)
- `GET /api/public/products` - Listar productos activos
- `GET /api/public/products/{id}` - Ver producto específico
- `GET /api/public/categories` - Listar categorías
- `GET /api/public/whatsapp-link/{id}` - Generar link de WhatsApp

### Admin (requiere autenticación)
- `POST /api/admin/login` - Login de administrador
- `GET /api/admin/products` - Listar todos los productos
- `POST /api/admin/products` - Crear producto
- `PUT /api/admin/products/{id}` - Actualizar producto
- `DELETE /api/admin/products/{id}` - Eliminar producto
- `PATCH /api/admin/products/{id}/toggle-active` - Activar/desactivar
- `PATCH /api/admin/products/{id}/stock` - Actualizar stock

## 🔐 Autenticación Admin

Para acceder a endpoints admin:

1. Login:
```bash
curl -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"kalai2026"}'
```

2. Usar el token en requests:
```bash
curl http://localhost:8000/api/admin/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🌍 Deploy en Render

1. Crear cuenta en [render.com](https://render.com)
2. Conectar tu repositorio de GitHub
3. Crear nuevo Web Service
4. Configurar:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agregar variables de entorno desde el archivo `.env`
6. Deploy!

## 📁 Estructura del Proyecto

```
kalai-backend/
├── app/
│   ├── __init__.py
│   ├── config.py           # Configuración y variables de entorno
│   ├── database.py         # Conexión a Supabase
│   ├── models.py           # Modelos Pydantic
│   ├── auth.py             # Autenticación JWT
│   └── routes/
│       ├── __init__.py
│       ├── public.py       # Endpoints públicos
│       └── admin.py        # Endpoints admin
├── database/
│   └── schema.sql          # Schema de base de datos
├── main.py                 # Aplicación principal
├── requirements.txt        # Dependencias Python
├── .env.example           # Template de variables
├── .env                   # Variables de entorno (no subir a git)
└── README.md
```

## 🔒 Seguridad

- Las credenciales están en variables de entorno
- JWT para autenticación admin
- CORS configurado para dominios específicos
- Row Level Security (RLS) en Supabase
- Service role key solo en backend

## 👥 Credenciales por Defecto

**IMPORTANTE**: Cambiar en producción

- Username: `admin`
- Password: `kalai2026`

## 🆘 Troubleshooting

**Error de conexión a Supabase**
- Verificar que las variables SUPABASE_URL y SUPABASE_SERVICE_KEY sean correctas
- Verificar que la tabla `products` exista en Supabase

**Error 401 en endpoints admin**
- Verificar que el token JWT sea válido
- Verificar que el token esté en el header Authorization

## 📝 Licencia

Proyecto privado - Kalai Medical Center

## 👨‍💻 Desarrollado por

Miguel R. - 2026
