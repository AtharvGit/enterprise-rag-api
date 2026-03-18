# Use a lightweight Python 3.11 image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install build dependencies for ChromaDB and sentence-transformers
RUN apt-get update && apt-get install -y build-essential

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]