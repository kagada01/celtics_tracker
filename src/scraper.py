from nba_api.stats.endpoints import TeamGameLog, BoxScoreTraditionalV2
from nba_api.stats.static import teams
import pandas as pd
from datetime import datetime
import time

class CelticsScraper:
    def __init__(self):
        self.celtics_id = [team for team in teams.get_teams() 
                          if team['full_name'] == 'Boston Celtics'][0]['id']
        
    def get_game_ids(self, season='2024-25'):
        """Get all game IDs for the specified season"""
        game_log = TeamGameLog(team_id=self.celtics_id, season=season)
        games_df = game_log.get_data_frames()[0]
        return games_df['Game_ID'].tolist()
    
    def get_game_stats(self, game_id):
        """Get detailed box score for a specific game"""
        try:
            box_score = BoxScoreTraditionalV2(game_id=game_id)
            player_stats = box_score.get_data_frames()[0]
            
            # Filter for Celtics players only
            celtics_stats = player_stats[player_stats['TEAM_ID'] == self.celtics_id].copy()
            
            # Keep only columns that exist in the database schema
            valid_columns = [
                'GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 
                'PLAYER_ID', 'PLAYER_NAME', 'MIN', 'FGM', 'FGA', 'FG_PCT', 
                'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 
                'REB', 'AST', 'STL', 'BLK', 'PTS', 'PLUS_MINUS'
            ]
            
            # Select only valid columns
            celtics_stats = celtics_stats[valid_columns]
            
            # Add timestamp
            celtics_stats['SCRAPE_TIMESTAMP'] = datetime.now()
            
            time.sleep(1)  # Rate limiting
            return celtics_stats
        except Exception as e:
            print(f"Error fetching game {game_id}: {str(e)}")
            return None

    def get_season_stats(self, season='2024-25'):
        """Get all game stats for the specified season"""
        game_ids = self.get_game_ids(season)
        all_stats = []
        
        for game_id in game_ids:
            game_stats = self.get_game_stats(game_id)
            if game_stats is not None:
                all_stats.append(game_stats)
        
        if all_stats:
            return pd.concat(all_stats, ignore_index=True)
        return pd.DataFrame()

# Usage example:
if __name__ == "__main__":
    scraper = CelticsScraper()
    season_stats = scraper.get_season_stats()
    print(season_stats.head())