import sqlite3
import pandas as pd
import os
from datetime import datetime

class CelticsDB:
    def __init__(self, db_path='data/celtics.db'):
        # Ensure full path is used and directory exists
        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.initialize_db()
    
    def initialize_db(self):
        """Create the database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_stats (
                GAME_ID TEXT,
                TEAM_ID INTEGER,
                TEAM_ABBREVIATION TEXT,
                TEAM_CITY TEXT,
                PLAYER_ID INTEGER,
                PLAYER_NAME TEXT,
                MIN TEXT,
                FGM INTEGER,
                FGA INTEGER,
                FG_PCT FLOAT,
                FG3M INTEGER,
                FG3A INTEGER,
                FG3_PCT FLOAT,
                FTM INTEGER,
                FTA INTEGER,
                FT_PCT FLOAT,
                REB INTEGER,
                AST INTEGER,
                STL INTEGER,
                BLK INTEGER,
                PTS INTEGER,
                PLUS_MINUS INTEGER,
                SCRAPE_TIMESTAMP TIMESTAMP,
                PRIMARY KEY (GAME_ID, PLAYER_ID)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_game_stats(self, stats_df):
        """Save game stats to database"""
        conn = sqlite3.connect(self.db_path)
        
        # Convert DataFrame to SQL
        stats_df.to_sql('game_stats', conn, if_exists='append', index=False)
        
        conn.close()