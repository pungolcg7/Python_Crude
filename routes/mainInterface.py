import sqlite3
from flask import render_template, request, flash, redirect, url_for


def init_mainInterface_routes(app):
    app.secret_key = 'your_secret_key'  # Replace with your actual secret key

    def get_db_connection():
        conn = sqlite3.connect('database.db')  # Replace with your actual database path
        conn.row_factory = sqlite3.Row
        return conn

    @app.route('/')
    @app.route('/index')
    def index():
        conn = get_db_connection()
        user_count = conn.execute('SELECT COUNT(*) FROM User').fetchone()[0]
        category_count = conn.execute('SELECT COUNT(*) FROM Category').fetchone()[0]
        product_count = conn.execute('SELECT COUNT(*) FROM Product').fetchone()[0]
        total_stock = conn.execute('SELECT SUM(current_stock) FROM Product').fetchone()[0]
        count_employee = conn.execute('''SELECT COUNT(*) FROM User WHERE role = 'Manager' ''').fetchone()[0]
        return render_template("index.html", user_count=user_count, category_count=category_count, product_count=product_count, total_stock=total_stock, count_employee=count_employee)

    @app.route('/products')
    def products():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Product')
        products = cursor.fetchall()
        conn.close()
        return render_template('products.html', products=products)
    @app.route('/add_product', methods=['POST'])
    def add_product():
        code = request.form['code']
        image = request.form['image']
        name = request.form['name']
        category = request.form['category']
        cost = request.form['cost']
        price = request.form['price']
        current_stock = request.form['current_stock']
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO Product (code, image, name, category, cost, price, current_stock) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (code, image, name, category, cost, price, current_stock))
            conn.commit()
            flash('Product added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
        finally:
            conn.close()

        return redirect(url_for('products'))
    @app.route('/edit_product', methods=['POST'])
    def edit_product():
        try:
            product_id = request.form['id']
            code = request.form['code']
            image = request.form['image']
            name = request.form['name']
            category = request.form['category']
            cost = request.form['cost']
            price = request.form['price']
            current_stock = request.form['current_stock']

            conn = get_db_connection()
            conn.execute(
                'UPDATE Product SET code = ?, image = ?, name = ?, category = ?, cost = ?, price = ?, current_stock = ? WHERE id = ?',
                (code, image, name, category, cost, price, current_stock, product_id))
            conn.commit()
            conn.close()
            flash('Product updated successfully!')
        except Exception as e:
            flash(f'Error updating product: {e}')

        return redirect('/products')
    @app.route('/delete_product/<int:id>', methods=['POST'])
    def delete_product(id):
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM Product WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            flash('Product deleted successfully!')
        except Exception as e:
            flash(f'Error deleting product: {e}')

        return redirect('/products')

    @app.route('/category')
    def category():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Category')
        categories = cursor.fetchall()
        conn.close()
        return render_template("category.html", categories=categories)
    @app.route('/add_category', methods=['POST'])
    def add_category():
        name = request.form['name']
        description = request.form['description']
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO Category (name, description) VALUES (?, ?)',
                (name, description)
            )
            conn.commit()
            flash('Category added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding category: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('category'))
    @app.route('/edit_category', methods=['POST'])
    def edit_category():
        try:
            category_id = request.form['id']
            name = request.form['name']
            description = request.form['description']

            conn = get_db_connection()
            conn.execute(
                'UPDATE Category SET name = ?, description = ? WHERE id = ?',
                (name, description, category_id)
            )
            conn.commit()
            flash('Category updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating category: {e}', 'error')
        finally:
            conn.close()

        return redirect(url_for('category'))
    @app.route('/delete_category/<int:id>', methods=['POST'])
    def delete_category(id):
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM Category WHERE id = ?', (id,))
            conn.commit()
            flash('Category deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting category: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('category'))

    @app.route('/users')
    def users():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User')
        users = cursor.fetchall()
        conn.close()
        return render_template('users.html', users=users)
    @app.route('/add_user', methods=['POST'])
    def add_user():
        code = request.form['code']
        profile = request.form['profile']
        name = request.form['name']
        gender = request.form['gender']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO User (code, profile, name, gender, role, email, phone, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (code, profile, name, gender, role, email, phone, address))
            conn.commit()
            flash('User added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding user: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('users'))
    @app.route('/edit_user', methods=['POST'])
    def edit_user():
        try:
            user_id = request.form['id']
            code = request.form['code']
            profile = request.form['profile']
            name = request.form['name']
            gender = request.form['gender']
            role = request.form['role']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']

            conn = get_db_connection()
            conn.execute(
                'UPDATE User SET code = ?, profile = ?, name = ?, gender = ?, role = ?, email = ?, phone = ?, address = ? WHERE id = ?',
                (code, profile, name, gender, role, email, phone, address, user_id))
            conn.commit()
            flash('User updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating user: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('users'))
    @app.route('/delete_user/<int:id>', methods=['POST'])
    def delete_user(id):
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM User WHERE id = ?', (id,))
            conn.commit()
            flash('User deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error deleting user: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('users'))


