# src/populate_database.py
import pandas as pd
from scraper import CelticsScraper
from database import CelticsDB
import time

def main():
    try:
        scraper = CelticsScraper()
        db = CelticsDB()
        
        # Get season stats with limited number of games to avoid rate limiting
        game_ids = scraper.get_game_ids(season='2024-25')  # Set to all '24-'25 games
        
        all_stats = []
        for game_id in game_ids:
            game_stats = scraper.get_game_stats(game_id)
            if game_stats is not None:
                all_stats.append(game_stats)
                time.sleep(1)  # Rate limiting
        
        # Combine stats
        if all_stats:
            season_stats = pd.concat(all_stats, ignore_index=True)
            
            # Save to database
            db.save_game_stats(season_stats)
            print(f"Saved {len(season_stats)} game stats records")
        else:
            print("No game stats retrieved")
    
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()