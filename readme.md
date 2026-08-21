# DexShop - E-Commerce & Data Management System

## Project Description
DexShop is a dynamic, full-stack web application developed using Python and the Flask micro-framework. Originally conceived as a static web project, it has been expanded into a fully functional e-commerce platform to demonstrate proficiency in backend integration, session management, and dynamic data rendering.

The application simulates a computer hardware store, allowing users to browse products, view detailed specifications, and simulate purchase orders via a responsive interface. It includes a restricted administration area for data management.

## Technical Architecture

### Backend
- **Language:** Python 3
- **Framework:** Flask
- **Security:** Werkzeug (for password hashing), Flask-Session (for state management)
- **Data Storage:** JSON-based persistence layer (simulating a NoSQL database structure)

### Frontend
- **Templating Engine:** Jinja2 (Server-side rendering)
- **Styling:** Custom CSS3 (Dark Mode Theme, Responsive Grid Layout)
- **Interactivity:** Vanilla JavaScript (DOM manipulation for Sidebar Checkout, Sticky Navbar, Scroll Reveal)

## Key Features

### Public User Interface
1.  **Dynamic Catalogue:** Renders products from the JSON database with server-side pagination logic.
2.  **Product Details:** Dedicated page for each item displaying technical specifications and related products.
3.  **Interactive Shopping:** A JavaScript-powered sidebar checkout system that validates user login status before order submission.
4.  **Responsive Design:** Optimized layout for desktop and mobile devices.

### Administration & Security
1.  **Authentication System:** Secure Login and Registration system using hashed passwords.
2.  **Route Protection:** Implementation of custom Python decorators (`@login_required`) to restrict access to administrative routes.
3.  **Admin Dashboard:** A protected interface for managing store operations (structure ready for CRUD expansion).

## Installation and Setup

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Access the application:**
    Open a web browser and navigate to: http://127.0.0.1:5000/

## Deployment

The application is configured for deployment on PaaS platforms like Render. It includes:
- `Procfile` for Gunicorn configuration.
- Environment variable support for sensitive data (SECRET_KEY).

**Note on Persistence:** Due to the ephemeral file system of free hosting tiers (like Render), changes made to the JSON data files (e.g., new user registrations) may reset after server restarts. For a production environment, a migration to a persistent database (MongoDB/PostgreSQL) is recommended.

## Access Credentials (For Testing)

To access the protected Dashboard and test the checkout restrictions, use the following Administrator account:

- **Email:** mohamed.cyber@hotmail
- **Password:** default_password

---

**Author:** Mohamed Jaa
**Institution:** Faculté des Sciences Semlalia (FSSM) - Marrakech
**Department:** Computer Science