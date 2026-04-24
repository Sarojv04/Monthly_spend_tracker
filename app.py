from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email, create_user, get_user_by_id

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("landing"))
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        error = "All fields are required."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif get_user_by_email(email):
        error = "An account with that email already exists."
    else:
        error = None

    if error:
        return render_template("register.html", error=error)

    create_user(name, email, generate_password_hash(password))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("landing"))
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email:
        return render_template("login.html", error="Email is required.")
    if not password:
        return render_template("login.html", error="Password is required.")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Nitish Kumar",
        "email": "nitish@example.com",
        "member_since": "January 2026",
        "initials": "NK",
    }
    stats = {
        "total_spent": "393.24",
        "transaction_count": 8,
        "top_category": "Food",
    }
    transactions = [
        {"date": "2026-04-20", "description": "Restaurant dinner",       "category": "Food",          "amount": "55.75"},
        {"date": "2026-04-14", "description": "New shoes",               "category": "Shopping",      "amount": "89.99"},
        {"date": "2026-04-10", "description": "Streaming subscriptions", "category": "Entertainment", "amount": "25.00"},
        {"date": "2026-04-08", "description": "Pharmacy",                "category": "Health",        "amount": "35.00"},
        {"date": "2026-04-05", "description": "Electricity bill",        "category": "Bills",         "amount": "120.00"},
    ]
    categories = [
        {"name": "Bills",         "total": "120.00", "pct": 30},
        {"name": "Food",          "total": "98.25",  "pct": 25},
        {"name": "Shopping",      "total": "89.99",  "pct": 23},
        {"name": "Health",        "total": "35.00",  "pct": 9},
        {"name": "Entertainment", "total": "25.00",  "pct": 6},
        {"name": "Transport",     "total": "15.00",  "pct": 4},
        {"name": "Other",         "total": "10.00",  "pct": 3},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
