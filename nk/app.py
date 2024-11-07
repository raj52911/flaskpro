# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Company, Item, Purchase, Sales
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    company = Company.query.first()
    return render_template('index.html', cash_balance=company.cash_balance)

@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        new_item = Item(item_name=item_name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('view_items'))
    return render_template('add_item.html')

@app.route('/items')
def view_items():
    items = Item.query.all()
    return render_template('view_items.html', items=items)

@app.route('/purchase/add', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        item_id = request.form['item_id']
        qty = int(request.form['qty'])
        rate = float(request.form['rate'])
        amount = qty * rate
        purchase = Purchase(item_id=item_id, qty=qty, rate=rate, amount=amount)
        
        # Update Company Cash and Item Quantity
        company = Company.query.first()
        company.cash_balance -= amount
        
        item = Item.query.get(item_id)
        item.qty += qty
        
        db.session.add(purchase)
        db.session.commit()
        return redirect(url_for('view_purchases'))
    items = Item.query.all()
    return render_template('add_purchase.html', items=items)

@app.route('/purchases')
def view_purchases():
    purchases = Purchase.query.all()
    return render_template('view_purchases.html', purchases=purchases)

@app.route('/sales/add', methods=['GET', 'POST'])
def add_sales():
    if request.method == 'POST':
        item_id = request.form['item_id']
        qty = int(request.form['qty'])
        rate = float(request.form['rate'])
        amount = qty * rate
        sale = Sales(item_id=item_id, qty=qty, rate=rate, amount=amount)
        
        # Update Company Cash and Item Quantity
        company = Company.query.first()
        company.cash_balance += amount
        
        item = Item.query.get(item_id)
        item.qty -= qty
        
        db.session.add(sale)
        db.session.commit()
        return redirect(url_for('view_sales'))
    items = Item.query.all()
    return render_template('add_sales.html', items=items)

@app.route('/sales')
def view_sales():
    sales = Sales.query.all()
    return render_template('view_sales.html', sales=sales)

@app.route('/report')
def report():
    company = Company.query.first()
    items = Item.query.all()
    return render_template('report.html', cash_balance=company.cash_balance, items=items)

with app.app_context():
    db.create_all() 

    if not Company.query.first():
        initial_company = Company(company_name="Namma Kadai", cash_balance=1000)
        db.session.add(initial_company)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
