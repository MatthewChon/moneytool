from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transaction.db"
db.init_app(app)

#------- End preconfiguration process -------#

class TransactionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    name = db.Column(db.String(99))
    category = db.Column(db.String(99))
    amount = db.Column(db.Float)

    def __init__(self, date, name, category, amount=0):
        self.date = date
        self.name = name
        self.category = category
        self.amount = amount

with app.app_context():
    db.create_all()

def retrieve_earnings():
    '''Retrieves earnings from the database
    
    Return:
        earnings (float: precision 2)
    '''
    earning_logs, earnings = db.session.query(TransactionModel).filter_by(category='EARNING').all(), 0
    for earning_log in earning_logs:
        earnings += earning_log.amount
    return float('%.2f'%earnings)

def retrieve_spendings():
    '''Retrieves spending from the database
    Return:
        spendings (float: precision 2)
    '''
    spending_logs, spendings = db.session.query(TransactionModel).filter(TransactionModel.category != 'EARNING').all(), 0
    for spending_log in spending_logs:
        spendings += spending_log.amount
    return float('%.2f'%spendings)

def compute_utilization_percentage(earnings, spendings):
    '''Computes the utilization percentage
    
    Keyword arguments:
        earnings -- current earnings
        spendings -- current spendings

    Return:
        utilization percentage (float: precision 3)
    '''
    earnings = max(1, earnings)
    return float('%.3f'%((spendings/earnings) * 100))

def base_render(html_page, **kwargs):
    '''Allows data and configs to share globally across pages

    Keyword arguments:
        html_page -- html page to be rendered
        kwargs -- individual data to be sent
    '''
    header_data = {
        'earnings': retrieve_earnings(),
        'spendings': retrieve_spendings(),
        'utilization_threshold': 30
    }
    header_data['delta'] = header_data['earnings'] - header_data['spendings']
    header_data['utilization'] = compute_utilization_percentage(header_data['earnings'], header_data['spendings'])
    return render_template(html_page, header_data=header_data, **kwargs)

#======= Page Configurations =======#
@app.route("/")
def index():
    return base_render('index.html')

@app.route("/transaction_history")
def load_transaction_log():
    transaction_history = db.session.query(TransactionModel).all()
    return base_render("transaction.html", transaction_logs=transaction_history)

@app.route("/new_transaction")
def load_new_transaction_page():
    return base_render("spendingsform.html")

@app.route("/handle_transaction", methods=['POST'])
def handle_new_transaction_request():
    model_schema = ['date', 'name', 'category', 'amount']
    transaction_form = request.form
    transaction_record = TransactionModel(transaction_form.get('transaction_date'),
                                          transaction_form.get('transaction_name'),
                                          transaction_form.get('transaction_category'),
                                          transaction_form.get('transaction_amount'))
    db.session.add(transaction_record)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/new_earnings")
def load_new_earnings_page():
    return base_render("earningsform.html")

@app.route("/clear")
def clear():
    db.session.query(TransactionModel).delete()
    db.session.commit()
    return redirect(url_for('index'))
#------- End of Page Configuration -------#