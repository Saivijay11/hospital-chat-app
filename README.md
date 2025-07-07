## Hospital Messaging System

A secure, HIPAA-conscious full-stack communication platform enabling real-time and asynchronous messaging between doctors and patients. Built using Django (Channels + DRF) for the backend and Next.js (React) for the frontend, this application supports role-based access, message delivery status, and audit readiness.

## Features

- **Role-Based Authentication** (Admin, Doctor, Patient)
- **Real-time & Asynchronous Messaging** (WebSockets via Django Channels)
- **Unread Message Tracking**
- **Secure JWT Authentication** (Username/Email login)
- **Role-based Dashboards**
- **Future-Ready: Token rotation, Audit Logging, Data Retention**

## Tech Stack

### Backend (Django + Channels)
- Django REST Framework
- Django Channels + Redis (for WebSocket)
- PostgreSQL (DB)
- Custom JWT Token Handling (with role claims)
- Celery (planned for async tasks)
- Redis (for channel layers and background queue)

### Frontend (Next.js + React)
- Next.js (App Router)
- Axios (JWT secured API calls)
- WebSocket Client for real-time messaging
- TailwindCSS (UI styling)

## 📂 Project Structure

### Backend
```
backend/
│
├── core/               # Main settings, routing
├── users/              # Auth logic, roles, tokens
├── chat/               # Messaging models, views, WebSocket handling
├── static/             # Static files
└── requirements.txt    # Dependencies
```

### Frontend
```
frontend/
├── app/                # App router structure
│   ├── login/          # Login page
│   ├── register/       # Registration page
│   ├── doctor/         # Doctor dashboard
│   ├── patient/        # Patient dashboard
│   ├── chat/           # Messaging page
├── components/         # Reusable UI (Header, ChatBox, Message)
├── hooks/              # Auth hook
└── styles/             # CSS files
```


## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Saivijay11/hospital-chat-app.git
cd hospital-chat-app
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

> Redis must be running for WebSocket and async tasks.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Authentication Flow

- User registers as a patient.
- Admin assigns role (Doctor/Admin).
- JWT token issued on login.
- Custom claims like `is_doctor`, `is_patient` included in token.
- Dashboards rendered based on role.
- All API routes are secured.

## Real-Time Chat Flow

1. WebSocket connects on `/ws/chat/<user_id>/`
2. Doctor sees list of patients; patients see list of doctors.
3. Messages sent over WebSocket and stored in DB.
4. Unread messages tracked; badge indicators shown.
5. Async messages delivered when receiver reconnects.

## Security & HIPAA Considerations

| Feature                    | Status   |
|----------------------------|----------|
| JWT-Based Role Auth        | Done  |
| Secure Socket Messaging    | Done  |
| Token Expiry & Rotation    | Planned |
| Audit Logging              | Planned |

## Future Enhancements

- Role approval notifications for Admins
- Message encryption (at-rest and in-transit)
- Audit log for sensitive operations
- Patient reports & file upload (PDF/Image)
- Doctor availability status indicator
- Celery + Redis integration for background tasks

## Documentation

[Confluence Project Documentation](https://saivijaywork1.atlassian.net/wiki/spaces/~7120200acc6dfec77f48e5bece4cf671707648/pages/98306/Hospital+Messaging+System)

