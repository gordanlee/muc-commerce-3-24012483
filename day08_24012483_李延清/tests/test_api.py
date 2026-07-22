import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app


class TestDay08API(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def login(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "student"

    def test_01_health_returns_200(self):
        rv = self.client.get("/health")
        self.assertEqual(rv.status_code, 200)
        data = rv.get_json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["service"], "day08-flask-upgrade")

    def test_02_metrics_requires_login(self):
        rv = self.client.get("/api/metrics")
        self.assertEqual(rv.status_code, 302)

    def test_03_metrics_returns_four_cards(self):
        self.login()
        rv = self.client.get("/api/metrics")
        self.assertEqual(rv.status_code, 200)
        data = rv.get_json()
        self.assertTrue(data["ok"])
        self.assertEqual(len(data["metrics"]), 4)
        labels = [m["label"] for m in data["metrics"]]
        self.assertIn("总用户数", labels)
        self.assertIn("总体流失率", labels)

    def test_04_categories_filter(self):
        self.login()
        rv = self.client.get("/api/categories?category=Fashion")
        self.assertEqual(rv.status_code, 200)
        data = rv.get_json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["category"], "Fashion")
        for row in data["rows"]:
            self.assertEqual(row["偏好品类"], "Fashion")

    def test_05_categories_all(self):
        self.login()
        rv = self.client.get("/api/categories")
        self.assertEqual(rv.status_code, 200)
        data = rv.get_json()
        self.assertEqual(data["category"], "全部")
        self.assertGreater(len(data["rows"]), 1)

    def test_06_categories_requires_login(self):
        rv = self.client.get("/api/categories")
        self.assertEqual(rv.status_code, 302)


if __name__ == "__main__":
    unittest.main()
