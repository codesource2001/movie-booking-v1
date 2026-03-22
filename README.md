# Movie Booking API

[![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-green)](http://127.0.0.1:8000/api/docs/)
[![Redoc](https://img.shields.io/badge/Redoc-OpenAPI-blue)](http://127.0.0.1:8000/api/redoc/)

Complete RESTful API for a **Movie Ticket Booking System** built with Django REST Framework. Supports full lifecycle from user registration to payment and notifications.

## 🚀 Features

- **User Management**: JWT authentication with roles (Customer, Admin, Theatre Owner, Staff)
- **Movie Catalog**: CRUD for movies with genres, posters, trailers
- **Theatre Management**: Theatres & screens with JSON seat layouts & facilities
- **Show Scheduling**: Link movies to screens with pricing & availability
- **Seat Booking**: JSON seat selection, status tracking (pending/confirmed/etc.)
- **Payment Processing**: Multiple methods (card/UPI/etc.), transaction tracking
- **Notifications**: User-specific alerts for bookings/payments/shows
- **Admin Panel**: Full Django Admin
- **API Documentation**: Auto-generated Swagger UI & ReDoc

## 🛠 Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Auth**: JWT (SimpleJWT)
- **Docs**: drf-spectacular (OpenAPI 3)
- **DB**: SQLite (dev), easy PostgreSQL migration
- **Architecture**: Repository/Service pattern per app
- **Media**: ImageField for posters

## 📁 Project Structure

```
Movie-booking/
├── manage.py
├── mba_main/          # Main project settings
├── booking/           # Bookings & seats
├── core/              # Shared repositories
├── movie/             # Movies catalog
├── notification/      # User notifications
├── payment/           # Payments
├── show/              # Show schedules
├── theatre/           # Theatres & screens
└── user/              # Custom users & auth
```

Each app follows: `models.py` → `serializers.py` → `services.py` → `repositories.py` → `views.py`.

## 🗄 Database Models Overview

### User (user/models.py)
| Field | Type | Description |
|-------|------|-------------|
| role | CharField | customer/admin/theatre_owner/staff |
| phone, address, date_of_birth | Optional | Profile info |

*Extends AbstractUser, AUTH_USER_MODEL='user.User'*

### Movie (movie/models.py)
| Field | Type | Description |
|-------|------|-------------|
| title, description, duration, release_date | Required | Movie details |
| genre | Choice | action/comedy/etc. |
| poster | ImageField | /movies/posters/ |

### Theatre & Screen (theatre/models.py)
- **Theatre**: name, owner (User), location, seats_layout (JSON), facilities (JSON)
- **Screen**: theatre FK, name, type (standard/3d/imax/4dx), seats_layout (JSON)

### Show (show/models.py)
| Field | Type | Description |
|-------|------|-------------|
| movie FK, screen FK | Required | Links entities |
| start_time, end_time, price | Required | Schedule & pricing |
| status | Choice | scheduled/running/etc. |

### Booking (booking/models.py)
| Field | Type | Description |
|-------|------|-------------|
| user FK, show FK | Required | Who & what |
| seats | JSONField | ['A1', 'A2'] list |
| total_price, status | Decimal/Char | pending/confirmed/etc. |

### Payment (payment/models.py)
- Links to Booking, method (card/upi/etc.), status (completed/failed), transaction_id

### Notification (notification/models.py)
- user FK, title/message, type (booking/etc.), related_id

## 🔌 API Endpoints

Base: `http://127.0.0.1:8000/api/`

| Tag | Prefix | Operations |
|-----|--------|------------|
| Authentication | `/auth/` | login/register/refresh/profile |
| Movies | `/movies/` | List/Create/Retrieve/Update/Delete |
| Theatres | `/theatres/` | CRUD Theatres/Screens |
| Shows | `/shows/` | Schedule shows, check availability |
| Bookings | `/bookings/` | Create/select seats, status update |
| Payments | `/payments/` | Process payments |
| Notifications | `/notifications/` | List/mark read |

**Interactive Docs:**
- [Swagger UI](http://127.0.0.1:8000/api/docs/)
- [ReDoc](http://127.0.0.1:8000/api/redoc/)
- Schema: `/api/schema/`

Example (auth): `POST /api/auth/login/` → `{"username":"...", "password":"..."}` → JWT tokens.

## 🚀 Quick Start

1. **Clone/Setup**
   ```bash
   cd Movie-booking
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   pip install django djangorestframework rest-framework-simplejwt drf-spectacular pillow
   ```

2. **Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```
   → Visit [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)

5. **Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🧪 Testing

```bash
pip install pytest pytest-django
pytest
```

Tests in `app/tests.py`.

## 🔒 Permissions & Auth

- JWT required for most endpoints.
- Role-based: theatre_owner manages own theatres, admin full access.
- Custom permissions in `user/permissions.py`.

## 📊 Production Deployment

- PostgreSQL: Update `DATABASES` in `settings.py`.
- Static/Media: `python manage.py collectstatic`.
- Gunicorn + Nginx/Apache.
- Env vars for SECRET_KEY, etc.

## 🤝 Contributing

1. Fork & PR.
2. Follow PEP8, add tests.
3. Update docs.

## 📄 License

MIT

---

*Built with ❤️ for movie lovers!*

