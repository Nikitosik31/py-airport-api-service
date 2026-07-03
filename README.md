# Airport API Service

RESTful API for managing airport operations — flights, routes, airplanes, crew, and ticket orders.

## Technologies

- **Python 3.13** / **Django 6**
- **Django REST Framework** — API
- **JWT Authentication** — via `djangorestframework-simplejwt`
- **PostgreSQL** — database
- **Docker** + **Docker Compose** — containerization
- **Gunicorn** — production WSGI server
- **drf-spectacular** — Swagger / ReDoc documentation

## Features

- JWT-based authentication (register, login, token refresh)
- Flight management with filtering by date, source, destination, airplane
- Airplane management with image upload
- Route, crew, airport, country, city management
- Order creation with nested ticket validation
- Ticket seat/row validation against airplane capacity
- Pagination on all list endpoints
- Admin panel with search and filtering

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Run with Docker

1. Clone the repository:
```bash
git clone https://github.com/Nikitosik31/py-airport-api-service.git
cd py-airport-api-service
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Fill in the `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*

POSTGRES_DB=airport_db
POSTGRES_USER=airport_user
POSTGRES_PASSWORD=airport_pass
DATABASE_NAME=airport_db
DATABASE_USER=airport_user
DATABASE_PASSWORD=airport_pass
DATABASE_HOST=db
DATABASE_PORT=5432
```

4. Build and run:
```bash
docker-compose up --build
```

5. The API will be available at: `http://localhost:8001/`

### API Documentation

- Swagger UI: `http://localhost:8001/api/doc/swagger/`
- ReDoc: `http://localhost:8001/api/doc/redoc/`

## API Endpoints

| Endpoint | Description |
|---|---|
| `POST /api/user/register/` | Register new user |
| `POST /api/user/token/` | Get JWT token |
| `POST /api/user/token/refresh/` | Refresh JWT token |
| `GET /api/airport/flights/` | List flights (with filters) |
| `GET /api/airport/airplanes/` | List airplanes |
| `GET /api/airport/routes/` | List routes |
| `GET /api/airport/orders/` | List user orders |
| `POST /api/airport/orders/` | Create order with tickets |

## Running Tests

```bash
docker-compose run app python manage.py test airport.tests
```

## Getting Access

1. Register: `POST /api/user/register/` with `{"email": "...", "password": "..."}`
2. Get token: `POST /api/user/token/` with the same credentials
3. Use the token in the `Authorization` header: `Bearer <your_token>`
