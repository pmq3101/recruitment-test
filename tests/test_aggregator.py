import unittest
from src.aggregator import (
    aggregate_campaigns,
    compute_metrics,
    top_n_by_ctr,
    top_n_by_cpa
)

class TestAggregator(unittest.TestCase):

    def setUp(self):
        self.sample_rows = [
            {"campaign_id": "CMP1", "impressions": 1000, "clicks": 50, "spend": 10.0, "conversions": 2},
            {"campaign_id": "CMP1", "impressions": 2000, "clicks": 150, "spend": 20.0, "conversions": 3},
            {"campaign_id": "CMP2", "impressions": 5000, "clicks": 100, "spend": 50.0, "conversions": 0},
        ]

    def test_aggregate_campaigns(self):
        # We wrap sample_rows in a generator that "returns" stats like our real parser
        def mock_generator():
            for row in self.sample_rows:
                yield row
            return len(self.sample_rows), 0
            
        campaigns, stats = aggregate_campaigns(mock_generator())
        
        self.assertEqual(len(campaigns), 2)
        self.assertEqual(stats, (3, 0)) # 3 successful rows, 0 skipped
        
        # Check CMP1 aggregation
        self.assertEqual(campaigns["CMP1"]["total_impressions"], 3000)
        self.assertEqual(campaigns["CMP1"]["total_clicks"], 200)
        self.assertEqual(campaigns["CMP1"]["total_spend"], 30.0)
        self.assertEqual(campaigns["CMP1"]["total_conversions"], 5)

    def test_aggregate_empty_data(self):
        # Mocking empty generator with return stats (0, 0)
        def mock_empty_generator():
             if False: yield {} # Make it a generator
             return 0, 0
             
        campaigns, stats = aggregate_campaigns(mock_empty_generator())
        
        self.assertEqual(len(campaigns), 0)
        self.assertEqual(stats, (0, 0))

    def test_compute_metrics(self):
        aggregated_data = {
            "CMP1": {
                "total_impressions": 3000,
                "total_clicks": 300,
                "total_spend": 50.0,
                "total_conversions": 5
            },
            "CMP2": {
                "total_impressions": 1000,
                "total_clicks": 0,
                "total_spend": 10.0,
                "total_conversions": 0
            }
        }
        
        metrics = compute_metrics(aggregated_data)
        
        self.assertEqual(len(metrics), 2)
        
        # Verify CMP1
        cmp1 = next(c for c in metrics if c["campaign_id"] == "CMP1")
        self.assertAlmostEqual(cmp1["CTR"], 0.1)  # 300 / 3000
        self.assertAlmostEqual(cmp1["CPA"], 10.0) # 50 / 5
        
        # Verify CMP2 (edge cases: zero division)
        cmp2 = next(c for c in metrics if c["campaign_id"] == "CMP2")
        self.assertAlmostEqual(cmp2["CTR"], 0.0)
        self.assertIsNone(cmp2["CPA"])

    def test_top_n_by_ctr(self):
        campaigns = [
            {"campaign_id": "CMP1", "CTR": 0.05, "CPA": 10},
            {"campaign_id": "CMP2", "CTR": 0.10, "CPA": 20},
            {"campaign_id": "CMP3", "CTR": 0.01, "CPA": 5},
        ]
        
        top = top_n_by_ctr(campaigns, n=2)
        
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]["campaign_id"], "CMP2") # Highest CTR
        self.assertEqual(top[1]["campaign_id"], "CMP1")

    def test_top_n_by_cpa(self):
        campaigns = [
            {"campaign_id": "CMP1", "CTR": 0.05, "CPA": 10.0},
            {"campaign_id": "CMP2", "CTR": 0.10, "CPA": 5.0},
            {"campaign_id": "CMP3", "CTR": 0.01, "CPA": None}, # Should be excluded
            {"campaign_id": "CMP4", "CTR": 0.02, "CPA": 20.0},
        ]
        
        top = top_n_by_cpa(campaigns, n=2)
        
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]["campaign_id"], "CMP2") # Lowest CPA
        self.assertEqual(top[1]["campaign_id"], "CMP1")
        # CMP3 must not be in the list

if __name__ == '__main__':
    unittest.main()
