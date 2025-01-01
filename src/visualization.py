# src/visualization.py
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Celtics color palette
CELTICS_GREEN = '#007A33'
CELTICS_WHITE = '#FFFFFF'
CELTICS_SECONDARY_GREEN = '#4A7C59'

def visualize_player_performance(db_path='data/celtics.db', output_dir='data'):
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    # Player Performance Scatter Plot
    player_stats_query = """
    SELECT 
        PLAYER_NAME, 
        AVG(PTS) as Avg_Points, 
        AVG(REB) as Avg_Rebounds, 
        AVG(AST) as Avg_Assists
    FROM game_stats
    GROUP BY PLAYER_NAME
    """
    player_df = pd.read_sql_query(player_stats_query, conn)
    
    # Scoring Visualization
    scoring_fig = px.scatter(player_df, 
                     x='Avg_Points', 
                     y='Avg_Assists', 
                     size='Avg_Rebounds',
                     hover_name='PLAYER_NAME',
                     title='Celtics Players Scoring Performance',
                     labels={'Avg_Points': 'Average Points', 
                             'Avg_Assists': 'Average Assists'},
                     color_discrete_sequence=[CELTICS_GREEN],
                     size_max=20)
    
    # Add annotation explaining the visualization
    scoring_fig.add_annotation(
        text="This scatter plot shows each Celtics player's offensive performance. " 
             "The x-axis represents average points scored, the y-axis shows average assists, " 
             "and the size of each bubble indicates average rebounds.",
        xref="paper", yref="paper",
        x=0.5, y=-0.15,
        showarrow=False
    )
    
    scoring_fig.update_layout(
        title_x=0.5, 
        template='plotly_white',
        plot_bgcolor=CELTICS_WHITE,
        paper_bgcolor=CELTICS_WHITE,
        height=800  # Increase height to accommodate annotation
    )
    pio.write_html(scoring_fig, file=f'{output_dir}/player_scoring_performance.html', auto_open=False)
    
    # Rebounding Visualization
    rebounding_query = """
    SELECT 
        PLAYER_NAME, 
        SUM(REB) as Total_Rebounds,
        COUNT(DISTINCT GAME_ID) as Games_Played,
        AVG(REB) as Avg_Rebounds
    FROM game_stats
    GROUP BY PLAYER_NAME
    ORDER BY Total_Rebounds DESC
    """
    rebounding_df = pd.read_sql_query(rebounding_query, conn)
    
    rebounding_fig = px.bar(rebounding_df.head(10), 
                             x='PLAYER_NAME', 
                             y='Total_Rebounds',
                             hover_data=['Avg_Rebounds', 'Games_Played'],
                             title='Top 10 Celtics Players by Total Rebounds',
                             color_discrete_sequence=[CELTICS_GREEN])
    
    # Add annotation explaining the visualization
    rebounding_fig.add_annotation(
        text="This bar chart displays the top 10 Celtics players by total rebounds. " 
             "The height of each bar represents the total number of rebounds across all games.",
        xref="paper", yref="paper",
        x=0.5, y=-0.15,
        showarrow=False
    )
    
    rebounding_fig.update_layout(
        title_x=0.5, 
        template='plotly_white',
        plot_bgcolor=CELTICS_WHITE,
        paper_bgcolor=CELTICS_WHITE,
        height=800  # Increase height to accommodate annotation
    )
    pio.write_html(rebounding_fig, file=f'{output_dir}/player_rebounding_performance.html', auto_open=False)
    
    conn.close()
    print("Visualizations saved in data directory")

# Example usage
if __name__ == "__main__":
    visualize_player_performance()