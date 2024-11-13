ARG PYTHON_IMAGE=python:3.10
ARG PYTHON_PORT=8000
FROM ${PYTHON_IMAGE}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the contents of the Django project into the container
COPY app/ /app/
COPY .env /app/.env

# Expose the port your app runs on
EXPOSE ${PYTHON_PORT}

# Run your application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
