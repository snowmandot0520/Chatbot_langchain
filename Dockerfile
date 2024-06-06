# Stage 1: Build React app
FROM node:16-alpine as frontend

# Set working directory
WORKDIR /app

# Copy the frontend code
COPY client/package*.json ./
COPY client/vite.config.js ./

# Install dependencies and build the frontend
RUN npm install
COPY client/ ./
RUN npm run build

# Stage 2: Setup Django app
FROM python:3.11.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY . /app/

# Copy the built React files to Django's static files directory
COPY --from=frontend /app/dist /app/client/dist

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
