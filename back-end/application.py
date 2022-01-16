from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

EMPTY_RESPONSE = ""     # this is used for a successful action but there's no need to return anything

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name}: {self.description}"

def errorMessageWithCode(status, code):
    return {"status": status}, code

@app.route("/createinventory", methods=["POST"])
def createInventoryItem():
    if "name" not in request.json:
        return errorMessageWithCode("There was no item name given.", 400)
    if "description" not in request.json:
        description = ""
    else:
        description = request.json["description"]

    name = request.json["name"]
    if name == "":
        return errorMessageWithCode("The name field was empty.", 400)

    item = InventoryItem(name=name, description=description)
    db.session.add(item)
    db.session.commit()

    return {"id": item.id}

@app.route("/editinventory/<itemid>", methods=["PUT"])
def editInventoryItem(itemid):
    item = InventoryItem.query.get_or_404(itemid)

    if "name" in request.json:
        if request.json["name"] != "":
            item.name = request.json["name"]
        else:
            return errorMessageWithCode("Please fill in name field if you plan to change it.", 400)

    if "description" in request.json:
        item.description = request.json["description"]

    db.session.commit()
    return EMPTY_RESPONSE

@app.route("/deleteinventory/<itemid>", methods=["DELETE"])
def deleteInventoryItem(itemid):
    item = InventoryItem.query.get_or_404(itemid)

    db.session.delete(item)
    db.session.commit()

    return EMPTY_RESPONSE

@app.route("/getinventory")
def getItems():
    items = InventoryItem.query.all()
    output = []

    for item in items:
        output.append({"id": item.id, "name": item.name, "description": item.description})

    response = jsonify(output)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response