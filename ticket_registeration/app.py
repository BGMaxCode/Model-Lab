from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    failed_attempts = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Generic (Train, Movie, Event, etc.)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50))
    venue = db.Column(db.String(100))
    price = db.Column(db.String(50))
    description = db.Column(db.Text)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def init_db():
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin')
            admin = User(username='admin', password=hashed_pw, is_admin=True)
            db.session.add(admin)
            db.session.commit()

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return redirect(url_for('admin')) if user.is_admin else redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.is_locked:
                flash('Account locked due to multiple failed attempts. Contact Admin.', 'danger')
            elif check_password_hash(user.password, request.form['password']):
                user.failed_attempts = 0
                db.session.commit()
                session['user_id'] = user.id
                return redirect(url_for('index'))
            else:
                user.failed_attempts += 1
                if user.failed_attempts >= 3 and not user.is_admin:
                    user.is_locked = True
                db.session.commit()
                flash(f'Invalid credentials. Attempt {user.failed_attempts}/3', 'danger')
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
        else:
            new_user = User(username=username, password=generate_password_hash(request.form['password']))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/user')
def user_dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user or user.is_admin: return redirect(url_for('login'))
    
    tickets = Ticket.query.all()
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('user.html', tickets=tickets, messages=messages, user=user)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_id' not in session: return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin: return redirect(url_for('login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_ticket':
            db.session.add(Ticket(
                title=request.form['title'], 
                category=request.form['category'], 
                date=request.form['date'],
                time=request.form.get('time'),
                venue=request.form.get('venue'),
                price=request.form.get('price'),
                description=request.form.get('description')
            ))
        elif action == 'message':
            db.session.add(Message(content=request.form['content']))
        db.session.commit()
        return redirect(url_for('admin'))
        
    users = User.query.filter_by(is_admin=False).all()
    tickets = Ticket.query.all()
    return render_template('admin.html', users=users, tickets=tickets)

@app.route('/unlock/<int:id>')
def unlock(id):
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_admin:
            u = User.query.get(id)
            if u:
                u.is_locked = False
                u.failed_attempts = 0
                db.session.commit()
                flash(f'Unlocked user {u.username}', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8888)
