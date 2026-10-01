# ShopAPI

ShopAPI is a backend-focused e-commerce REST API built with Django REST Framework and PostgreSQL.

The project demonstrates the architecture of a modern REST API, including relational data modeling, serialization, CRUD operations, JWT authentication, role-based permissions, ownership protection, automated testing, OpenAPI documentation, and production-oriented architecture.

![ShopAPI Home Page](screenshots/shopapi-home.png)

---

## Key Highlights

- Django REST Framework architecture
- PostgreSQL database
- RESTful API design
- JSON request and response flow
- Product and category management
- Order and order item management
- Custom user model
- JWT authentication
- Access and refresh tokens
- Authentication and authorization
- Role-based product permissions
- User-specific order ownership
- Ownership-protected API operations
- OpenAPI schema
- Interactive Swagger UI
- JWT authorization through Swagger
- 26 automated tests passing
- Environment-based configuration
- Modular Django application structure
- Production-oriented architecture

---

## API Architecture

ShopAPI follows a layered Django REST Framework architecture.

![ShopAPI System Architecture](screenshots/system-architecture.png)

The main request flow can be summarized as:

    API Client / Frontend / Postman
                │
                ▼
           REST Endpoint
                │
                ▼
        JWT Authentication
                │
                ▼
           Permissions
                │
                ▼
             ViewSet
                │
                ▼
           Serializer
                │
                ▼
           Django ORM
                │
                ▼
           PostgreSQL
                │
                ▼
          JSON Response

Each layer has a separate responsibility:

- **Model** defines the database structure.
- **Serializer** converts model data to and from JSON and performs validation.
- **ViewSet** manages API behavior and CRUD operations.
- **Router** generates REST API routes for ViewSets.
- **JWT Authentication** identifies authenticated users.
- **Permissions** determine what authenticated users are allowed to do.
- **Django ORM** communicates with PostgreSQL.
- **PostgreSQL** stores persistent application data.

---

## Product and Category API

ShopAPI provides REST endpoints for managing e-commerce products and categories.

Product functionality includes:

- Product listing
- Product detail
- Product creation
- Product updates
- Product deletion
- Category relationships
- Product stock management
- Product pricing
- Active/inactive product state
- Serializer validation

Product write operations are protected using role-based permissions.

Public users can read product data, while product creation, modification, and deletion require staff privileges.

### Product Endpoints

    GET    /api/products/
    POST   /api/products/

    GET    /api/products/<id>/
    PUT    /api/products/<id>/
    PATCH  /api/products/<id>/
    DELETE /api/products/<id>/

![ShopAPI Product Endpoints](screenshots/products-swagger-endpoints.png)

### Category Endpoints

    GET    /api/categories/
    POST   /api/categories/

    GET    /api/categories/<id>/
    PUT    /api/categories/<id>/
    PATCH  /api/categories/<id>/
    DELETE /api/categories/<id>/

---

## JWT Authentication

ShopAPI uses JWT authentication through Django REST Framework SimpleJWT.

Authentication functionality includes:

- User registration
- JWT login
- Access token generation
- Refresh token generation
- Access token renewal
- Authenticated profile endpoint
- Protected API endpoints

### User Endpoints

    POST /api/users/register/
    POST /api/users/token/
    POST /api/users/token/refresh/
    GET  /api/users/profile/

![ShopAPI User and JWT Endpoints](screenshots/users-jwt-endpoints.png)

### JWT Authentication Flow

    User
     │
     ▼
    Login Request
     │
     ▼
    Username + Password
     │
     ▼
    JWT Token Endpoint
     │
     ├── Access Token
     │
     └── Refresh Token
            │
            ▼
    Authorization: Bearer <access_token>
            │
            ▼
    JWTAuthentication
            │
            ▼
    request.user
            │
            ▼
    Protected API Endpoint

The access token authenticates API requests.

The refresh token can be used to obtain a new access token without requiring the user to submit login credentials again.

---

## Swagger JWT Authorization

Swagger UI is integrated with JWT authentication.

![ShopAPI JWT Authorization](screenshots/jwt-authorization.png)

The Swagger authentication flow is:

    Login
      │
      ▼
    Receive Access Token
      │
      ▼
    Swagger Authorize
      │
      ▼
    JWT Bearer Authentication
      │
      ▼
    Protected Endpoint
      │
      ▼
    Authenticated Response

This allows protected API functionality to be tested directly through the interactive API documentation.

---

## Authentication, Authorization and Ownership

ShopAPI separates three important backend security concepts.

### Authentication

Authentication answers:

> Who is the user?

JWT authentication identifies the user making the API request.

### Authorization

Authorization answers:

> What is the authenticated user allowed to do?

Permissions determine whether the authenticated user can perform a particular operation.

### Ownership

Ownership answers:

> Which records belong to the authenticated user?

