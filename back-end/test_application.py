from flask_testing import TestCase
from application import app, db, InventoryItem

class BaseTestCase(TestCase):
    """
    Test case class that all test cases should extend.
    This class handles setting up the test Flask app and test database.
    """
    def create_app(self):
        """Creates the test Flask app and database."""
        test_app = app
        test_app.config["TESTING"] = True
        test_app.config["DEBUG"] = False
        test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://" # Creates an in-memory database for testing
        db.init_app(test_app)
        return test_app

    def setUp(self):
        """Automatically called before the start of any singular test case."""
        # Create a fresh database before running any test.
        db.create_all()

    def tearDown(self):
        """Automatically called after the end of any singular test case."""
        # Clear out the database after running any test.
        db.session.remove()
        db.drop_all()

    def createInventory(self):
        return InventoryItem(name="Kleenex", description="Tissues for people")

class AddInventoryItem(BaseTestCase):
    def testValidInventoryAdd(self):
        response = self.client.post("/createinventory", json=dict(name="Kleenex", description="Tissues for people"))

        assert response.status_code == 200
        assert response.json["id"] == 1

        inventoryItem = InventoryItem.query.get(1)

        assert inventoryItem.name == "Kleenex"
        assert inventoryItem.description == "Tissues for people"

    def testNameNotIncluded(self):
        response = self.client.post("/createinventory", json=dict(description="Tissues for people"))

        assert response.status_code == 400
        assert response.json["status"] == "There was no item name given."

    def testNameFieldEmpty(self):
        response = self.client.post("/createinventory", json=dict(name="", description="Tissues for people"))

        assert response.status_code == 400
        assert response.json["status"] == "The name field was empty."

    def testDescriptionNotIncluded(self):
        response = self.client.post("/createinventory", json=dict(name="Kleenex"))

        assert response.status_code == 200
        assert response.json["id"] == 1

        inventoryItem = InventoryItem.query.get(1)

        assert inventoryItem.name == "Kleenex"
        assert inventoryItem.description == ""

class EditInventoryItem(BaseTestCase):
    def testEditValidNameAndDescription(self):
        db.session.add(self.createInventory())
        db.session.commit()

        response = self.client.put("/editinventory/1", json=dict(name="Toilet Paper", description="To wipe"))

        assert response.status_code == 200

        item = InventoryItem.query.get(1)

        assert item.name == "Toilet Paper"
        assert item.description == "To wipe"

    def testEditInvalidName(self):
        db.session.add(self.createInventory())
        db.session.commit()

        response = self.client.put("/editinventory/1", json=dict(name="", description="To wipe"))

        assert response.status_code == 400
        assert response.json["status"] == "Please fill in name field if you plan to change it."

    def testInvalidItemToEdit(self):
        response = self.client.put("/editinventory/1", json=dict(name="Toilet Paper", description="To wipe"))

        assert response.status_code == 404

class DeleteInventoryItem(BaseTestCase):
    def testDeleteValidItem(self):
        db.session.add(self.createInventory())
        db.session.commit()

        response = self.client.delete("/deleteinventory/1")

        assert response.status_code == 200
        assert self.client.delete("/deleteinventory/1").status_code == 404

    def testDeleteInvalidItem(self):
        response = self.client.delete("/deleteinventory/1")

        assert response.status_code == 404