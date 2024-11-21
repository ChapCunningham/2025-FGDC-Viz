import pandas as pd
import streamlit as st
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Helper function to extract everything after the first word in a name
def get_last_name(full_name):
    return " ".join(full_name.split(" ")[1:]) if len(full_name.split(" ")) > 1 else full_name

# Modified Baseball_Field class with adjusted Pen box and summary box
class Baseball_Field:
    def __init__(self, figsize):
        self.figsize = figsize

    def __generate_baseball_field2D__(self, player_positions, relief_pitchers, starting_pitchers, dh_players, summary_text):
        # Coordinates for player positions (excluding Home Plate)
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
            if position == 'Pitcher':  # Skip adding "Pitcher" as a position; replace with SP box
                continue
            players = player_positions.get(position, []) if position != 'DH' else dh_players
            box_width, box_height = 0.2, 0.1  # Define box size
            ax.add_patch(Rectangle((x - box_width / 2, y - box_height / 2), box_width, box_height,
                                   edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=1))
            
            # Plot player names
            for idx, player in enumerate(players):
                fontweight = "bold" if idx == 0 else "normal"
                plt.text(x, y - 0.015 * idx, player, color="blue", fontsize=10, ha="center", va="center", fontweight=fontweight)

        # Add a summary box in the top-right corner
        summary_x, summary_y = 0.7, 0.7  # Coordinates for the top-right corner
        summary_width, summary_height = 0.25, 0.25  # Box dimensions
        ax.add_patch(Rectangle((summary_x, summary_y), summary_width, summary_height,
                               edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=2))
        plt.text(summary_x + summary_width / 2, summary_y + summary_height - 0.03, summary_text,
                 fontsize=10, color="black", ha="center", va="top", wrap=True)

        # Add a box for the DH position
        dh_x, dh_y = 0.11, 0.615  # Coordinates for DH box
        box_width, box_height = 0.2, 0.1  # Define box size
        ax.add_patch(Rectangle((dh_x - box_width / 2, dh_y - box_height / 2), box_width, box_height,
                               edgecolor="black", facecolor="lightgrey", alpha=0.8, lw=1))
        plt.text(dh_x, dh_y + 0.025, "DH:", fontsize=10, color="black", ha="center", va="center")
        for idx, player in enumerate(dh_players):
            fontweight = "bold" if idx == 0 else "normal"
            plt.text(dh_x, dh_y - 0.015 * idx, player, color="blue", fontsize=10, ha="center", va="center", fontweight=fontweight)

        plt.axis('off')  # Remove axes for a clean look
        return fig, ax

# Updated function to calculate and prepare the summary text
def prepare_summary_text(hitter_df, pitcher_df, team):
    # WAR calculations for infield and outfield
    infield_positions = ["1B", "2B", "SS", "3B", "C"]
    outfield_positions = ["LF", "CF", "RF"]
    
    infield_war = hitter_df[hitter_df['Pos'].isin(infield_positions)]['WAR'].sum()
    outfield_war = hitter_df[hitter_df['Pos'].isin(outfield_positions)]['WAR'].sum()
    
    # Total hitting and pitching WAR
    all_hitting_war = hitter_df['WAR'].sum()
    all_pitching_war = pitcher_df['WAR'].sum()

    # WAR for SP and RP
    sp_war = pitcher_df[pitcher_df['Pos'] == 'SP']['WAR'].sum()
    rp_war = pitcher_df[pitcher_df['Pos'] == 'RP']['WAR'].sum()

    # Prepare the summary text
    summary_text = f"**2025 FGDC {team.upper()}**\n\n" + \
                   f"**All Hitting:** {all_hitting_war:.1f} fWAR\n" + \
                   f"Infield: {infield_war:.1f} fWAR\n" + \
                                      f"Outfield: {outfield_war:.1f} fWAR\n\n" + \
                   f"**All Pitching:** {all_pitching_war:.1f} fWAR\n" + \
                   f"SP: {sp_war:.1f} fWAR\n" + \
                   f"RP: {rp_war:.1f} fWAR"
    return summary_text


