FROM python:3.10-slim

# OpenCV এর জন্য প্রয়োজনীয় সিস্টেম লাইব্রেরি
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements কপি ও ইনস্টল
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# প্রজেক্টের সব ফাইল কপি
COPY . .

# Static ফাইল ও Database Migration
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate

# Render পোর্ট হ্যান্ডেল করা
EXPOSE 10000

# Gunicorn দিয়ে অ্যাপ চালু (neurohealth_project এর জায়গায় আপনার আসল প্রজেক্ট নাম দিন)
CMD ["gunicorn", "neurohealth_project.wsgi:application", "--bind", "0.0.0.0:10000"]