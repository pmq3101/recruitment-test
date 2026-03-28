import unittest
from src.writer import format_row

class TestWriter(unittest.TestCase):

    def test_format_row(self):
        campaign = {
            "campaign_id": "CMP123",
            "total_impressions": 10000,
            "total_clicks": 350,
            "total_spend": 123.456,
            "total_conversions": 12,
            "CTR": 0.035,
            "CPA": 10.288
        }
        
        formatted = format_row(campaign)
        
        # Check exact decimal formatting
        self.assertEqual(formatted["CTR"], "0.0350")
        self.assertEqual(formatted["CPA"], "10.29")
        self.assertEqual(formatted["total_spend"], "123.46")
        self.assertEqual(formatted["total_impressions"], 10000)

    def test_format_row_none_cpa(self):
        campaign = {
            "campaign_id": "CMP123",
            "total_impressions": 10000,
            "total_clicks": 0,
            "total_spend": 10.5,
            "total_conversions": 0,
            "CTR": 0.0,
            "CPA": None
        }
        
        formatted = format_row(campaign)
        
        self.assertEqual(formatted["CTR"], "0.0000")
        self.assertEqual(formatted["CPA"], "") # None should output empty string
        self.assertEqual(formatted["total_spend"], "10.50")

if __name__ == '__main__':
    unittest.main()
