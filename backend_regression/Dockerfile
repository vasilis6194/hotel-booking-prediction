# Use an official Python image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Regression API
EXPOSE 8000

# Command to run the Regression API
CMD ["uvicorn", "main_regression_api:app", "--host", "0.0.0.0", "--port", "8000"]
