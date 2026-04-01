from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "atm-super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///atm.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pin_hash = db.Column(db.String(256), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'Deposit' or 'Withdrawal'
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- Auth Decorator ---
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# --- Routes ---
@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'user_id' in session else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pin = request.form['pin']
        action = request.form.get('action')

        if action == 'register':
            if User.query.filter_by(username=username).first():
                flash('Username already exists. Try logging in.', 'warning')
            else:
                user = User(username=username, pin_hash=generate_password_hash(pin))
                db.session.add(user)
                db.session.commit()
                flash('Account created! Please log in.', 'success')
                
        elif action == 'login':
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.pin_hash, pin):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            flash('Invalid username or PIN.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been securely fully logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        action = request.form.get('action')
        try:
            amount = float(request.form.get('amount', 0))
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Please enter a valid positive amount.", "danger")
            return redirect(url_for('dashboard'))

        if action == 'deposit':
            user.balance += amount
            tx = Transaction(user_id=user.id, type='Deposit', amount=amount)
            db.session.add(tx)
            db.session.commit()
            flash(f"Successfully deposited ${amount:.2f}", "success")
            
        elif action == 'withdraw':
            if user.balance >= amount:
                user.balance -= amount
                tx = Transaction(user_id=user.id, type='Withdrawal', amount=amount)
                db.session.add(tx)
                db.session.commit()
                flash(f"Successfully withdrew ${amount:.2f}", "success")
            else:
                flash("Insufficient funds for this withdrawal.", "danger")
                
        return redirect(url_for('dashboard'))

    transactions = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', user=user, transactions=transactions)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
