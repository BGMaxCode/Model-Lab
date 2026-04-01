"""
==============================================================
  Ticket Management Registration System — Flask Backend
  -----------------------------------------------
  PLACEHOLDERS (replace before use):
    Ticket Management          → e.g. "EventHub", "TicketMaster Pro"
    Ticket        → singular label, e.g. "Registration", "Ticket"
    Tickets       → plural label,   e.g. "Registrations", "Tickets"
    [CATEGORY_OPTIONS]  → list of category strings (see model below)
    [STATUS_OPTIONS]    → list of status strings (see model below)
    [DB_URI]            → e.g. "sqlite:///app.db" or keep in-memory default
==============================================================
"""

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

# ──────────────────────────────────────────────
# App & Database Configuration
# ──────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-before-production")

# [DB_URI] — swap to a real DB URI in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticket_management.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ──────────────────────────────────────────────
# Placeholder constants — customise these
# ──────────────────────────────────────────────
CATEGORY_OPTIONS = [
    "Bug Report",   # e.g. "General Admission", "VIP", "Early Bird"
    "Feature Request",
    "General Inquiry",
    "Other",
]

STATUS_OPTIONS = [
    "Active",         # e.g. "Confirmed", "Pending", "Cancelled"
    "Inactive",
]

# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password_h = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items      = db.relationship("Ticket", backref="owner", lazy=True)

    def set_password(self, pw):
        self.password_h = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_h, pw)


class Ticket(db.Model):
    """
    Core registration/item entity.
    Rename this class and its tablename to match your domain,
    e.g. Registration, Ticket, Enrollment, Booking …
    """
    __tablename__ = "tickets"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)   # Ticket title / name
    email       = db.Column(db.String(120), nullable=False)   # contact email
    category    = db.Column(db.String(80),  nullable=False)   # one of CATEGORY_OPTIONS
    description = db.Column(db.Text)
    status      = db.Column(db.String(40),  default="Active") # one of STATUS_OPTIONS
    created_at  = db.Column(db.DateTime,    default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Optional: add domain-specific fields below
    # [EXTRA_FIELD_1] = db.Column(db.String(120))   # e.g. event_date, seat_number


# ──────────────────────────────────────────────
# Auth helpers
# ──────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def current_user():
    return User.query.get(session.get("user_id"))

# ──────────────────────────────────────────────
# Auth routes
# ──────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        pw    = request.form.get("password", "")
        pw2   = request.form.get("confirm_password", "")

        if not all([name, email, pw]):
            flash("All fields are required.", "danger")
        elif pw != pw2:
            flash("Passwords do not match.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
        else:
            user = User(name=name, email=email)
            user.set_password(pw)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pw    = request.form.get("password", "")
        user  = User.query.filter_by(email=email).first()
        if user and user.check_password(pw):
            session["user_id"] = user.id
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("auth.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ──────────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    all_items   = Ticket.query.filter_by(user_id=user.id).all()
    active_cnt  = sum(1 for i in all_items if i.status == "Active")
    inactive_cnt = len(all_items) - active_cnt
    recent_items = Ticket.query.filter_by(user_id=user.id)\
                               .order_by(Ticket.created_at.desc())\
                               .limit(10).all()
    return render_template(
        "dashboard.html",
        user=user,
        total=len(all_items),
        active=active_cnt,
        inactive=inactive_cnt,
        recent_items=recent_items,
        item_label="Ticket",
        items_label="Tickets",
    )

# ──────────────────────────────────────────────
# Tickets CRUD
# ──────────────────────────────────────────────
@app.route("/items", methods=["GET"])
@login_required
def list_items():
    user   = current_user()
    search = request.args.get("q", "").strip()
    page   = request.args.get("page", 1, type=int)
    query  = Ticket.query.filter_by(user_id=user.id)
    if search:
        query = query.filter(Ticket.name.ilike(f"%{search}%"))
    items = query.order_by(Ticket.created_at.desc()).paginate(page=page, per_page=10)
    return render_template("items.html", items=items, search=search,
                           item_label="Ticket", items_label="Tickets")


@app.route("/items/new", methods=["GET"])
@login_required
def new_item():
    return render_template("form.html", item=None,
                           categories=CATEGORY_OPTIONS,
                           statuses=STATUS_OPTIONS,
                           item_label="Ticket")


@app.route("/items", methods=["POST"])
@login_required
def create_item():
    user = current_user()
    item = Ticket(
        name        = request.form["name"],
        email       = request.form["email"],
        category    = request.form["category"],
        description = request.form.get("description", ""),
        status      = request.form.get("status", "Active"),
        user_id     = user.id,
    )
    db.session.add(item)
    db.session.commit()
    flash("Ticket created successfully.", "success")
    return redirect(url_for("list_items"))


@app.route("/items/<int:item_id>", methods=["GET"])
@login_required
def show_item(item_id):
    item = Ticket.query.get_or_404(item_id)
    return render_template("form.html", item=item,
                           categories=CATEGORY_OPTIONS,
                           statuses=STATUS_OPTIONS,
                           item_label="Ticket",
                           readonly=True)


@app.route("/items/<int:item_id>", methods=["POST"])
@login_required
def update_item(item_id):
    item = Ticket.query.get_or_404(item_id)
    item.name        = request.form["name"]
    item.email       = request.form["email"]
    item.category    = request.form["category"]
    item.description = request.form.get("description", "")
    item.status      = request.form.get("status", item.status)
    db.session.commit()
    flash("Ticket updated.", "success")
    return redirect(url_for("list_items"))


@app.route("/items/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    item = Ticket.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Ticket deleted.", "info")
    return redirect(url_for("list_items"))

# ──────────────────────────────────────────────
# Error handlers
# ──────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("base.html", error_title="404", error_msg="Page not found."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("base.html", error_title="500", error_msg="Internal server error."), 500

# ──────────────────────────────────────────────
# Bootstrap DB and run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
