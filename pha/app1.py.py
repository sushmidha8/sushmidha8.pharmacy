from flask import Flask, render_template, request, redirect, url_for,render_template_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route("/", methods=['POST'])
def login():
    username = request.form['name']
    password = request.form['password']
    if username == "selvikumuthamhospital" and password == "@Skh08":
        return redirect(url_for('basic_page'))
    else:
        return render_template('afterlogin.html')

@app.route('/basicpage')
def basic_page():
    return render_template('basicpage.html')

@app.route('/redirect', methods=['POST'])
def submit():
    name = request.form['name']
    number = request.form['password']
    return redirect(url_for('after_login'))

@app.route('/after_login')
def after_login():
    return render_template("afterlogin.html")

@app.route('/redirect1', methods=['GET'])
def redirect_page1():
    return redirect(url_for('page1'))

@app.route('/redirect2')
def redirect_page2():
    return redirect(url_for('page2'))

@app.route('/redirect3')
def redirect_page3():
    return redirect(url_for('page3'))

@app.route('/redirect4')
def redirect_page4():
    return redirect(url_for('page4'))

@app.route('/redirect5')
def redirect_page5():
    return redirect(url_for('page5'))

@app.route('/redirect6')
def redirect_page6():
    return redirect(url_for('page6'))

@app.route('/patientrecord1')
def page1():
    return redirect(url_for('patient_record1'))

@app.route('/bill')
def page2():
    return render_template('billgen.html')

@app.route('/stockdetails')
def page3():
    return render_template('stockdetails.html')

@app.route('/patient_record1')
def patient_record1():
    return render_template("patientrecord1.html")

@app.route('/patientrecord')
def page5():
    return render_template('find.html')


@app.route('/stockdetails1')
def page4():
    return render_template('stockdetails1.html')
global grand_total
grand_total = 0.0

def home():
    return render_template('billgen.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    items = request.form.getlist('items[]')
    prices = request.form.getlist('prices[]')
    quantities = request.form.getlist('quantities[]')

    invoice_items = []
    total_amount = 0

    for item, price, quantity in zip(items, prices, quantities):
        amount = float(price) * int(quantity)
        invoice_items.append({
            'item': item,
            'price': float(price),
            'quantity': int(quantity),
            'amount': amount
        })
        total_amount += amount

    return render_template('billgen.html', invoice_items=invoice_items, total_amount=total_amount)

stocks=[]

@app.route('/')
def index():
    return render_template('stockdetails.html')

@app.route('/add_stock', methods=['POST'])
def add_stock():
    if request.method == 'POST':
        global stock_name
        stock_name = request.form['stockName']
        stock_quantity = int(request.form['stockQuantity'])
        stock_price = float(request.form['stockPrice'])
        stock_data = f"Name: {stock_name},Stock Quantity  : {stock_quantity }, Stock Price: {stock_price}\n"
        with open('stocks.txt', 'a') as f:
            f.write( stock_data)
        with open('stocks.txt','r')as f:
            content=f.read()
            stocks.append(content)
            return redirect(url_for('after_login'))

@app.route('/')
def home():
    return render_template('find.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    file_path = 'patients.txt'  
    results = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if search_term in line:
                    results.append(f"Line {line_number}: {line.strip()}")
    except FileNotFoundError:
        results.append(f"The file {file_path} does not exist.")
    except Exception as e:
        results.append(f"An error occurred: {e}")

    return render_template('search_results.html', search_term=search_term, results=results)


patient_stack = []

@app.route('/submit', methods=['POST'])
def submit11():
    global name1
    name1 = request.form['number']
    age = request.form['age']
    gender = request.form['gender']
    diagnosis = request.form['diagnosis']
    patient_data = {'Number': name1,'Age': age, 'Gender': gender, 
'Diagnosis': diagnosis}
    
    patient_stack.append(patient_data)
    

    with open('patients.txt', 'a') as f:
        while patient_stack:
            entry = patient_stack.pop()
            f.write(f"Number: {entry['Number']}, Age: {entry['Age']}, Gender: {entry['Gender']}, Diagnosis: {entry['Diagnosis']}\n")
            
    return redirect(url_for('after_login'))

@app.route('/')
def home1():
    return render_template('stockdetails1.html')

@app.route('/search1', methods=['POST'])
def search1():
    search_term = request.form['search_term']
    file_path = 'stocks.txt'  
    results = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if search_term in line:
                    results.append(f"Line {line_number}: {line.strip()}")
    except FileNotFoundError:
        results.append(f"The file {file_path} does not exist.")
    except Exception as e:
        results.append(f"An error occurred: {e}")

    return render_template('search_results1.html', search_term=search_term, results=results)


if __name__ == '__main__':
    app.run(debug=True)
