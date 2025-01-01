import unittest
from src.scraper import CelticsScraper
from src.database import CelticsDB
import pandas as pd
import os
import sqlite3
from datetime import datetime
import time

class TestCelticsStats(unittest.TestCase):
    def setUp(self):
        self.test_db_path = 'data/test_celtics.db'
        self.scraper = CelticsScraper()
        self.db = CelticsDB(db_path=self.test_db_path)
        
    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
    def test_game_ids_retrieval(self):
        game_ids = self.scraper.get_game_ids()
        self.assertIsInstance(game_ids, list)
        self.assertTrue(len(game_ids) > 0)
        self.assertTrue(all(isinstance(id, str) for id in game_ids))
        
    def test_single_game_stats(self):
        # Get first game ID
        game_ids = self.scraper.get_game_ids()
        first_game = game_ids[0]
        
        # Test stats retrieval
        stats = self.scraper.get_game_stats(first_game)
        self.assertIsInstance(stats, pd.DataFrame)
        self.assertTrue(len(stats) > 0)
        
        # Verify required columns
        required_cols = ['GAME_ID', 'PLAYER_ID', 'PLAYER_NAME', 'MIN', 'PTS']
        self.assertTrue(all(col in stats.columns for col in required_cols))
        
    def test_database_operations(self):
        # Get sample data
        game_ids = self.scraper.get_game_ids()[:3]  # Limit to first 3 games
        stats = self.scraper.get_game_stats(game_ids[0])
        
        # Test database insertion
        self.db.save_game_stats(stats)
        
        # Verify data in database
        conn = sqlite3.connect(self.test_db_path)
        saved_data = pd.read_sql('SELECT * FROM game_stats', conn)
        conn.close()
        
        self.assertEqual(len(saved_data), len(stats))
        self.assertTrue(all(stats['PLAYER_ID'].isin(saved_data['PLAYER_ID'])))
        
    def test_full_pipeline(self):
        # Get season stats for first few games
        game_ids = self.scraper.get_game_ids()[:5]  # Limit to first 5 games
        
        all_stats = []
        for game_id in game_ids:
            game_stats = self.scraper.get_game_stats(game_id)
            if game_stats is not None:
                all_stats.append(game_stats)
                time.sleep(1)  # Add small delay between API calls
        
        season_stats = pd.concat(all_stats, ignore_index=True)
        
        self.assertIsInstance(season_stats, pd.DataFrame)
        
        # Save to database
        self.db.save_game_stats(season_stats)
        
        # Verify data integrity
        conn = sqlite3.connect(self.test_db_path)
        saved_data = pd.read_sql('SELECT * FROM game_stats', conn)
        conn.close()
        
        self.assertEqual(len(saved_data), len(season_stats))
        
if __name__ == '__main__':
    unittest.main()