from flask import Flask, render_template

app = Flask(__name__)

def retrieve_earnings():
    return 0

def retrieve_spendings():
    return 0

def compute_utilization_percentage(earnings, spendings):
    earnings = max(1, earnings)
    return float('%.3f'%((spendings/earnings) * 100))

def base_render(html_page, **kwargs):
    header_data = {'earnings': retrieve_earnings(), 'spendings': retrieve_spendings(), 'utilization_threshold': 30
    }
    header_data['delta'] = header_data['earnings'] - header_data['spendings']
    header_data['utilization'] = compute_utilization_percentage(header_data['earnings'], header_data['spendings'])
    return render_template(html_page, header_data=header_data, **kwargs)
@app.route("/")
def index():
    return base_render('index.html')

@app.route("/new_transaction")
def load_transaction_page():
    return base_render("submission.html")

@app.route("/new_earnings")
def load_earnings_page():
    return base_render("earnings.html")