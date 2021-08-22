from typing import Dict
import os

# Youtube Data API Key.
# Quota is 10.000 operation units per day.
# All requests we use only require 1 operational unit.
api_key: str = "..."

# Directory where logs are kept.
# Structure:
# Channel Name 1
#   Video Id 1
#   Video Id 2
#   ..
# Channel Name 2
#   Video Id 3
#   ..
out_dir: str = os.path.join(os.path.dirname(__file__), "./data")
channels_dir: str = os.path.join(out_dir, "channels")
excel_file: str = os.path.join(out_dir, "videos.xlsx")
bad_videos_file = os.path.join(out_dir, "bad_videos.txt")

track_time_days: int = 7


# IDs of playlists to watch for new uploads.
# Obtain by listing contentDetails of channel.
# See https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel
playlists: Dict[str, str] = {
    "Dr. Julian Hosp": "UUseNUrq7mUUWqTspr4QJ9eg",
    "Sheldon Evans": "UUZ3fejCy_P5xhv9QF-V6-YA",
}