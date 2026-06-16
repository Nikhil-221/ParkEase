#25AACR15
# ParkEase 

---

## Abstract

Parking availability is a persistent issue in urban areas, leading to wasted time, stress, and environmental pollution. Ironically, individuals and businesses often have unused land or parking spaces that could be monetized but lack a structured platform to do so. 

The system allows users to conveniently **search, view, and book available parking spots** in private areas such as houses or apartments, while lenders can **list and manage** their own spaces through a simple dashboard. Payments are handled securely using **Razorpay**, and users can provide feedback through the **review and rating system** after their booking.  

Our website aims to bridge this gap by providing a marketplace for renting parking spaces and vehicles, enhancing convenience for users and offering revenue opportunities for space owners.
At ParkEase, we believe in making parking Smarter, Simpler, and more Sustainable.

---

## Features

### User Side
- View and search available parking spots (filtered by location, price, and vehicle type)  
- Book spots directly via Razorpay payment gateway  
- View previously booked spots  
- Rate and review parking experiences  

### Lender Side
- Add new parking spaces with details, price, and images  
- Manage and monitor listed spaces through the lender dashboard  
- View bookings and relist previously rented spaces  

### General Features
- Responsive and modern UI (Black–Yellow–White theme)  
- Secure login/signup for users and lenders  
- Automatic booking status updates  
- Contact pages for issue reporting  
- SQLite database management with Flask-Migrate  
- Google Maps integration for future public parking discovery  

---

## Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python, Flask |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Payment Gateway** | Razorpay |
| **APIs Used** | Google Maps JavaScript API, Geolocation API, Geocoding API, Directions API, Places API |
| **Version Control** | GitHub |
| **Styling** | Black, Yellow, and White Theme (Modern UI/UX Design) |

---

## System Architecture

### Modules:
1. **User Module** – Handles user registration, login, parking spot browsing, and booking.  
2. **Lender Module** – Allows lenders to manage their listings and view active or previous bookings.  
3. **Payment Module** – Integrates Razorpay for secure and real-time transactions.  
4. **Database Module** – Manages users, spots, bookings, and reviews.  
5. **Contact Module** – Handles user/lender feedback submissions.  

---

## Project Structure

```

ParkEase/
│
├── instance/
│ └── parkease.db
│
├── migrations/
│ ├── versions/
│ ├── alembic.ini
│ └── env.py
│
├── static/
│ └── uploads/
│
├── templates/
│ ├── aboutus.html
│ ├── addspots.html
│ ├── bookings.html
│ ├── contact.html
│ ├── home.html
│ ├── lenderaccount.html
│ ├── lendercontact.html
│ ├── lenderdashboard.html
│ ├── login.html
│ ├── logout.html
│ ├── payment.html
│ ├── pbs.html
│ ├── privacypolicy.html
│ ├── private.html
│ ├── public.html
│ ├── reviews.html
│ ├── signup.html
│ ├── signupas.html
│ ├── terms.html
│ ├── useraccount.html
│ ├── usercontact.html
│ └── userdashboard.html
│
├── main.py
├── requirements.txt
└── README.md

````

---

## How to Run the Project

### 1) Clone the Repository
```bash
git clone https://github.com/<url>/ParkEase.git
cd ParkEase
````

### 2️) Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # For Windows
```

### 3️) Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️) Run Database Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5️) Run the Flask Application

```bash
flask run
```

### 6️) Access the App

```
http://127.0.0.1:5000/
```

---

### Team ID: 25AACR15 
**Team Members:**  
- Senior Mentor - Revanth  
- Junior Mentor - Zubair  
- Team Member 1 - Manasvini
- Team Member 2 - Nikhil 
- Team Member 3 - Rithisha  
- Team Member 4 - Pranav  
- Team Member 5 - Gowrish  

## Payment Gateway Integration

The application uses **Razorpay Test Mode** for secure and simulated payments.

```python
razorpay_client = razorpay.Client(auth=("rzp_test_xxxxx", "your_secret_key"))
```

---

## Future Improvements

* Add an **Admin Dashboard** to manage public parking spaces (malls, offices, etc.)
* Enable **vehicle rental features** for users who wish to lend or rent vehicles
* Introduce **real-time map-based parking spot tracking** using Google Maps
* Add **email/SMS notifications** for booking confirmations and reminders

---

## 🏁 Conclusion

**ParkEase** simplifies the entire parking experience for both lenders and users through a smart, intuitive, and efficient web-based platform.
It minimizes parking chaos, ensures better space utilization, and aims to create a sustainable and digital parking ecosystem.

---

### Developed by Team 25AACR15

```
```