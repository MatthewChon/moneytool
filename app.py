from flask import Flask, render_template

app = Flask(__name__)

def retrieve_earnings():
    '''Retrieves earnings from the database
    
    Return:
        earnings (float: precision 2)
    '''
    return 0

def retrieve_spendings():
    '''Retrieves spending from the database
    Return:
        spendings (float: precision 2)
    '''
    return 0

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
    return base_render("transaction.html")

@app.route("/new_transaction")
def load_new_transaction_page():
    return base_render("spendingsform.html")

@app.route("/new_earnings")
def load_new_earnings_page():
    return base_render("earningsform.html")
#------- End of Page Configuration -------#