# Function to process and plot the field
def plot_field_with_data(hitter_df, pitcher_df, team):
    # Process hitters
    hitter_df = hitter_df[hitter_df['Team'] == team]
    hitter_df = hitter_df[hitter_df['Name'] != 'Total']
    hitter_df['WAR'] = pd.to_numeric(hitter_df['WAR'], errors='coerce')
    hitter_df['PA'] = pd.to_numeric(hitter_df['PA'], errors='coerce')
    total_war = hitter_df.groupby('Name')['WAR'].sum().reset_index().rename(columns={'WAR': 'Total_WAR'})
    hitter_df = pd.merge(hitter_df, total_war, on='Name')

    # Field positions
    field_positions = {key: [] for key in ['Catcher', '1st Base', '2nd Base', '3rd Base', 'ShortStop',
                                           'Left Fielder', 'Center Fielder', 'Right Fielder', 'Pitcher']}
    position_map = {"C": "Catcher", "1B": "1st Base", "2B": "2nd Base", "3B": "3rd Base",
                    "SS": "ShortStop", "LF": "Left Fielder", "CF": "Center Fielder",
                    "RF": "Right Fielder", "P": "Pitcher"}
    
    dh_players = []
    for pos in hitter_df['Pos'].unique():
        if pos in position_map:
            pos_df = hitter_df[(hitter_df['Pos'] == pos) & (hitter_df['PA'] >= 100)].sort_values(by='PA', ascending=False)
            for _, row in pos_df.iterrows():
                player_name = f"{get_last_name(row['Name'])} - {row['Total_WAR']:.1f} WAR"
                field_positions[position_map[pos]].append(player_name)
        elif pos == "DH":
            dh_df = hitter_df[(hitter_df['Pos'] == pos) & (hitter_df['PA'] >= 100)].sort_values(by='PA', ascending=False)
            for _, row in dh_df.iterrows():
                dh_players.append(f"{get_last_name(row['Name'])} - {row['Total_WAR']:.1f} WAR")

    # Process pitchers
    pitcher_df = pitcher_df[pitcher_df['Team'] == team]
    pitcher_df = pitcher_df[pitcher_df['Name'] != 'Total']
    pitcher_df['IP'] = pd.to_numeric(pitcher_df['IP'], errors='coerce')
    pitcher_df['WAR'] = pd.to_numeric(pitcher_df['WAR'], errors='coerce')

    # Top 5 SP and RP
    sp_df = pitcher_df[pitcher_df['Pos'] == 'SP']
    top_sp = sp_df.nlargest(5, 'IP')[['Name', 'WAR']]
    starting_pitchers = [f"{get_last_name(row['Name'])} - {row['WAR']:.1f} WAR" for _, row in top_sp.iterrows()]

    rp_df = pitcher_df[pitcher_df['Pos'] == 'RP']
    top_rp = rp_df.nlargest(10, 'IP')[['Name', 'WAR']]
    relief_pitchers = [f"{get_last_name(row['Name'])} - {row['WAR']:.1f} WAR" for _, row in top_rp.iterrows()]

    # Prepare the summary text
    summary_text = prepare_summary_text(hitter_df, pitcher_df, team)

    # Plot field
    obj = Baseball_Field((14, 14))
    fig, ax = obj.__generate_baseball_field2D__(field_positions, relief_pitchers, starting_pitchers, dh_players, summary_text)
    return fig


# Streamlit app
def main():
    st.title("2025 FGDC Baseball Field Visualizer")

    # Load the data
    hitter_file_path = "2025 FGDC Projections - All Hitters.csv"
    pitcher_file_path = "2025 FGDC Projections - All Pitchers.csv"

    hitter_df = pd.read_csv(hitter_file_path)
    pitchers_df = pd.read_csv(pitcher_file_path)

    # Get unique team names
    teams = hitter_df['Team'].unique()

    # Dropdown menu for team selection
    selected_team = st.selectbox("Select a Team", teams)

    # Generate the field visualization for the selected team
    if st.button("Generate Field"):
        fig = plot_field_with_data(hitter_df, pitcher_df, selected_team)
        st.pyplot(fig)

if __name__ == "__main__":
    main()

