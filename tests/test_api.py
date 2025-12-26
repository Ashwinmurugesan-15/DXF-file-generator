import unittest
from fastapi.testclient import TestClient
import sys
import os

# Add the project root to the sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_beam_success(self):
        payload = {
            "component_type": "beam",
            "params": {"H": 200, "B": 100, "tw": 10, "tf": 15}
        }
        response = self.client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/dxf", response.headers["content-type"])

    def test_generate_column_success(self):
        payload = {
            "component_type": "column",
            "params": {"width": 100, "height": 200}
        }
        response = self.client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/dxf", response.headers["content-type"])

    def test_generate_invalid_type(self):
        payload = {
            "component_type": "invalid_type",
            "params": {"H": 200}
        }
        response = self.client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid component type", response.json()["detail"])

    def test_generate_validation_failure(self):
        # H=0 should fail validation
        payload = {
            "component_type": "beam",
            "params": {"H": 0, "B": 100, "tw": 10, "tf": 15}
        }
        response = self.client.post("/generate", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("must be between 1", response.json()["detail"])

if __name__ == '__main__':
    unittest.main()
