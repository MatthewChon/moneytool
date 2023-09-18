from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_transaction")
def load_transaction_page():
    return render_template("submission.html")

@app.route("/new_earnings")
def load_earnings_page():
    return render_template("earnings.html")