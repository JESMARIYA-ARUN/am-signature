# A&M Signature 
### Wear Your Story

A&M Signature is a full-stack **Django eCommerce web application** designed for a fashion brand.  
The platform allows users to browse products, select sizes where applicable, manage cart and wishlist, and place orders.  
It includes stock management, admin notifications, and customer confirmation emails.

---

## Features

### User Features
- User registration and login
- Secure password validation
- Browse product collection
- Product detail view
- Size selection (XS–XXL) for applicable products
- Add to cart with live quantity updates
- Wishlist management
- Move items from wishlist to cart
- Place orders (Cash on Delivery)
- Order confirmation email to customer

### Admin Features
- Django Admin dashboard
- Product management
- Size and stock management
- Order management
- Email notification on every new order

---

## Product Handling
- **Products with sizes**
  - XS, S, M, L, XL, XXL
  - Stock-based availability
  - Out-of-stock sizes disabled
- **Products without sizes**
  - Example: Sarees
  - Can be added directly to cart

---

## Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Django |
| Frontend | HTML, CSS, Bootstrap |
| Database | PostgreSQL |
| Authentication | Django Auth |
| Emails | Brevo (SendinBlue) SMTP |
| Static Files | WhiteNoise |
| Deployment | Render |
| Version Control | Git & GitHub |

---

## Project Structure

am_signature/
│
├── accounts/ # User authentication
├── products/ # Products & wishlist
├── orders/ # Cart & order logic
├── templates/ # HTML templates
├── static/ # CSS, JS, images
├── media/ # Uploaded product images
├── am_signature/ # Project settings
├── manage.py
├── requirements.txt
└── README.md


---

##  Local Setup

Clone the Repository
git clone https://github.com/YOUR_USERNAME/am-signature.git
cd am-signature
Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate

Mac / Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt


Environment Variables
Create a .env file in the project root:
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=am_signature_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_brevo_smtp_login
EMAIL_HOST_PASSWORD=your_brevo_smtp_key
DEFAULT_FROM_EMAIL=A&M Signature <no-reply@example.com>

ADMIN_NOTIFICATION_EMAILS=admin@example.com

Do NOT commit .env to GitHub.


Database Setup
python manage.py makemigrations
python manage.py migrate

Create admin user:
python manage.py createsuperuser

Run the Application
python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

Admin panel:
http://127.0.0.1:8000/admin/


Static Files
python manage.py collectstatic
Static files are served using WhiteNoise in production.

Email System
Admin receives email when a new order is placed
Customer receives order confirmation email
HTML + plain text fallback
Powered by Brevo SMTP


Tested Areas
User authentication
Product display
Size validation
Cart logic
Wishlist
Order placement
Stock reduction
Email notifications


Deployment (Render)
Deployment Steps

Push project to GitHub (without secrets)

Create a Web Service on Render

Create a PostgreSQL database on Render

Add environment variables in Render dashboard

Build Command:
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate


Start Command:
gunicorn am_signature.wsgi:application

Security
Environment variables for secrets
Django password hashing
Atomic database transactions
CSRF protection enabled


Future Enhancements

Online payment gateway
Order tracking
Product search & filters
Admin analytics dashboard
User profile management



Author
Jesmariya Arun
Final Project – Full Stack Development
A&M Signature — Wear Your Story

