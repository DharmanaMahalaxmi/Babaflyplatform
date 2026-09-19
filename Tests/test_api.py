import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base, get_db
from app.utils.security import get_password_hash
from app.models.user import User
from main import app

# In-memory SQLite for clean test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    # Seed default admin for testing product creation
    db = TestingSessionLocal()
    admin_user = User(
        name="Test Admin",
        email="testadmin@babafly.com",
        hashed_password=get_password_hash("AdminPass123!"),
        role="admin"
    )
    db.add(admin_user)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

# ==========================================
# 1. Test Case: User Registration
# ==========================================
def test_1_user_registration():
    payload = {
        "name": "Sarah Jenkins",
        "email": "sarah.jenkins@test.com",
        "password": "Password123!",
        "role": "user"
    }
    response = client.post("/api/users/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert data["role"] == "user"
    assert "id" in data
    assert "hashed_password" not in data  # Security check

    # Verify duplicate email is rejected
    duplicate_res = client.post("/api/users/register", json=payload)
    assert duplicate_res.status_code == 400

# ==========================================
# 2. Test Case: User Login
# ==========================================
def test_2_user_login():
    login_payload = {
        "email": "sarah.jenkins@test.com",
        "password": "Password123!"
    }
    response = client.post("/api/users/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "sarah.jenkins@test.com"

    # Test invalid password failure
    bad_login = client.post("/api/users/login", json={"email": "sarah.jenkins@test.com", "password": "WrongPassword"})
    assert bad_login.status_code == 401

# ==========================================
# 3. Test Case: Create Product (Admin Only)
# ==========================================
def test_3_create_product():
    # Login as admin to get admin token
    admin_login = client.post("/api/users/login", json={"email": "testadmin@babafly.com", "password": "AdminPass123!"})
    admin_token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}

    product_payload = {
        "name": "Infinity Gold Pendant",
        "description": "22K gold pendant with polished finish and certified hallmark.",
        "category": "Necklaces",
        "price": 540.0,
        "discount": 5.0,
        "stock": 30,
        "rating": 4.9,
        "metalType": "Gold",
        "polishType": "High Polish",
        "imageUrl": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600"
    }

    response = client.post("/api/products", json=product_payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_payload["name"]
    assert data["metalType"] == "Gold"
    assert data["polishType"] == "High Polish"
    assert data["price"] == 540.0
    assert "id" in data

    # Verify standard user cannot create product (Role-Based Access Control)
    user_login = client.post("/api/users/login", json={"email": "sarah.jenkins@test.com", "password": "Password123!"})
    user_token = user_login.json()["access_token"]
    forbidden_res = client.post("/api/products", json=product_payload, headers={"Authorization": f"Bearer {user_token}"})
    assert forbidden_res.status_code == 403

# ==========================================
# 4. Test Case: Fetch Product & Filters
# ==========================================
def test_4_fetch_product():
    # Fetch by ID
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Infinity Gold Pendant"

    # Fetch list with query filters
    filter_res = client.get("/api/products?metal=Gold&price_min=100&price_max=1000&sort=price_high")
    assert filter_res.status_code == 200
    list_data = filter_res.json()
    assert "products" in list_data
    assert "total" in list_data
    assert len(list_data["products"]) >= 1
    assert list_data["products"][0]["metalType"] == "Gold"

# ==========================================
# 5. Test Case: Create Order (JWT Required)
# ==========================================
def test_5_create_order():
    user_login = client.post("/api/users/login", json={"email": "sarah.jenkins@test.com", "password": "Password123!"})
    user_token = user_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {user_token}"}

    order_payload = {
        "items": [
            {
                "productId": 1,
                "name": "Infinity Gold Pendant",
                "price": 540.0,
                "quantity": 1,
                "imageUrl": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600"
            }
        ],
        "totalPrice": 540.0,
        "paymentStatus": "PAID",
        "address": "452 Orchid Boulevard, Suite 300, New York, NY"
    }

    response = client.post("/api/orders", json=order_payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["totalPrice"] == 540.0
    assert data["paymentStatus"] == "PAID"
    assert data["address"] == order_payload["address"]
    assert "id" in data
    assert "userId" in data

    # Verify fetching user's orders
    orders_res = client.get("/api/orders", headers=headers)
    assert orders_res.status_code == 200
    orders_list = orders_res.json()
    assert len(orders_list) >= 1
    assert orders_list[0]["id"] == data["id"]
