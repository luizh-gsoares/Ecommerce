from models import *
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy

# Rotas principais
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('dashboard' if user.is_admin else 'index'))
        else:
            flash('Credenciais Inválidas. Verifique e tente novamente.', 'danger')
    return render_template('login.html')
 
@app.route('/logout')
def logout():
    session.clear()
    flash('Você realizou o logout.', 'info')
    return redirect(url_for('login'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
 
@app.route('/dashboard')
def dashboard():
    if not session.get('is_admin'):
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    users = User.query.all()
    products = Product.query.all()
    return render_template('dashboard.html', users=users, products=products)

@app.route('/user/delete/<int:id>')
def delete_user(id):
    if not session.get('is_admin'):
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluido com sucesso.', 'success')
    return redirect(url_for('dashboard'))

# Rotas de produtos
@app.route('/product/create', methods=['GET', 'POST'])
def create_product():
    if not session.get('is_admin'):
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        amount = request.form['amount']
        new_product = Product(name=name, price=price, description=description, amount=amount)
        db.session.add(new_product)
        db.session.commit()
        flash('Produto criado com sucesso', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_product.html')

@app.route('/product/view/<int:id>')
def view_product(id):
    product = Product.query.get(id)
    return render_template('view_product.html', product=product)

@app.route('/product/list')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if not session.get('is_admin'):
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('index'))
    
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        
        db.session.commit()
        flash('Produto atualizado com sucesso.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_product.html', product=product)

@app.route('/product/delete/<int:id>')
def delete_product(id):
    if not session.get('is_admin'):
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('index'))
    
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Produto excluido com sucesso.', 'success')
    return redirect(url_for('dashboard'))

# carrinho salvo na sessão
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    return render_template('cart.html', products=products)

@app.route('/cart/add/<int:id>')
def add_to_cart(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    flash('Produto adicionado ao carrinho.', 'success')
    return redirect(url_for('index'))

@app.route('/cart/remove/<int:id>')
def remove_from_cart(id):
    cart = session.get('cart', [])
    cart.remove(id)
    session['cart'] = cart
    flash('Produto removido do carrinho.', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/clear')
def clear_cart():
    session['cart'] = []
    flash('Carrinho limpo.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    