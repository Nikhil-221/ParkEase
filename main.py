import os
import razorpay
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

# ----------------------
# Flask App Setup
# ----------------------
app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parkease.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
razorpay_client = razorpay.Client(auth=("rzp_test_RKAX7zDSrQ7oQg", "fWZQpc2mDGz9KqhYV6i4LzEy"))

# Initialize DB + Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------
# Models
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def login_required(role=None):
    """Decorator to protect routes based on login and role."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if role and session.get('user_role') != role:
                return "Unauthorized", 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    slot_from = db.Column(db.Time, nullable=False)
    slot_till = db.Column(db.Time, nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    lender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booked = db.Column(db.Boolean, default=False)

    lender = db.relationship('User', backref='spots')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spot.id'), nullable=False)
    payment_id = db.Column(db.String(100), nullable=False)
    order_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    hours = db.Column(db.Integer, nullable=True)
    slot = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)
    reviewed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='bookings')
    spot = db.relationship('Spot', backref='bookings')

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20))  # 'user' or 'lender'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ----------------------
# Routes
# ----------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ----------------------
# Authentication
# ----------------------

@app.route('/signupas')
def signupas():
    return render_template('signupas.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        role = request.form.get('role')

        if password != confirm_password:
            return "Passwords do not match", 400

        if User.query.filter_by(email=email).first():
            return "Email already registered", 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            fullname=fullname,
            email=email,
            password=hashed_password,
            phone=phone,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['user_role'] = new_user.role

        return redirect(url_for('lenderdashboard' if role == 'lender' else 'userdashboard'))

    role = request.args.get('role')
    return render_template('signup.html', role=role)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            return redirect(url_for('lenderdashboard' if user.role == "lender" else 'userdashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ----------------------
# Static Pages
# ----------------------
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

# ----------------------
# Lender Pages
# ----------------------
@app.route('/lenderdashboard')
@login_required(role="lender")
def lenderdashboard():
    spots = Spot.query.filter_by(lender_id=session['user_id']).all()
    return render_template('lenderdashboard.html', spots=spots)

@app.route("/lenderaccount")
@login_required(role="lender")
def lenderaccount():
    lender = User.query.get(session["user_id"])
    return render_template("lenderaccount.html", lender=lender)



@app.route('/lendercontact', methods=['GET', 'POST'])
@login_required(role="lender")
def lendercontact():
    if request.method == 'POST':
        message = request.form.get('message')
        lender = User.query.get(session['user_id'])

        new_contact = Contact(
            name=lender.fullname,
            email=lender.email,
            message=message,
            role='lender'
        )
        db.session.add(new_contact)
        db.session.commit()

        return render_template('lendercontact.html', success=True)

    return render_template('lendercontact.html', success=False)


@app.route('/addspots', methods=['GET', 'POST'])
@login_required(role="lender")
def addspots():
    if request.method == 'POST':
        location = request.form['address']
        price = float(request.form['price'])
        description = request.form['vehicleType']
        slot_from = datetime.strptime(request.form['slotFrom'], '%H:%M').time()
        slot_till = datetime.strptime(request.form['slotTill'], '%H:%M').time()
        contact = request.form['contact']
        image = request.files.get('image')

        image_url = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = url_for('static', filename=f'uploads/{filename}')

        new_spot = Spot(
            location=location,
            price=price,
            description=description,
            slot_from=slot_from,
            slot_till=slot_till,
            contact=contact,
            image_url=image_url,
            lender_id=session['user_id']
        )
        db.session.add(new_spot)
        db.session.commit()
        return redirect(url_for('lenderdashboard'))
    return render_template('addspots.html')


@app.route('/bookings')
@login_required(role="lender")
def bookings():
    lender_id = session['user_id']
    bookings = Booking.query.join(Spot).filter(Spot.lender_id == lender_id).all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/reviews')
@login_required(role="lender")
def reviews():
    lender_id = session['user_id']
    # Fetch bookings where this lender’s spots have received reviews
    reviews = (
        Booking.query
        .join(Spot)
        .filter(Spot.lender_id == lender_id, Booking.reviewed == True)
        .all()
    )
    return render_template('reviews.html', reviews=reviews)


# ----------------------
# User Pages
# ----------------------
@app.route('/userdashboard')
@login_required(role="user")
def userdashboard():
    return render_template('userdashboard.html')

@app.route('/usercontact', methods=['GET', 'POST'])
@login_required(role="user")
def usercontact():
    if request.method == 'POST':
        message = request.form.get('message')
        user = User.query.get(session['user_id'])

        new_contact = Contact(
            name=user.fullname,
            email=user.email,
            message=message,
            role='user'
        )
        db.session.add(new_contact)
        db.session.commit()

        return render_template('usercontact.html', success=True)

    return render_template('usercontact.html', success=False)

@app.route('/useraccount')
@login_required(role="user")
def useraccount():
    user = User.query.get(session["user_id"])
    return render_template("useraccount.html", user=user)

@app.route('/pbs')
@login_required(role="user")
def pbs():
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template('pbs.html', bookings=bookings)

@app.route('/private')
@login_required(role="user")
def private():
    spots = Spot.query.all()
    return render_template('private.html', spots=spots)

@app.route('/public')
def public():
    return render_template('public.html')

@app.route('/bookaspot')
@login_required(role="user")
def bookaspot():
    return render_template('bookaspot.html')

@app.route('/payment/<int:spot_id>')
@login_required(role="user")
def payment(spot_id):
    hours = request.args.get("hours", 1, type=int)
    spot = Spot.query.get_or_404(spot_id)
    return render_template("payment.html", spot=spot, hours=hours)

# ----------------------
# Razorpay Integration
# ----------------------
@app.route("/create_order", methods=["POST"])
def create_order():
    data = request.get_json()
    amount = int(data["amount"]) * 100
    order = razorpay_client.order.create(dict(amount=amount, currency="INR", payment_capture="1"))
    return jsonify(order)

@app.route('/confirm_booking', methods=['POST'])
@login_required(role="user")
def confirm_booking():
    try:
        data = request.get_json()
        spot_id = data.get("spot_id")
        payment_id = data.get("payment_id")
        order_id = data.get("order_id")
        hours = data.get("hours", 1)

        spot = Spot.query.get(spot_id)
        if not spot:
            return jsonify({"success": False, "error": "Spot not found"}), 404

        # Mark spot as booked
        spot.booked = True

        slot_string = f"{spot.slot_from} - {spot.slot_till}"
        booking = Booking(
            user_id=session["user_id"],
            spot_id=spot_id,
            payment_id=payment_id,
            order_id=order_id,
            amount=spot.price,
            hours=int(hours),
            slot=slot_string
        )
        db.session.add(booking)
        db.session.commit()

        return jsonify({"success": True, "redirect_url": url_for('pbs')})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# ----------------------
# Submit Review Route
# ----------------------
@app.route("/submit_review", methods=["POST"])
@login_required(role="user")
def submit_review():
    data = request.get_json()
    booking_id = data.get("booking_id")
    rating = data.get("rating")
    review = data.get("review")

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"status": "error", "message": "Booking not found"})

    spot = Spot.query.get(booking.spot_id)
    if not spot:
        return jsonify({"status": "error", "message": "Spot not found"})

    booking.rating = rating
    booking.review = review
    booking.reviewed = True

    # Reopen spot
    spot.booked = False

    db.session.commit()
    return jsonify({"status": "success", "message": "Review submitted successfully"})

# ----------------------
# Run App
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
