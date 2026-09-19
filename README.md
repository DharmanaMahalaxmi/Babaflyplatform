# BabaFly Platform - Python FastAPI Backend Application

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT%20Bearer-black.svg?style=flat&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Pytest](https://img.shields.io/badge/Tests-5%20Passing-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)

A production-grade Python backend system built for the **BabaFly Platform** under the **InfoBharatInterns (IBI) Python Development Internship Program**.

---

## 📌 Project Architecture

The application is structured following clean **MVC / MVT** layered architecture with high cohesion and loose coupling:

```text
/
├── app/
│   ├── config/             # Database connection & App Settings (Pydantic Settings)
│   │   ├── database.py
│   │   └── settings.py
│   ├── models/             # SQLAlchemy ORM Database Models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── order.py
│   ├── schemas/            # Pydantic v2 Request/Response Validation Models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── order.py
│   ├── services/           # Business Logic Layer
│   │   ├── user_service.py
│   │   ├── category_service.py
│   │   ├── product_service.py
│   │   └── order_service.py
│   ├── controllers/        # Request Orchestration Layer
│   │   ├── user_controller.py
│   │   ├── category_controller.py
│   │   ├── product_controller.py
│   │   └── order_controller.py
│   ├── routes/             # FastAPI Route Endpoints & Tags
│   │   ├── user_routes.py
│   │   ├── category_routes.py
│   │   ├── product_routes.py
│   │   └── order_routes.py
│   └── utils/              # Security (bcrypt, JWT), Logger & Middlewares
│       ├── security.py
│       └── logger.py
├── tests/                  # Automated pytest Suite (5 mandatory test cases)
│   └── test_api.py
├── main.py                 # Application Entrypoint, Middlewares & Auto Seed
├── requirements.txt        # Production Dependencies
├── Dockerfile              # Containerization specification
├── docker-compose.yml      # Multi-container PostgreSQL + API orchestration
└── README.md               # Complete Setup & Documentation
```

---

## 🚀 Key Features

- **Authentication & Security:**
  - Password hashing with `bcrypt` (salted)
  - JWT Access Token generation & Bearer verification
  - Unique email validation
  - Role-Based Access Control (`Admin` vs `User`)
- **Product Management:**
  - Full CRUD operations (Admin-protected write/delete)
  - Rich jewelry schema: `metalType` (Gold, Platinum, Silver, Rose Gold), `polishType` (High Polish, Matte, Antique)
  - Advanced filtering (`?price_min=`, `?price_max=`, `?metal=`, `?polish=`)
  - Sorting (`?sort=latest | price_low | price_high | rating | popularity`)
  - Offset Pagination (`?page=&limit=`)
- **Category Management:**
  - Category listings and Category-wise product filtering (`GET /api/categories/{id}/products`)
- **Order Management:**
  - Customer order placement with JWT validation
  - Personal order history & detail inspection
- **Production Hardening:**
  - Structured request logging with processing time (`X-Process-Time`)
  - Centralized global error handling middleware
  - Auto-generated interactive Swagger UI & ReDoc

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **FastAPI** | High-performance asynchronous Python web framework |
| **PostgreSQL / SQLite** | Relational Database storage |
| **SQLAlchemy 2.0** | Object-Relational Mapping (ORM) |
| **Pydantic v2** | Data schema validation and serialization |
| **python-jose & Passlib** | JWT token management & bcrypt password hashing |
| **Pytest & HTTPX** | Automated integration testing |
| **Uvicorn** | Lightning-fast ASGI web server |

---

## ⚡ Quick Start Guide

### 1. Clone the Repository & Set Up Virtual Environment

```bash
git clone https://github.com/your-username/babafly-python-backend.git
cd babafly-python-backend

python3 -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
PROJECT_NAME="BabaFly Platform Backend API"
SECRET_KEY="your-super-secret-jwt-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# For SQLite (default out of the box):
DATABASE_URL="sqlite:///./babafly.db"

# For PostgreSQL:
# DATABASE_URL="postgresql://babafly_user:babafly_password@localhost:5432/babafly_db"
```

### 4. Run the Application

```bash
uvicorn main:app --reload --port 8000
```

Once running:
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 🐳 Docker Deployment

To spin up both **PostgreSQL** and the **FastAPI Backend** with a single command:

```bash
docker-compose up --build -d
```

Access Swagger UI at `http://localhost:8000/docs`.

---

## 🧪 Automated Testing (Pytest)

Run the mandatory 5 automated test cases:

```bash
pytest -v tests/test_api.py
```

### Verified Test Cases:
1. `test_1_user_registration` - Register user, check unique email validation
2. `test_2_user_login` - Authenticate, obtain JWT token, check invalid credentials
3. `test_3_create_product` - Admin-only product creation & Role-Based Access Control verification
4. `test_4_fetch_product` - Fetch product by ID and test query filters (`price_min`, `price_max`, `metal`, `sort`)
5. `test_5_create_order` - Place order with JWT authentication and query order history

---

## 📡 API Endpoints Reference

### 1. User & Authentication Module
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/register` | Register new user | None |
| `POST` | `/api/users/login` | Login and receive Bearer JWT | None |
| `GET` | `/api/users/profile` | Fetch profile details | JWT Bearer |

### 2. Product Module
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/products` | Filter & sort products | None |
| `GET` | `/api/products/{id}` | Get product details | None |
| `POST` | `/api/products` | Create product | Admin JWT |
| `PUT` | `/api/products/{id}` | Update product | Admin JWT |
| `DELETE` | `/api/products/{id}` | Delete product | Admin JWT |

### 3. Category Module
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/categories` | List all categories | None |
| `GET` | `/api/categories/{id}/products` | List products by category | None |
| `POST` | `/api/categories` | Add category | Admin JWT |

### 4. Order Module
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/orders` | Place a customer order | JWT Bearer |
| `GET` | `/api/orders` | View user's order history | JWT Bearer |
| `GET` | `/api/orders/{id}` | View specific order | JWT Bearer |

---

## 🎥 Submission Checklist for InfoBharatInterns

- [x] Production code follows **PEP8** standards with clean MVC architecture
- [x] Password hashing with **bcrypt** and **JWT authentication**
- [x] Admin Role-Based Access Control on Product mutations
- [x] Filtering (`price_min`, `price_max`, `metal`, `polish`), Sorting, and Pagination implemented
- [x] Global Error-Handling and Request Logging Middlewares configured
- [x] 5 Automated Test Cases passing via `pytest`
- [x] Ready for GitHub upload with comprehensive `README.md`
- [x] Ready for Postman / Swagger demo video recording

**Internship Submission:** Tag `@InfoBharatInterns` on LinkedIn with your live deployed URL and demo video!
