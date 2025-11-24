FROM python:3.10-slim

# Usar formato recomendado: KEY=VALUE
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para SQLite
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto completo
COPY . /app/

# Collect static (si lo necesitas)
# RUN python manage.py collectstatic --noinput

# Exponer puerto Django
EXPOSE 8000

# Variables de entorno recomendadas
ENV DJANGO_SETTINGS_MODULE=artezon_project.settings
ENV PYTHONPATH=/app

# Comando final
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