Orders and order items are restricted to their authenticated owners.

Security rules are enforced by the backend rather than relying on frontend restrictions.

---

## Roles and Permissions

![ShopAPI Roles and Permissions](screenshots/roles-permissions.png)

### Public Users

Public users can perform safe product read operations:

    GET
    HEAD
    OPTIONS

### Authenticated Normal Users

Normal authenticated users can read products but cannot create, modify, or delete them.

Restricted product write operations return:

    403 Forbidden

Authenticated users can work with their own protected order data.

### Staff / Admin Users

Staff users can perform product management operations including:

    POST
    PUT
    PATCH
    DELETE

This creates a clear separation between public API access, authenticated user operations, and administrative functionality.

---

## Order Management

ShopAPI includes relational order management through `Order` and `OrderItem`.

### Order

An order belongs to an authenticated user.

Orders contain:

- User ownership
- Order status
- Creation timestamp
- Update timestamp
- Related order items

Supported statuses:

    pending
    processing
    shipped
    delivered
    cancelled

### OrderItem

Order items connect products with orders.

Each order item contains:

- Related order
- Related product
- Quantity
- Price

The relationship can be summarized as:

    User
     │
     ▼
    Order
     │
     ▼
    OrderItem
     │
     ▼
    Product

### Order API Endpoints

    GET    /api/orders/orders/
    POST   /api/orders/orders/

    GET    /api/orders/orders/<id>/
    PUT    /api/orders/orders/<id>/
    PATCH  /api/orders/orders/<id>/
    DELETE /api/orders/orders/<id>/

### Order Item Endpoints

    GET    /api/orders/order-items/
    POST   /api/orders/order-items/

    GET    /api/orders/order-items/<id>/
    PUT    /api/orders/order-items/<id>/
    PATCH  /api/orders/order-items/<id>/
    DELETE /api/orders/order-items/<id>/

![ShopAPI Order Endpoints](screenshots/orders-swagger-endpoints.png)

---

## Ownership Protection

Order data is user-specific.

The core ownership rule is:

> An authenticated user can access only orders and order items that belong to that user.

Order querysets are restricted using the authenticated user.

Conceptually:

    Order.objects.filter(user=request.user)

Order items follow the same ownership principle through their related order.

This prevents authenticated users from accessing another user's protected order data by manually changing object IDs.

Ownership is enforced by the backend.

---

## OpenAPI and Swagger Documentation

ShopAPI includes automatically generated OpenAPI documentation using `drf-spectacular`.

![ShopAPI Swagger Documentation](screenshots/swagger-api-documentation.png)

### OpenAPI Schema

    /api/schema/

The OpenAPI schema provides a machine-readable description of the API, including endpoints, request structures, response structures, and authentication requirements.

### Swagger UI

    /api/docs/

Swagger UI provides an interactive browser interface for exploring and testing ShopAPI.

Developers can:

- Browse REST endpoints
- Inspect request schemas
- Inspect response schemas
- Execute API requests
- Test CRUD operations
- Authenticate using JWT
- Test protected endpoints

---

## Automated Testing

ShopAPI includes automated API tests covering application behavior and security rules.

### Current Test Status

    26 tests passed successfully.

![ShopAPI Automated Tests](screenshots/automated-tests.png)

The test suite covers functionality including:

- Product listing
- Product detail
- Product creation
- Product updates
- Product deletion
- Invalid product data
- Authentication
- User registration
- JWT token generation
- JWT token refresh
- Protected profile access
- Order CRUD operations
- Order ownership
- Order item ownership
- Public product access
- Normal-user product restrictions
- Staff product permissions
- Authentication requirements
- Authorization rules
- Security behavior

Run the complete test suite with:

    python manage.py test

A passing regression suite helps ensure that existing API behavior and security rules continue working as the project evolves.

---

## Tech Stack

![ShopAPI Technology Stack](screenshots/technology-stack.png)

### Backend

- Python 3.12.10
- Django 5.2.17
- Django REST Framework 3.18.1
- Django ORM

### Database

- PostgreSQL 17.11

### Authentication

- SimpleJWT 5.5.1
- JWT Access Tokens
- JWT Refresh Tokens
- Bearer Authentication

### API Documentation

- OpenAPI
- Swagger UI
- drf-spectacular 0.30.0

### Configuration and Database Connectivity

- python-dotenv
- dj-database-url
- psycopg

### Testing

- Django Test Framework
- Django REST Framework APITestCase
- Authentication tests
- Permission tests
- Ownership tests
- API regression tests

### Development and Version Control

- Git
- GitHub
- Visual Studio Code

---

## Project Structure

