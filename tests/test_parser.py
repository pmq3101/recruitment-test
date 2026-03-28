import unittest
from src.parser import parse_row

class TestParser(unittest.TestCase):

    def test_parse_row_valid(self):
        row = {
            "campaign_id": "CMP001 ",
            "date": "2025-01-01",
            "impressions": "12000",
            "clicks": "300",
            "spend": "45.50",
            "conversions": "12"
        }
        
        parsed = parse_row(row)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["campaign_id"], "CMP001")  # Should strip whitespace
        self.assertEqual(parsed["impressions"], 12000)
        self.assertEqual(parsed["clicks"], 300)
        self.assertEqual(parsed["spend"], 45.50)
        self.assertEqual(parsed["conversions"], 12)

    def test_parse_row_invalid_types(self):
        row = {
            "campaign_id": "CMP001",
            "date": "2025-01-01",
            "impressions": "not_an_int",
            "clicks": "300",
            "spend": "45.50",
            "conversions": "12"
        }
        
        parsed = parse_row(row)
        self.assertIsNone(parsed)  # Should return None for ValueError

    def test_parse_row_missing_keys(self):
        row = {
            "campaign_id": "CMP001",
            "date": "2025-01-01",
            # missing impressions
            "clicks": "300",
            "spend": "45.50",
        }
        
        parsed = parse_row(row)
        self.assertIsNone(parsed)  # Should return None for KeyError

    def test_parse_row_negative_values(self):
        row = {
            "campaign_id": "CMP001",
            "date": "2025-01-01",
            "impressions": "-100", # negative
            "clicks": "300",
            "spend": "45.50",
            "conversions": "12"
        }
        
        parsed = parse_row(row)
        self.assertIsNone(parsed) # Should return None for negative values

class TestStreamCSV(unittest.TestCase):
    def test_stream_csv_stats(self):
        import os
        from src.parser import stream_csv
        
        # Create a temporary CSV file
        test_file = "test_stream.csv"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("campaign_id,date,impressions,clicks,spend,conversions\n")
            f.write("C1,2025-01-01,100,10,1.0,1\n") # Valid
            f.write("C2,2025-01-01,-50,5,0.5,0\n")  # Negative (skip)
            f.write("C3,2025-01-01,abc,2,0.2,0\n") # Malformed (skip)
            
        success_list = []
        gen = stream_csv(test_file)
        while True:
            try:
                row = next(gen)
                success_list.append(row)
            except StopIteration as e:
                stats = e.value
                break
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
            
        self.assertEqual(len(success_list), 1)
        self.assertEqual(stats, (1, 2)) # 1 success, 2 skips

if __name__ == '__main__':
    unittest.main()
