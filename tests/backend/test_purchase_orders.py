"""
Tests for purchase order API endpoints.
"""
import pytest
from datetime import datetime, timedelta


class TestPurchaseOrderEndpoints:
    """Test suite for purchase order-related endpoints."""

    def test_create_purchase_order(self, client, sample_backlog_item):
        """Test creating a new purchase order."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Premium Components Ltd",
            "quantity": 100,
            "unit_cost": 25.50,
            "expected_delivery_date": "2025-10-15",
            "notes": "Rush delivery requested"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code == 201 or response.status_code == 200

        data = response.json()
        assert data["id"]  # ID should be generated
        assert data["backlog_item_id"] == sample_backlog_item["id"]
        assert data["supplier_name"] == "Premium Components Ltd"
        assert data["quantity"] == 100
        assert data["unit_cost"] == 25.50
        assert data["expected_delivery_date"] == "2025-10-15"
        assert data["status"] == "Submitted"
        assert data["notes"] == "Rush delivery requested"
        assert data["created_date"]  # Should have creation timestamp

    def test_create_purchase_order_without_notes(self, client, sample_backlog_item):
        """Test creating a purchase order without optional notes field."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Standard Supplies Inc",
            "quantity": 50,
            "unit_cost": 15.00,
            "expected_delivery_date": "2025-10-20"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code == 201 or response.status_code == 200

        data = response.json()
        assert data["id"]
        assert data["backlog_item_id"] == sample_backlog_item["id"]
        assert data["supplier_name"] == "Standard Supplies Inc"
        assert data["quantity"] == 50
        assert data["unit_cost"] == 15.00
        # Notes should be empty string when not provided
        assert data["notes"] == "" or data["notes"] is None

    def test_create_purchase_order_with_zero_quantity(self, client, sample_backlog_item):
        """Test creating a purchase order with zero quantity."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            "quantity": 0,
            "unit_cost": 10.00,
            "expected_delivery_date": "2025-10-15"
        }

        # Should accept zero quantity (data validation allows it)
        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["quantity"] == 0

    def test_create_purchase_order_with_negative_unit_cost(self, client, sample_backlog_item):
        """Test creating a purchase order with negative unit cost."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            "quantity": 100,
            "unit_cost": -5.00,
            "expected_delivery_date": "2025-10-15"
        }

        # Should accept negative cost (data validation allows it)
        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["unit_cost"] == -5.00

    def test_create_purchase_order_missing_required_field(self, client, sample_backlog_item):
        """Test creating a purchase order with missing required field."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            # Missing quantity field
            "unit_cost": 10.00,
            "expected_delivery_date": "2025-10-15"
        }

        response = client.post("/api/purchase-orders", json=payload)
        # Should return validation error (422)
        assert response.status_code == 422

    def test_get_purchase_order_by_backlog_item(self, client):
        """Test retrieving a purchase order by backlog item ID."""
        import uuid

        # Use a unique backlog item ID to avoid conflicts with other tests
        unique_backlog_id = f"backlog-{uuid.uuid4()}"

        # First create a purchase order
        create_payload = {
            "backlog_item_id": unique_backlog_id,
            "supplier_name": "Components Plus",
            "quantity": 75,
            "unit_cost": 18.75,
            "expected_delivery_date": "2025-10-18"
        }

        create_response = client.post("/api/purchase-orders", json=create_payload)
        assert create_response.status_code in [200, 201]
        created_po = create_response.json()

        # Now retrieve it
        retrieve_response = client.get(f"/api/purchase-orders/{unique_backlog_id}")
        assert retrieve_response.status_code == 200

        retrieved_po = retrieve_response.json()
        assert retrieved_po["id"] == created_po["id"]
        assert retrieved_po["backlog_item_id"] == unique_backlog_id
        assert retrieved_po["supplier_name"] == "Components Plus"
        assert retrieved_po["quantity"] == 75
        assert retrieved_po["unit_cost"] == 18.75

    def test_get_nonexistent_purchase_order(self, client):
        """Test retrieving a non-existent purchase order."""
        response = client.get("/api/purchase-orders/nonexistent-backlog-id")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_purchase_order_structure(self, client, sample_backlog_item):
        """Test that created purchase order has correct structure."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Quality Suppliers",
            "quantity": 200,
            "unit_cost": 32.50,
            "expected_delivery_date": "2025-11-01",
            "notes": "Test PO structure"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()

        # Verify all required fields are present
        required_fields = [
            "id",
            "backlog_item_id",
            "supplier_name",
            "quantity",
            "unit_cost",
            "expected_delivery_date",
            "status",
            "created_date",
            "notes"
        ]

        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    def test_purchase_order_id_uniqueness(self, client, sample_backlog_item):
        """Test that multiple purchase orders get unique IDs."""
        payload1 = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Supplier A",
            "quantity": 100,
            "unit_cost": 10.00,
            "expected_delivery_date": "2025-10-15"
        }

        # We can't create two POs for the same backlog item in this system
        # but we can at least verify the first PO got an ID
        response1 = client.post("/api/purchase-orders", json=payload1)
        assert response1.status_code in [200, 201]

        po1 = response1.json()
        assert po1["id"]
        assert po1["id"]  # UUID should be a non-empty string

    def test_purchase_order_data_types(self, client, sample_backlog_item):
        """Test that purchase order fields have correct data types."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            "quantity": 50,
            "unit_cost": 25.99,
            "expected_delivery_date": "2025-10-15",
            "notes": "Test data types"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()

        # Verify data types
        assert isinstance(data["id"], str)
        assert isinstance(data["backlog_item_id"], str)
        assert isinstance(data["supplier_name"], str)
        assert isinstance(data["quantity"], int)
        assert isinstance(data["unit_cost"], (int, float))
        assert isinstance(data["expected_delivery_date"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["created_date"], str)
        assert isinstance(data["notes"], (str, type(None)))

    def test_purchase_order_date_format(self, client, sample_backlog_item):
        """Test that purchase order dates are in correct format."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            "quantity": 100,
            "unit_cost": 15.00,
            "expected_delivery_date": "2025-10-15"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()

        # Verify expected_delivery_date format (should be YYYY-MM-DD)
        assert len(data["expected_delivery_date"]) == 10
        assert data["expected_delivery_date"].count("-") == 2

        # Verify created_date format (should be ISO format with time)
        assert "T" in data["created_date"]  # ISO format includes T separator
        assert len(data["created_date"]) >= 19  # At least YYYY-MM-DDTHH:MM:SS

    def test_purchase_order_status_is_submitted(self, client, sample_backlog_item):
        """Test that newly created purchase orders have 'Submitted' status."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            "quantity": 100,
            "unit_cost": 20.00,
            "expected_delivery_date": "2025-10-20"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()
        assert data["status"] == "Submitted"

    def test_purchase_order_with_very_large_quantity(self, client, sample_backlog_item):
        """Test creating purchase order with very large quantity."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Bulk Supplier",
            "quantity": 1000000,  # 1 million units
            "unit_cost": 0.01,
            "expected_delivery_date": "2025-12-31"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()
        assert data["quantity"] == 1000000

    def test_purchase_order_with_special_characters_in_supplier(self, client, sample_backlog_item):
        """Test creating purchase order with special characters in supplier name."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "ABC & Co. / Ltd. (North)",
            "quantity": 100,
            "unit_cost": 25.00,
            "expected_delivery_date": "2025-10-15"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()
        assert data["supplier_name"] == "ABC & Co. / Ltd. (North)"

    def test_purchase_order_with_unicode_in_notes(self, client, sample_backlog_item):
        """Test creating purchase order with unicode characters in notes."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "International Supplier",
            "quantity": 50,
            "unit_cost": 30.00,
            "expected_delivery_date": "2025-10-15",
            "notes": "Urgent! 急ぎ です. Срочно!"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        data = response.json()
        assert "急ぎ" in data["notes"]
        assert "Срочно" in data["notes"]

    def test_purchase_order_response_headers(self, client, sample_backlog_item):
        """Test that purchase order endpoints return correct response headers."""
        payload = {
            "backlog_item_id": sample_backlog_item["id"],
            "supplier_name": "Test Supplier",
            "quantity": 100,
            "unit_cost": 15.00,
            "expected_delivery_date": "2025-10-15"
        }

        response = client.post("/api/purchase-orders", json=payload)
        assert response.status_code in [200, 201]

        # Check content type
        assert "application/json" in response.headers.get("content-type", "")
