import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

db_user = os.getenv("MYSQL_USER", "bankuser")
db_pass = os.getenv("MYSQL_PASSWORD", "bankpass")
db_host = os.getenv("DB_HOST", "db")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("MYSQL_DATABASE", "bankdb")

# Database setup (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Account(db.Model):
    account_id = db.Column(db.String(50), primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.account_id'), nullable=False)
    type = db.Column(db.String(20))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route("/")
def index():
    accounts = Account.query.all()
    return render_template("index.html", accounts=accounts)

@app.route("/create", methods=["POST"])
def create_account():
    account_id = request.form["account_id"]
    if Account.query.get(account_id):
        flash("Account already exists!", "danger")
    else:
        db.session.add(Account(account_id=account_id, balance=0.0))
        db.session.commit()
        flash(f"Account {account_id} created successfully!", "success")
    return redirect(url_for("index"))

@app.route("/deposit/<account_id>", methods=["POST"])
def deposit(account_id):
    amount = float(request.form["amount"])
    acc = Account.query.get(account_id)
    if acc:
        acc.balance += amount
        db.session.add(Transaction(account_id=account_id, type="deposit", amount=amount))
        db.session.commit()
        flash(f"Deposited {amount} to {account_id}", "success")
    else:
        flash("Account not found!", "danger")
    return redirect(url_for("index"))

@app.route("/withdraw/<account_id>", methods=["POST"])
def withdraw(account_id):
    amount = float(request.form["amount"])
    acc = Account.query.get(account_id)
    if acc:
        if acc.balance < amount:
            flash("Insufficient funds!", "danger")
        else:
            acc.balance -= amount
            db.session.add(Transaction(account_id=account_id, type="withdraw", amount=amount))
            db.session.commit()
            flash(f"Withdrew {amount} from {account_id}", "success")
    else:
        flash("Account not found!", "danger")
    return redirect(url_for("index"))

@app.route("/transfer", methods=["POST"])
def transfer():
    from_id = request.form["from_id"]
    to_id = request.form["to_id"]
    amount = float(request.form["amount"])
    from_acc, to_acc = Account.query.get(from_id), Account.query.get(to_id)
    if not from_acc or not to_acc:
        flash("One or both accounts not found!", "danger")
    elif from_acc.balance < amount:
        flash("Insufficient funds for transfer!", "danger")
    else:
        from_acc.balance -= amount
        to_acc.balance += amount
        db.session.add(Transaction(account_id=from_id, type="transfer_out", amount=amount))
        db.session.add(Transaction(account_id=to_id, type="transfer_in", amount=amount))
        db.session.commit()
        flash(f"Transferred {amount} from {from_id} to {to_id}", "success")
    return redirect(url_for("index"))

@app.route("/history/<account_id>")
def history(account_id):
    acc = Account.query.get(account_id)
    if not acc:
        flash("Account not found!", "danger")
        return redirect(url_for("index"))
    return render_template("history.html", account=acc, transactions=acc.transactions)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

