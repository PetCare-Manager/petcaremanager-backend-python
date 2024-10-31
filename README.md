# PetCareManager Backend (Python)

This is the backend for the PetCareManager application, built with FastAPI.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features
- APIRest 
- SQLAlchemy for database interactions
- SQLite for database
- Pydantic for data validation
- JWT for authentication

## Requirements
- Python 3.8+
- pip (Python package installer)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/petcaremanager-backend-python.git
    cd petcaremanager-backend-python
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```env
    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=your_secret_key
    ```


## Running the Application
1. **Start the FastAPI server:**
    ```sh
    uvicorn app.main:app --reload
    ```

2. **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000`.



## API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- Swagger UI: `http://127.0.0.1:8000/docs`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.