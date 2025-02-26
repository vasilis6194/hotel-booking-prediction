# Use an official Python image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Classification API
EXPOSE 8001

# Command to run the Classification API
CMD ["uvicorn", "main_classification_api:app", "--host", "0.0.0.0", "--port", "8001"]
