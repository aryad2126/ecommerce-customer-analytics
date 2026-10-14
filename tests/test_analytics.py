"""
Unit and integration tests for E-Commerce Intelligence Dashboard.
Covers core analytical calculations, money formatting, data mart integrity, and service resilience.
Uses Python standard library unittest.
"""

import sys
import unittest
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root and dashboard to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "dashboard"))

from dashboard.common import (
    money, mongo_status, hadoop_status, format_state_name,
    load_category_mart, load_delivery_mart, load_reviews_mart,
    load_top_products_mart
)

class TestAnalyticsFormulas(unittest.TestCase):
    def test_money_formatter(self):
        self.assertEqual(money(0), "R$ 0.00")
        self.assertEqual(money(np.nan), "R$ 0.00")
        self.assertEqual(money(45.5), "R$ 45.50")
        self.assertEqual(money(1250), "R$ 1.2K")
        self.assertEqual(money(3500000), "R$ 3.50M")

    def test_format_state_name(self):
        self.assertEqual(format_state_name("SP"), "São Paulo (SP)")
        self.assertEqual(format_state_name("RJ"), "Rio de Janeiro (RJ)")
        self.assertEqual(format_state_name("mg"), "Minas Gerais (MG)")
        self.assertEqual(format_state_name("XYZ"), "XYZ")
        self.assertEqual(format_state_name(""), "")
        self.assertEqual(format_state_name(None), "")

    def test_delivery_duration_and_delay(self):
        t_purchase = pd.Timestamp("2018-05-01 10:00:00")
        t_delivered = pd.Timestamp("2018-05-10 16:00:00")
        t_estimated = pd.Timestamp("2018-05-15 00:00:00")

        duration_days = (t_delivered - t_purchase).total_seconds() / 86400.0
        delay_days = (t_delivered - t_estimated).total_seconds() / 86400.0

        self.assertAlmostEqual(duration_days, 9.25, places=2)
        self.assertLess(delay_days, 0) # Arrived early
        self.assertFalse(delay_days > 0) # Is not late

    def test_late_delivery_identification(self):
        t_delivered_late = pd.Timestamp("2018-05-18 10:00:00")
        t_estimated = pd.Timestamp("2018-05-15 00:00:00")
        delay_days = (t_delivered_late - t_estimated).total_seconds() / 86400.0
        self.assertGreater(delay_days, 0) # Is late

    def test_repeat_rate_calculation(self):
        is_repeat = [False] * 8 + [True] * 2
        rate = sum(is_repeat) / len(is_repeat) * 100
        self.assertEqual(rate, 20.0)

class TestDataMartIntegrity(unittest.TestCase):
    def test_category_mart(self):
        cat_df = load_category_mart()
        self.assertFalse(cat_df.empty, "Category mart should not be empty")
        self.assertIn("category_english", cat_df.columns)
        self.assertIn("revenue", cat_df.columns)
        self.assertIn("units_sold", cat_df.columns)
        self.assertFalse(cat_df["category_english"].duplicated().any())
        self.assertGreater(len(cat_df), 50)

    def test_delivery_mart(self):
        del_orders, state_del = load_delivery_mart()
        self.assertFalse(del_orders.empty, "Delivery orders mart should not be empty")
        self.assertFalse(state_del.empty, "State delivery summary should not be empty")
        self.assertIn("delivery_duration_days", del_orders.columns)
        self.assertIn("is_late", del_orders.columns)
        self.assertGreater(len(state_del), 25) # Should cover ~27 Brazilian states

    def test_reviews_mart(self):
        dist_df, delay_df, trend_df, state_df = load_reviews_mart()
        self.assertFalse(dist_df.empty, "Review distribution should not be empty")
        self.assertEqual(len(dist_df), 5) # 1 to 5 stars
        self.assertFalse(delay_df.empty, "Review delay impact should not be empty")
        self.assertFalse(trend_df.empty, "Review monthly trend should not be empty")
        self.assertFalse(state_df.empty, "State review scores should not be empty")

    def test_top_products_mart(self):
        top_p = load_top_products_mart()
        self.assertFalse(top_p.empty, "Top products mart should not be empty")
        self.assertIn("product_id", top_p.columns)
        self.assertIn("revenue", top_p.columns)

class TestServiceResilience(unittest.TestCase):
    def test_status_functions_do_not_throw(self):
        m_state, m_detail = mongo_status()
        self.assertIn(m_state, ["up", "empty", "down"])
        self.assertIsInstance(m_detail, str)

        h_state, h_detail = hadoop_status()
        self.assertIn(h_state, ["up", "down"])
        self.assertIsInstance(h_detail, str)

if __name__ == "__main__":
    unittest.main()
