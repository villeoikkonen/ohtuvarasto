"""Tests for the warehouse web interface."""

import unittest

from app import create_app


class TestWarehouseWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def create_warehouse(self, name="Main", capacity="10"):
        return self.client.post("/warehouses", data={
            "name": name,
            "capacity": capacity,
        }, follow_redirects=True)

    def test_home_page_lists_empty_state(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No warehouses yet", response.data)

    def test_create_and_list_multiple_warehouses(self):
        self.create_warehouse("Main", "10")
        response = self.create_warehouse("Overflow", "25")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Main", response.data)
        self.assertIn(b"Overflow", response.data)
        self.assertIn(b"0 / 10 units", response.data)
        self.assertIn(b"0 / 25 units", response.data)

    def test_rejects_missing_name_invalid_capacity_and_duplicate_name(self):
        for form in (
            {"name": "  ", "capacity": "10"},
            {"name": "Broken", "capacity": "nope"},
            {"name": "Broken", "capacity": "0"},
            {"name": "Broken", "capacity": "nan"},
        ):
            response = self.client.post("/warehouses", data=form, follow_redirects=True)
            self.assertIn(b"Enter a name" if not form["name"].strip()
                          else b"Capacity must be", response.data)

        self.create_warehouse("Main")
        response = self.create_warehouse("main", "20")
        self.assertIn(b"already exists", response.data)
        self.assertEqual(len(self.app.extensions["warehouses"]), 1)

    def test_add_stock_uses_warehouse_capacity(self):
        self.create_warehouse("Main", "10")

        response = self.client.post("/warehouses/1/add", data={"quantity": "12"},
                                    follow_redirects=True)

        self.assertIn(b"Added 10 to Main", response.data)
        self.assertIn(b"10 / 10 units", response.data)

    def test_remove_stock_uses_existing_inventory_behavior(self):
        self.create_warehouse()
        self.client.post("/warehouses/1/add", data={"quantity": "8"})

        response = self.client.post("/warehouses/1/remove", data={"quantity": "20"},
                                    follow_redirects=True)

        self.assertIn(b"Removed 8 from Main", response.data)
        self.assertIn(b"0 / 10 units", response.data)

    def test_invalid_stock_quantities_are_rejected(self):
        self.create_warehouse()
        for quantity in ("", "-2", "0", "invalid", "inf"):
            response = self.client.post("/warehouses/1/add", data={"quantity": quantity},
                                        follow_redirects=True)
            self.assertIn(b"Quantity must be", response.data)

    def test_unknown_warehouse_returns_not_found(self):
        response = self.client.post("/warehouses/99/add", data={"quantity": "1"})

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
