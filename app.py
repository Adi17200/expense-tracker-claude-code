from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, seed_db, get_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")

        conn = get_db()
        existing_user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if existing_user:
            return render_template("register.html", error="Email already registered.")

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, hashed_pw)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template("login.html", error="Both email and password are required.")

        conn = get_db()
        user = conn.execute(
            "SELECT id, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("profile"))


        return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Hardcoded data for Step 4 UI validation
    user = {
        "name": "Adithya Kumar",
        "email": "adithya@example.com",
        "initials": "AK",
        "member_since": "October 2024"
    }

    stats = {
        "total_spent": "12,450",
        "count": 24,
        "top_category": "Food & Dining"
    }

    transactions = [
        {"date": "2024-10-20", "description": "Starbucks Coffee", "category": "Food", "amount": "450"},
        {"date": "2024-10-18", "description": "Uber Ride to Office", "category": "Transport", "amount": "320"},
        {"date": "2024-10-15", "description": "Amazon - Mechanical Keyboard", "category": "Shopping", "amount": "4,500"},
        {"date": "2024-10-12", "description": "Grocery Store", "category": "Food", "amount": "1,200"},
    ]

    categories = [
        {"name": "Food", "amount": "5,600", "percent": 45},
        {"name": "Transport", "amount": "3,200", "percent": 25},
        {"name": "Shopping", "amount": "3,650", "percent": 30},
    ]

    return render_template("profile.html", user=user, stats=stats, transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
