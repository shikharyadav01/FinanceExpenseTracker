import csv
import io

from flask import Flask, flash, redirect, render_template, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-change-me"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=dt.date.today)
    

with app.app_context():
    db.create_all()

CATEGORIES = ["Food", "Transport", "Rent", "Utilities","Others"]



def parse_date_or_none(s: str) -> dt.date | None:
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None
    except TypeError:
        return None


def filtered_expense_query(start_date, end_date, filter_category):
    q = Expense.query
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    if filter_category:
        q = q.filter(Expense.category == filter_category)
    return q


@app.route("/")
def home():
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    filter_category = (request.args.get("category") or "").strip()

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    if start_date and end_date and start_date > end_date:
        flash("Start date must be before end date.", "error")
        start_date = end_date = None

    q = filtered_expense_query(start_date, end_date, filter_category)

    # Totals by category for charts (same filters as the expense list).
    agg_q = db.session.query(Expense.category, func.sum(Expense.amount))
    if start_date:
        agg_q = agg_q.filter(Expense.date >= start_date)
    if end_date:
        agg_q = agg_q.filter(Expense.date <= end_date)
    if filter_category:
        agg_q = agg_q.filter(Expense.category == filter_category)
    agg_rows = agg_q.group_by(Expense.category).order_by(Expense.category).all()
    cat_labels = [row[0] for row in agg_rows]
    cat_values = [round(float(row[1] or 0), 2) for row in agg_rows]

    day_q = db.session.query(Expense.date, func.sum(Expense.amount))
    if start_date:
        day_q = day_q.filter(Expense.date >= start_date)
    if end_date:
        day_q = day_q.filter(Expense.date <= end_date)
    if filter_category:
        day_q = day_q.filter(Expense.category == filter_category)
    day_rows = day_q.group_by(Expense.date).order_by(Expense.date).all()
    day_labels = [row[0].isoformat() for row in day_rows]
    day_values = [round(float(row[1] or 0), 2) for row in day_rows]




    expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=CATEGORIES,
        start_str=start_str,
        end_str=end_str,
        filter_category=filter_category,
        cat_labels=cat_labels,
        cat_values=cat_values,
        day_labels=day_labels,
        day_values=day_values,
    )



@app.route("/add", methods=["POST"])
def add():
    description = (request.form.get("description") or "").strip()
    amount_raw = request.form.get("amount")
    category = (request.form.get("category") or "").strip()
    date_raw = request.form.get("date")

    if not description or not amount_raw or not category:
        flash("Please fill description, amount, and category.", "error")
        return redirect(url_for("home"))

    try:
        amount = float(amount_raw)
    except (TypeError, ValueError):
        flash("Invalid amount.", "error")
        return redirect(url_for("home"))

    if date_raw:
        try:
            expense_date = dt.date.fromisoformat(date_raw)
        except ValueError:
            expense_date = dt.date.today()
    else:
        expense_date = dt.date.today()

    db.session.add(
        Expense(
            description=description,
            amount=amount,
            category=category,
            date=expense_date,
        )
    )
    db.session.commit()
    flash("Expense added.", "success")
    return redirect(url_for("home"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted.", "success")
    return redirect(url_for("home"))




@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == "POST":
        description = (request.form.get("description") or "").strip()
        amount_raw = request.form.get("amount")
        category = (request.form.get("category") or "").strip()
        date_raw = (request.form.get("date") or "").strip()

        if not description or not amount_raw or not category:
            flash("Please fill description, amount, and category.", "error")
            return redirect(url_for("edit", expense_id=expense_id))

        if category not in CATEGORIES:
            flash("Invalid category.", "error")
            return redirect(url_for("edit", expense_id=expense_id))

        try:
            amount = float(amount_raw)
        except (TypeError, ValueError):
            flash("Invalid amount.", "error")
            return redirect(url_for("edit", expense_id=expense_id))

        if date_raw:
            try:
                expense_date = dt.date.fromisoformat(date_raw)
            except ValueError:
                expense_date = dt.date.today()
        else:
            expense_date = dt.date.today()

        expense.description = description
        expense.amount = amount
        expense.category = category
        expense.date = expense_date
        db.session.commit()

        flash("Expense updated.", "success")
        return redirect(url_for("home"))

    return render_template("edit.html", expense=expense, categories=CATEGORIES)


@app.route("/download_csv", methods=["GET"])
def download_csv():
    start_str = (request.args.get("start") or "").strip()
    end_str = (request.args.get("end") or "").strip()
    filter_category = (request.args.get("category") or "").strip()

    start_date = parse_date_or_none(start_str)
    end_date = parse_date_or_none(end_str)

    if start_date and end_date and start_date > end_date:
        flash("Start date must be before end date.", "error")
        return redirect(url_for("home"))

    expenses = (
        filtered_expense_query(start_date, end_date, filter_category)
        .order_by(Expense.date.desc(), Expense.id.desc())
        .all()
    )

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["date", "description", "category", "amount"])
    for e in expenses:
        # Excel shows ##### for date serials when the column is narrow; ="…" forces visible text.
        excel_date = f'="{e.date.isoformat()}"'
        writer.writerow(
            [excel_date, e.description, e.category, f"{e.amount:.2f}"]
        )

    return Response(
        "\ufeff" + buf.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="expenses.csv"',
        },
    )



if __name__=="__main__":
    app.run(debug = True)
