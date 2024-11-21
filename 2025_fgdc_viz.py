import streamlit as st
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Helper function to extract everything after the first word in a name
def get_last_name(full_name):
    return " ".join(full_name.split(" ")[1:]) if len(full_name.split(" ")) > 1 else full_name

# Baseball_Field class with summary box and dropdown functionality
class Baseball_Field:
    def __init__(self, figsize):
        self.figsize = figsize

    def __generate_baseball_field2D__(self, player_positions, relief_pitchers, starting_pitchers, dh_players, summary_text):
        names = ['Catcher', '1st Base', '2nd Base', '3rd Base', 'ShortStop',
                 'Left Fielder', 'Center Fielder', 'Right Fielder', 'Pitcher', 'DH']
        coord = [(0.1, 0.08), (0.43, 0.12), (0.5, 0.30), (0.11, 0.43), (0.35, 0.46),
                 (0.3, 0.8), (0.60, 0.60), (0.8, 0.3), (0.265, 0.265), (0.11, 0.615)]

        fig, ax = plt.subplots(1, figsize=self.figsize)

        # Draw the field
        ax.add_patch(patches.Rectangle((0.0, 0.0), 1, 1, facecolor="#247309", alpha=0.50))
        ax.add_patch(patches.Wedge((0.05, 0.05), 0.89, 360, 90, ec="none", facecolor="green"))
        ax.add_patch(patches.Wedge((0.1, 0.1), 0.52, 360, 90, ec="none", facecolor='white'))
        ax.add_patch(patches.Wedge((0.1, 0.1), 0.51, 360, 90, ec="none", facecolor='#66431d'))
        ax.add_patch(patches.Rectangle((0.1, 0.1), 0.32, 0.32, facecolor="white", ec="none"))
        ax.add_patch(patches.Rectangle((0.1, 0.1), 0.31, 0.31, facecolor="green", ec="none"))
        ax.add_patch(patches.Circle((0.1, 0.1), 0.056, ec="none", facecolor='white'))
        ax.add_patch(patches.Circle((0.1, 0.1), 0.05, ec="none", facecolor='#66431d'))
        ax.add_patch(patches.Rectangle((0.1, 0.1), 1.0, 0.01, facecolor="white", ec="none"))
        ax.add_patch(patches.Rectangle((0.1, 0.1), 0.01, 1, facecolor="white", ec="none"))
        ax.add_patch(patches.Circle((0.26, 0.26), 0.02, ec="none", facecolor='white'))

        # Add boxes for each position and display player names
        for position, (x, y) in zip(names, coord):
            if position == 'Pitcher':
                continue
            players = player_positions.get(position, []) if position != 'DH' else dh_players
            box_width, box_height = 0.2, 0.1
            ax.add_patch(Rectangle((x - box_width / 2, y - box_height / 2), box_width, box_height,
                                   edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=1))
            for idx, player in enumerate(players):
                fontweight = "bold" if idx == 0 else "normal"
                plt.text(x, y - 0.015 * idx, player, color="blue", fontsize=10, ha="center", va="center", fontweight=fontweight)

        # Add a summary box in the top-right corner
        summary_x, summary_y = 0.7, 0.7
        summary_width, summary_height = 0.25, 0.25
        ax.add_patch(Rectangle((summary_x, summary_y), summary_width, summary_height,
                               edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=2))
        for idx, line in enumerate(summary_text.split("\n")):
            fontweight = "bold" if line.startswith("2025 FGDC") or line.startswith("All Hitting:") or line.startswith("All Pitching:") else "normal"
            plt.text(summary_x + summary_width / 2, summary_y + summary_height - 0.03 - (idx * 0.05),
                     line, fontsize=10, color="black", ha="center", va="top", fontweight=fontweight)

        # DH box
        dh_x, dh_y = 0.11, 0.615
        box_width, box_height = 0.2, 0.1
        ax.add_patch(Rectangle((dh_x - box_width / 2, dh_y - box_height / 2), box_width, box_height,
                               edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=1))
        plt.text(dh_x, dh_y + 0.025, "DH:", fontsize=12, color="black", ha="center", va="center")
        for idx, player in enumerate(dh_players):
            fontweight = "bold" if idx == 0 else "normal"
            plt.text(dh_x, dh_y - 0.015 * idx, player, color="blue", fontsize=10, ha="center", va="center", fontweight=fontweight)

        # Pen box
        pen_x_start, pen_y_start = 0.6, 0.0001
        pen_width, pen_height = 0.3, 0.2
        ax.add_patch(Rectangle((pen_x_start, pen_y_start), pen_width, pen_height,
                               edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=2))
        pen_text = "Pen:\n" + "\n".join(relief_pitchers)
        plt.text(pen_x_start + pen_width / 2, pen_y_start + pen_height / 2, pen_text,
                 fontsize=10, color="black", ha="center", va="center", wrap=True)

        # SP box
        sp_x, sp_y = 0.265, 0.265
        sp_width, sp_height = 0.2, 0.1
        ax.add_patch(Rectangle((sp_x - sp_width / 2, sp_y - sp_height / 2), sp_width, sp_height,
                               edgecolor="black", facecolor="lightgrey", alpha=0.9, lw=2))
        sp_text = "SP:\n" + "\n".join(starting_pitchers)
        plt.text(sp_x, sp_y, sp_text, fontsize=10, color="black", ha="center", va="center", wrap=True)

        plt.axis('off')
        return fig, ax

# Streamlit app
def plot_field_with_data(hitter_df, pitcher_df, team):
    hitter_df = hitter_df[hitter_df['Team'] == team]
    hitter_df['WAR'] = pd.to_numeric(hitter_df['WAR'], errors='coerce')
    hitter_df['PA'] = pd.to_numeric(hitter_df['PA'], errors='coerce')
    pitcher_df = pitcher_df[pitcher_df['Team'] == team]
    pitcher_df['WAR'] = pd.to_numeric(pitcher_df['WAR'], errors='coerce')

    summary_text = prepare_summary_text(hitter_df, pitcher_df, team)

    obj = Baseball_Field((14, 14))
    fig, ax = obj.__generate_baseball_field2D__(field_positions, relief_pitchers, starting_pitchers, dh_players, summary_text)
    st.pyplot(fig)

# Main Streamlit app
hitter_file_path = "2025 FGDC Projections - All Hitters.csv"
pitcher_file_path = "2025 FGDC Projections - All Pitchers.csv"

hitter_df = pd.read_csv(hitter_file_path)
pitcher_df = pd.read_csv(pitcher_file_path)

st.title("2025 FGDC Baseball Visualization")
team = st.selectbox("Select a Team:", hitter_df['Team'].unique())

if st.button("Generate Field"):
    plot_field_with_data(hitter_df, pitcher_df, team)


