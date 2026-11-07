from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, seed_db, get_db
from database.queries import get_summary_stats, get_recent_transactions, get_category_breakdown, get_user_by_id, get_expense_by_id, update_expense, insert_expense, delete_expense
from datetime import datetime, timedelta


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

    user_id = session["user_id"]

    # Date filter handling
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    if date_from and date_to:
        try:
            datetime.strptime(date_from, "%Y-%m-%d")
            datetime.strptime(date_to, "%Y-%m-%d")
            if date_from > date_to:
                flash("Start date must be before end date.")
                date_from, date_to = None, None
        except ValueError:
            date_from, date_to = None, None

    # Fetch real user data
    user = get_user_by_id(user_id)
    if not user:
        return redirect(url_for("login"))

    stats = get_summary_stats(user_id, date_from, date_to)
    transactions = get_recent_transactions(user_id, date_from=date_from, date_to=date_to)
    categories = get_category_breakdown(user_id, date_from, date_to)

    # Compute preset dates for the template
    today = datetime.now().date()
    first_of_month = today.replace(day=1).strftime("%Y-%m-%d")
    this_month_from = first_of_month
    this_month_to = today.strftime("%Y-%m-%d")

    last_3m_from = (today - timedelta(days=90)).strftime("%Y-%m-%d")
    last_3m_to = today.strftime("%Y-%m-%d")

    last_6m_from = (today - timedelta(days=180)).strftime("%Y-%m-%d")
    last_6m_to = today.strftime("%Y-%m-%d")

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
        date_from=date_from,
        date_to=date_to,
        presets={
            "this_month": (this_month_from, this_month_to),
            "last_3m": (last_3m_from, last_3m_to),
            "last_6m": (last_6m_from, last_6m_to),
        }
    )


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        amount_str = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description", "").strip() or None

        error = None
        try:
            if not amount_str or float(amount_str) <= 0:
                raise ValueError("Amount must be a positive number.")
            amount = float(amount_str)
        except ValueError as e:
            error = str(e) if "positive number" in str(e) else "Invalid amount."

        if not category:
            error = "Category is required."

        if not date:
            error = "Date is required."
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format."

        if error:
            return render_template("add_expense.html", error=error,
                                   amount=amount_str, category=category, date=date, description=description)

        insert_expense(user_id, amount, category, date, description)
        flash("Expense added successfully!")
        return redirect(url_for("profile"))

    # GET handler
    categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("add_expense.html", categories=categories, today=today)



@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        amount_str = request.form.get("amount")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description", "").strip() or None

        error = None
        try:
            if not amount_str or float(amount_str) <= 0:
                raise ValueError("Amount must be a positive number.")
            amount = float(amount_str)
        except ValueError as e:
            error = str(e) if "positive number" in str(e) else "Invalid amount."

        if not category:
            error = "Category is required."

        if not date:
            error = "Date is required."
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format."

        if error:
            expense = get_expense_by_id(id, user_id)
            if not expense:
                return "Expense not found", 404
            return render_template("edit_expense.html", expense=expense, error=error,
                                   amount=amount_str, category=category, date=date, description=description)

        rows_affected = update_expense(id, user_id, amount, category, date, description)
        if rows_affected == 0:
            return "Expense not found or not owned", 404

        flash("Expense updated successfully!")
        return redirect(url_for("profile"))

    # GET handler
    expense = get_expense_by_id(id, user_id)
    if not expense:
        return "Expense not found", 404

    categories = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]
    return render_template("edit_expense.html", expense=expense, categories=categories)



@app.route("/expenses/<int:id>/delete", methods=["POST"])
def delete_expense_route(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Verify ownership and existence
    expense = get_expense_by_id(id, user_id)
    if not expense:
        return "Expense not found or not owned", 404

    delete_expense(id, user_id)
    flash("Expense deleted successfully!")
    return redirect(url_for("profile"))


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
