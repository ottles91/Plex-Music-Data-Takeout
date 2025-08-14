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
make_excel_too = True  # Set to False if you don't want Excel output

# === SAFETY: make a copy so we don't touch the live DB ===
db_copy_path = Path("plex_library_copy.db")
shutil.copy2(plex_db_path, db_copy_path)

# === Connect to the DB copy ===
conn = sqlite3.connect(db_copy_path)
cursor = conn.cursor()

# === SQL query ===
# metadata_type 10 = track, 9 = album, 8 = artist
query = """
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

cursor.execute(query)
rows = cursor.fetchall()

# === Write to CSV ===
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Track", "Album", "Artist", "Release Date", "Duration (seconds)", "GUID", "Added Timestamp"])
    writer.writerows(rows)

print(f"CSV exported: {output_csv.resolve()}")

# === Optional Excel output ===
if make_excel_too:
    try:
        import pandas as pd
        df = pd.DataFrame(rows, columns=["Track", "Album", "Artist", "Release Date", "Duration (seconds)", "GUID", "Added Timestamp"])
        excel_path = output_csv.with_suffix(".xlsx")
        df.to_excel(excel_path, index=False)
        print(f"Excel exported: {excel_path.resolve()}")
    except ImportError:
        print("Pandas not installed, skipping Excel output. Install with: pip install pandas openpyxl")

conn.close()