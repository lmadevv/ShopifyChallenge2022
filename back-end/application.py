from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

EMPTY_RESPONSE = ""     # this is used for a successful action but there's no need to return anything

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.name}: {self.description}"

def errorMessageWithCode(status, code):
    return {"status": status}, code

@app.route("/createinventory", methods=["POST"])
@cross_origin()
def createInventoryItem():
    if "name" not in request.json:
        return errorMessageWithCode("There was no item name given.", 400)
    if "description" not in request.json:
        description = ""
    else:
        description = request.json["description"]
    if "amount" not in request.json:
        return errorMessageWithCode("There was no amount given.", 400)

    name = request.json["name"]
    if name == "":
        return errorMessageWithCode("The name field was empty.", 400)

    item = InventoryItem(name=name, description=description, amount=request.json["amount"])
    db.session.add(item)
    db.session.commit()

    response = {"id": item.id}
    return response

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

    if "amount" in request.json:
        item.amount = request.json["amount"]

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
        output.append({"id": item.id, "name": item.name, "description": item.description, "amount": item.amount})

    response = jsonify(output)
    return response