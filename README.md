# Hospital Chat App
A secure, full-stack hospital communication platform designed for real-time and asynchronous messaging between patients and doctors. Built with Django, Django Channels, and Next.js, this app ensures role-based access and HIPAA-conscious practices.

## Features
* Role-based login (Admin, Doctor, Patient)
* Secure JWT authentication (username or email)
* Real-time chat via WebSockets (Django Channels + Redis)
* Chat history and unread message indicators
* Admin, Doctor, and Patient dashboards
* Contact and Medicines pages for patients


## Backend Setup (Django)
1. Navigate to backend folder:
   cd backend
2. Create and activate virtual environment:
   python -m venv venv
   source venv/bin/activate
3. Install packages:
   pip install django djangorestframework djangorestframework-simplejwt channels redis
4. Start Redis (macOS/Homebrew):
   brew services start redis
5. Apply migrations and create superuser:
   python manage.py migrate
   python manage.py createsuperuser
6. Run with Daphne (WebSocket server):
   daphne core.asgi:application

## Frontend Setup (Next.js)

1. Navigate to frontend:
   cd frontend
2. Install packages:
   npm install
3. Run development server:
   npm run dev

Access: http://localhost:3000

## Authentication & Routing
* Login with username/email and password
* JWT stored in localStorage
* Role-based redirects:
  - /doctor
  - /patient
* Protected routes with automatic redirection on invalid access

## HIPAA-Conscious Highlights

| Feature                   | Status       |
|---------------------------|--------------|
| Secure JWT                | Implemented
| Role-based dashboard      | Implemented
| WebSocket messaging       | With Redis
| Token expiration handling | Planned
| Audit logs                | Planned
| Soft delete               | Planned
