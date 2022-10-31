import os
import json
import dateutil.parser
import re
import pandas as pd
import csv

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
DATA_DIRECTORY = os.fsencode("./data/")
FILENAME_REGEX = re.compile(r"endsong_\d+\.json")

def main():
    data = {
        "artist": [],
        "title": [],
        "album": [],
        "timestamp": [],
        "album_artist": [],
        "duration": [],
        "filename": [],
    }
    filenames = list(filter(FILENAME_REGEX.match, map(os.fsdecode, os.listdir(DATA_DIRECTORY))))
    for filename in filenames:
        with open(f"./data/{filename}", "r") as file:
            plays = json.load(file)
            for play in plays:
                stopped_at = dateutil.parser.isoparse(play["ts"]).strftime(TIMESTAMP_FORMAT)
                duration = int(play["ms_played"]) / 1000
                if duration < 30:
                    continue
                duration = round(duration)
                data["artist"].append(play["master_metadata_album_artist_name"])
                data["title"].append(play["master_metadata_track_name"])
                data["album"].append(play["master_metadata_album_album_name"])
                data["timestamp"].append(stopped_at)
                data["album_artist"].append(play["master_metadata_album_artist_name"])
                data["duration"].append(duration)
                data["filename"].append(filename)
    df = pd.DataFrame(data=data)
    df = df.sort_values(by="timestamp")
    df.to_csv("./data/plays.csv", columns=["artist", "title", "album", "timestamp", "album_artist", "duration"], quoting=csv.QUOTE_ALL, index=False)


if __name__ == "__main__":
    main()
