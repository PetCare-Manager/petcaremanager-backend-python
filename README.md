# PetCareManager Backend


# Steps


## Requirements
- make
- docker
- docker compose

## Setup

1. **Clone the repository**
2. **Set up the environment variables:**
    
    - Create a `.env` file in the root directory following the `.env.example`
    - Create a `.env` file in the `/docker/local` directory following the `/docker/local/.env.example`

3. **Build the project!**
    ~~~sh
    make build
    make urls
    ~~~


export MYSQL_USER=petcaremysql2
export MYSQL_PASSWORD=TU_CONTRASEÑA
export MYSQL_DATABASE=petcaremysql2
export MYSQL_HOST=petcaremysql2.mysql.pythonanywhere-services.com
export PYTHONANYWHERE=true
export Entorno=desarrollo