ShopAPI follows a modular Django application architecture.

    ShopAPI/
    │
    ├── config/              # Django project configuration
    ├── core/                # Homepage and core functionality
    ├── users/               # Custom user and JWT authentication
    ├── products/            # Categories, products and permissions
    ├── orders/              # Orders, order items and ownership
    │
    ├── templates/           # Project templates
    ├── static/              # CSS and static assets
    ├── screenshots/         # Project screenshots
    │
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md

Each Django application is responsible for a specific part of the system, keeping the project modular, maintainable, and easier to test.

---

## Installation and Local Setup

### 1. Clone the Repository

    git clone https://github.com/taner-sahin/ShopAPI.git
    cd ShopAPI

### 2. Create a Virtual Environment

    python -m venv venv

Windows:

    venv\Scripts\activate

Linux:

    source venv/bin/activate

### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure Environment Variables

Create a local `.env` file based on `.env.example`.

Sensitive configuration such as the Django secret key and PostgreSQL credentials must never be committed to GitHub.

Example:

    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE

Use your own PostgreSQL credentials.

### 5. Configure PostgreSQL

ShopAPI uses PostgreSQL as its application database.

Create a PostgreSQL database and database user, then configure the connection through `DATABASE_URL`.

### 6. Apply Database Migrations

    python manage.py migrate

### 7. Run the Development Server

    python manage.py runserver

Local application:

    http://127.0.0.1:8000/

Local Swagger documentation:

    http://127.0.0.1:8000/api/docs/

---

## Environment Variables

ShopAPI separates sensitive configuration from source code using environment variables.

Configuration includes:

- Django secret key
- Debug mode
- Allowed hosts
- PostgreSQL database connection

The real `.env` file remains private and is excluded from version control.

The repository provides `.env.example` as a configuration template.

---

## Security Design

ShopAPI security rules are enforced directly by the backend.

Important security principles include:

- JWT authentication
- Authentication-protected endpoints
- Role-based permissions
- Staff-only product write operations
- User-specific order querysets
- Order ownership protection
- Order item ownership protection
- Environment-based secrets
- PostgreSQL credentials excluded from version control
- Automated permission tests
- Automated ownership tests

The frontend is never relied upon to enforce API authorization or ownership.

---

## Test and Production Architecture

ShopAPI is designed around the complete API lifecycle: development, security, testing, documentation, and production deployment.

![ShopAPI Test and Production Architecture](screenshots/test-production.png)

---

## Production Deployment

Production deployment is the next project stage.

The planned production request flow is:

    API Client
        │
        ▼
    Domain / DNS
        │
        ▼
    HTTPS / SSL/TLS
        │
        ▼
    Nginx
        │
        ▼
    Gunicorn
        │
        ▼
    Django REST Framework
        │
        ▼
    PostgreSQL

The deployment stage will include:

- VPS
- Ubuntu Linux
- PostgreSQL
- Gunicorn
- Nginx
- systemd
- Domain and DNS configuration
- SSL/TLS
- HTTPS
- HSTS
- Production security configuration
- Production API verification

This section will be updated with the real production configuration and live URLs after deployment is completed.

---

## Project Status

Current ShopAPI status:

    Core Backend Development       Complete
    PostgreSQL Integration         Complete
    Product API                    Complete
    User Authentication            Complete
    JWT Authentication             Complete
    Order API                      Complete
    Ownership Protection           Complete
    Product Permissions            Complete
    Automated Tests                26 Passing
    OpenAPI Schema                 Complete
    Swagger UI                     Complete
    JWT Swagger Authorization      Complete
    Professional README            Complete
    Project Screenshots            Complete
    Production Deployment          Next Stage

---

## What This Project Demonstrates

ShopAPI demonstrates practical Django REST Framework backend development beyond basic CRUD functionality.

The project demonstrates:

- REST API architecture
- Django REST Framework
- Relational database design
- PostgreSQL integration
- Django ORM
- Model relationships
- Serialization
- JSON request and response handling
- ViewSets
- Routers
- REST endpoints
- CRUD operations
- JWT authentication
- Access and refresh tokens
- Authentication and authorization
- Role-based permissions
- Ownership-based access control
- Secure user-specific data access
- Automated API testing
- Permission and ownership testing
- OpenAPI schema generation
- Interactive Swagger documentation
- Environment-based configuration
- Git and GitHub workflow
- Production-oriented backend architecture

The goal of ShopAPI is to demonstrate the complete path from relational database design to a secure, documented, tested, and production-oriented REST API.

---

## Live Application

Production deployment is the next project stage.

After deployment, this section will contain the real production URLs:

    Live Application:
    Live API:
    Swagger Documentation:
    OpenAPI Schema:

---

## About

ShopAPI is a backend-focused e-commerce REST API portfolio project built with Django REST Framework and PostgreSQL.

It was developed to demonstrate how a REST API is designed from database models through serializers, ViewSets, routers, JWT authentication, permissions, ownership rules, automated testing, OpenAPI documentation, and production deployment.