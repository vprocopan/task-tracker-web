# Use a lightweight Python base image
FROM python:3.14-alpine

# Set working directory
WORKDIR /app

# Copy requirements if you have them, or just Flask
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || pip install flask gunicorn

# Copy your project files
COPY . .

# Use Gunicorn to serve Flask
CMD ["gunicorn", "-b", "0.0.0.0:7777", "app:app"]