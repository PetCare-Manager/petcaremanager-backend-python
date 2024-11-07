# PetCareManager Backend (Python)

## Requirements
- Docker _(in progress)_
- make _(in progress)_
- Python 3.8+
- pip (Python package installer)

## Setup

1. **Clone the repository:**
2. **Create a virtual environment for the project:**

    ```sh
    python -m venv venv
    ```
3. **Activate the virtual environment**
    
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    
3. **Install the dependencies:**

    ```sh
    make build
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory

5. **Start the project**
    ```sh
    make start
    ```