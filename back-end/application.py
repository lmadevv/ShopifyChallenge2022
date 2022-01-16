from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name}: {self.description}"

def errorMessageWithCode(status, code):
    return {"status": status}, code

@app.route("/create", methods=["POST"])
def createInventoryItem():
    name = request.json["name"]
    description = request.json["description"]

    if name is None or name == "":
        return errorMessageWithCode(400, "There was no item name given.")
    if description is None:
        description = ""

    item = InventoryItem(name=name, description=description)
    db.session.add(item)
    db.session.commit()

    return {"id": item.id}