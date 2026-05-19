from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app import login_manager
from app import db
from app import db_users

# Definimos el Blueprint para cumplir con la estructura del curso
main = Blueprint('main', __name__)

class Usuario(UserMixin if 'UserMixin' in globals() else object):
    def __init__(self, username):
        self.id = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user_data = db_users.get_user_by_id(user_id)
    if user_data:
        return Usuario(user_data['username'])
    return None

@main.route("/")
@login_required
def home():
    search = request.args.get("search", "")
    sort_by = request.args.get("sort", "")
    items = db.get_all_items()
    if search:
        items = [item for item in items if search.lower() in item[1].lower()]
    if sort_by == "id": items.sort(key=lambda x: x[0])
    elif sort_by == "name": items.sort(key=lambda x: x[1].lower())
    elif sort_by == "quantity": items.sort(key=lambda x: x[2])
    elif sort_by == "price": items.sort(key=lambda x: x[3])
    return render_template("index.html", items=items, search=search, sort_by=sort_by, nombre=current_user.id)

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db_users.verify_credentials(username, password):
            user = Usuario(username)
            login_user(user)
            return redirect(url_for('main.home'))
        return render_template(
            'error.html', 
            error_code=401, 
            error_message="Invalid Credentials! The username or password you entered is incorrect."
        ), 401
    return render_template('login.html', error=error)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/add", methods=["GET", "POST"])
@login_required 
def add():
    error = ""
    if request.method == "POST":
        name = request.form["name"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        if not name or quantity < 0 or price < 0:
            error = "Please enter a valid name, quantity, and price."
        else:   
            db.add_item(name, quantity, price)
            return redirect(url_for("main.home"))
    return render_template("add.html", error=error)

@main.route("/delete/<int:item_id>")
@login_required 
def delete(item_id):
    db.delete_item(item_id)
    return redirect(url_for("main.home"))

@main.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit(item_id):
    item = db.get_item_by_id(item_id)
    if request.method == "POST":
        name = request.form["name"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        db.update_item(item_id, name, quantity, price)
        return redirect(url_for("main.home"))
    return render_template("edit.html", item=item)

@main.route('/register', methods=['GET', 'POST'])
def register():
    error = ""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if db_users.add_user(username, password):
            return redirect(url_for('main.login'))
        else: error = "This username is already taken."
    return render_template('register.html', error=error)

@main.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    error = ""
    success = ""
    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        if not db_users.verify_credentials(current_user.id, current_password):
            error = "Your current password is incorrect."
        elif new_password != confirm_password:
            error = "The new passwords do not match."
        elif not new_password.strip():
            error = "Password cannot be empty."
        else:
            db_users.update_user_password(current_user.id, new_password)
            success = "Your password has been changed successfully!"
    return render_template("change_password.html", error=error, success=success)