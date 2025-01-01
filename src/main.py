from scraper import CelticsScraper
from database import CelticsDB

def main():
    # Initialize scraper and database
    scraper = CelticsScraper()
    db = CelticsDB()
    
    # Get and save current season stats
    season_stats = scraper.get_season_stats()
    if not season_stats.empty:
        db.save_game_stats(season_stats)
        print(f"Saved {len(season_stats)} game stat records")
    else:
        print("No stats retrieved")

if __name__ == "__main__":
    main()