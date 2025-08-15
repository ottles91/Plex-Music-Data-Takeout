# Plex Music Data Takeout

_A Python script to **export your Plex music library** into CSV or Excel files for analysis or backup._

## Features

- Reads your Plex **SQLite database** (com.plexapp.plugins.library.db) safely.
- Exports **all music tracks** with details including:
  -Track Title
  -Album
  -Artist
  -Release date
  -Duration
  -GUID
  -Added timestamp
- Optionally outputs to **Excel (.xlsx)** in addition to CSV.
- Makes a **safe copy** of your Plex database before querying, so the live server is unaffected

## Requirements

- Python 3.12+
- Pandas (option, used for Excel export):

```bash
pip install pandas openpyxl
```

## Setup & Usage

1. Clone this repository

```bash
git clone https://github.com/ottles91/Plex-Music-Data-Takeout
```

2. Open the script and update the plex_db_path variable to point to your plex database. Please note that there are two variables, one for macOS, and one for Windows. Update the correct one based on your operating system and make sure the other is commented out with a `#` character

```python
plex_db_path = Path.home() / "Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db"
```

3. Run the script:

```bash
python plex_music_export.py
```

4. CSV and Excel files will be generated in the same folder as the script (default names: `plex_music_library.csv` and `plex_music_library.xlsx`).

## NOTES

- It is best to temporarily stop your Plex server temporarily to prevent any issues. Alternatively, create a copy of the server database and have the script read from the copied file
