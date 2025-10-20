import sqlite3
import csv
import shutil
from pathlib import Path

# === CONFIG ===

# Change this to the path of your Plex database
# macOS path:
plex_db_path = Path.home() / "Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"

# Windows path (replace USERNAME):
# plex_db_path = Path(r"C:\Users\USERNAME\AppData\Local\Plex Media Server\Plug-in Support\Databases\com.plexapp.plugins.library.db")

output_csv = Path("plex_music_library.csv")
make_excel_too = False  # Set to False if you don't want Excel output

output_dir = Path("exports")
output_dir.mkdir(exist_ok=True)

# === SAFETY: make a copy so we don't touch the live DB ===
db_copy_path = Path("plex_library_copy.db")
shutil.copy2(plex_db_path, db_copy_path)

# === Connect to the DB copy ===
conn = sqlite3.connect(db_copy_path)
cursor = conn.cursor()

# === SQL query ===

# Music
# metadata_type 10 = track, 9 = album, 8 = artist
music_query = """
SELECT
    tracks.title AS track_title,
    albums.title AS album_title,
    artists.title AS artist_name,
    tracks.originally_available_at AS release_date,
    ROUND(tracks.duration / 1000.0, 2) AS duration_seconds,
    tracks.guid AS track_guid,
    tracks.added_at AS added_timestamp
FROM metadata_items AS tracks
LEFT JOIN metadata_items AS albums ON tracks.parent_id = albums.id
LEFT JOIN metadata_items AS artists ON albums.parent_id = artists.id
WHERE tracks.metadata_type = 10
ORDER BY artist_name, album_title, track_title
"""

# Movies
movies_query = """
SELECT
    movies.title AS movie_title,
    movies.original_title AS original_title,
    movies.originally_available_at AS release_date,
    movies.studio AS studio,
    ROUND(movies.duration / 1000.0 / 60, 1) AS duration_minutes,
    movies.guid AS movie_guid,
    movies.added_at AS added_timestamp
FROM metadata_items AS movies
WHERE movies.metadata_type = 1
  AND movies.library_section_id = 3  
ORDER BY movie_title
"""

# TV episodes
tv_query = """
SELECT
    shows.title AS show_title,
    seasons.title AS season_title,
    episodes.title AS episode_title,
    episodes."index" AS episode_number,
    episodes.originally_available_at AS air_date,
    ROUND(episodes.duration / 1000.0 / 60, 1) AS duration_minutes,
    episodes.guid AS episode_guid,
    episodes.added_at AS added_timestamp
FROM metadata_items AS episodes
LEFT JOIN metadata_items AS seasons ON episodes.parent_id = seasons.id
LEFT JOIN metadata_items AS shows ON seasons.parent_id = shows.id
WHERE episodes.metadata_type = 4
ORDER BY show_title, seasons."index", episodes."index"
"""

# === Helper to run query and write CSV ===
def export_query_to_csv(query, output_file, headers):
    cursor.execute(query)
    rows = cursor.fetchall()
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"✅ Exported: {output_file}")

# === Run exports ===
export_query_to_csv(
    music_query,
    output_dir / "plex_music_library.csv",
    ["Track", "Album", "Artist", "Release Date", "Duration (s)", "GUID", "Added Timestamp"]
)

export_query_to_csv(
    movies_query,
    output_dir / "plex_movies_library.csv",
    ["Movie Title", "Original Title", "Release Date", "Studio", "Duration (min)", "GUID", "Added Timestamp"]
)

export_query_to_csv(
    tv_query,
    output_dir / "plex_tv_library.csv",
    ["Show", "Season", "Episode", "Episode Number", "Air Date", "Duration (min)", "GUID", "Added Timestamp"]
)

# === Done ===
conn.close()
print(f"\nAll exports complete. Files saved in: {output_dir.resolve()}")





# cursor.execute(query)
# rows = cursor.fetchall()

# === Write to CSV ===
# with open(output_csv, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["Track", "Album", "Artist", "Release Date", "Duration (seconds)", "GUID", "Added Timestamp"])
#     writer.writerows(rows)

# print(f"CSV exported: {output_csv.resolve()}")

# # === Optional Excel output ===
# if make_excel_too:
#     try:
#         import pandas as pd
#         df = pd.DataFrame(rows, columns=["Track", "Album", "Artist", "Release Date", "Duration (seconds)", "GUID", "Added Timestamp"])
#         excel_path = output_csv.with_suffix(".xlsx")
#         df.to_excel(excel_path, index=False)
#         print(f"Excel exported: {excel_path.resolve()}")
#     except ImportError:
#         print("Pandas not installed, skipping Excel output. Install with: pip install pandas openpyxl")

# conn.close()