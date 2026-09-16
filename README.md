## Home Helper Service (backend)

### The project documentation is stored in the folder "docs".

### 1.Create file .env-dev

    DB__DATABASE_URL=
    DB__ECHO_LOG=
    AUTH__JWT_SECRET_KEY=
    AUTH__JWT_ALGORITHM=
    AUTH__ACCESS_TOKEN_EXPIRE_MINUTES=
    AUTH__REFRESH_TOKEN_EXPIRE_DAYS=

### 2.Docker start
#### start from build
    docker compose up --build
#### start
    docker compose up

<hr>

### Api docs
    http://127.0.0.1:8000/docs#/


