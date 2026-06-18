from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.db import query
from werkzeug.utils import secure_filename
from flask import current_app
import os

admin = Blueprint('admin', __name__, url_prefix='/admin')

CATEGORIES = [
    'Coffee',
    'Tea',
    'Cold Beverages',
    'Pizza',
    'Burgers',
    'Sandwiches',
    'Desserts'
]

# ==========================================
# DASHBOARD (CORRECTED WITH STATS DICTIONARY)
# ==========================================
@admin.route('/dashboard')
def dashboard():
    total_items = query(
        "SELECT COUNT(*) as total FROM menu_items",
        one=True
    )

    total_reservations = query(
        "SELECT COUNT(*) as total FROM reservations",
        one=True
    )

    total_contacts = query(
        "SELECT COUNT(*) as total FROM contacts",
        one=True
    )

    # HTML template (Jinja2) ke 'stats' variable ki error thik karne ke liye mapping
    stats = {
        'total_items': total_items['total'] if total_items else 0,
        'total_reservations': total_reservations['total'] if total_reservations else 0,
        'total_contacts': total_contacts['total'] if total_contacts else 0
    }

    return render_template(
        'admin/dashboard.html',
        total_items=total_items,
        total_reservations=total_reservations,
        total_contacts=total_contacts,
        stats=stats # Yahan stats pass kar diya hai
    )

# MENU MANAGEMENT
@admin.route('/menu')
def menu():
    items = query(
        "SELECT * FROM menu_items ORDER BY created_at DESC"
    )
    return render_template(
        'admin/menu.html',
        items=items
    )

# ADD MENU ITEM
@admin.route('/menu/add', methods=['GET', 'POST'])
def menu_add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        is_featured = 1 if request.form.get('is_featured') else 0
        is_available = 1 if request.form.get('is_available') else 0

        image = 'default.jpg'
        file = request.files.get('image')

        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                filename
            )
            file.save(upload_path)
            image = filename

        query(
            """
            INSERT INTO menu_items
            (
                name,
                description,
                price,
                category,
                image,
                is_featured,
                is_available
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                name,
                description,
                price,
                category,
                image,
                is_featured,
                is_available
            ),
            commit=True
        )

        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin.menu'))

    return render_template(
        'admin/menu_form.html',
        item=None,
        categories=CATEGORIES
    )

# EDIT MENU ITEM
@admin.route('/menu/edit/<int:id>', methods=['GET', 'POST'])
def menu_edit(id):
    item = query(
        "SELECT * FROM menu_items WHERE id=%s",
        (id,),
        one=True
    )

    if not item:
        flash('Item not found', 'danger')
        return redirect(url_for('admin.menu'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        is_featured = 1 if request.form.get('is_featured') else 0
        is_available = 1 if request.form.get('is_available') else 0

        image = item['image']
        file = request.files.get('image')

        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                filename
            )
            file.save(upload_path)
            image = filename

        query(
            """
            UPDATE menu_items
            SET
                name=%s,
                description=%s,
                price=%s,
                category=%s,
                image=%s,
                is_featured=%s,
                is_available=%s
            WHERE id=%s
            """,
            (
                name,
                description,
                price,
                category,
                image,
                is_featured,
                is_available,
                id
            ),
            commit=True
        )

        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin.menu'))

    return render_template(
        'admin/menu_form.html',
        item=item,
        categories=CATEGORIES
    )

# DELETE MENU ITEM
@admin.route('/menu/delete/<int:id>', methods=['POST'])
def menu_delete(id):
    query(
        "DELETE FROM menu_items WHERE id=%s",
        (id,),
        commit=True
    )
    flash('Menu item deleted!', 'success')
    return redirect(url_for('admin.menu'))

# RESERVATIONS
@admin.route('/reservations')
def reservations():
    reservations = query(
        "SELECT * FROM reservations ORDER BY created_at DESC"
    )
    return render_template(
        'admin/reservations.html',
        reservations=reservations
    )

# CONTACTS
@admin.route('/contacts')
def contacts():
    contacts = query(
        "SELECT * FROM contacts ORDER BY created_at DESC"
    )
    return render_template(
        'admin/contacts.html',
        contacts=contacts
    )

# USERS
@admin.route('/users')
def users():
    users = query(
        "SELECT * FROM users ORDER BY created_at DESC"
    )
    return render_template(
        'admin/users.html',
        users=users
    )