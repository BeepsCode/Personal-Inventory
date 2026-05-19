from flask import Blueprint, jsonify, request
from app import db

main = Blueprint('main', __name__)

# READ: Obtener todos los productos
@main.route("/", methods=["GET"])
def home():
    items = db.get_all_items()
    # Formateamos a JSON para que la prueba .rest lo lea fácilmente
    lista_productos = [{"id": i[0], "name": i[1], "quantity": i[2], "price": i[3]} for i in items]
    return jsonify(lista_productos), 200

# CREATE: Añadir producto por JSON
@main.route("/add", methods=["POST"])
def add():
    datos = request.get_json()
    db.add_item(datos["name"], datos["quantity"], datos["price"])
    return jsonify({"message": "Item added successfully"}), 201

# UPDATE: Editar producto por JSON
@main.route("/edit/<int:item_id>", methods=["POST"])
def edit(item_id):
    datos = request.get_json()
    db.update_item(item_id, datos["name"], datos["quantity"], datos["price"])
    return jsonify({"message": "Item updated successfully"}), 200

# DELETE: Eliminar producto
@main.route("/delete/<int:item_id>", methods=["GET", "DELETE"])
def delete(item_id):
    db.delete_item(item_id)
    return jsonify({"message": "Item deleted successfully"}), 200