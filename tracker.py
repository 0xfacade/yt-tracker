from __future__ import annotations

import requests
import os
import time
from datetime import datetime
import pandas
import logging

from typing import List, Set, TypedDict

import config

num_requests: int = 0

class Views:
    timestamp: int
    count: int

    def __init__(self, timestamp: int, count: int):
        self.timestamp = timestamp
        self.count = count

    @staticmethod
    def parse(line: str):
        parts = line.split(",")
        timestamp = int(parts[0])
        count = int(parts[1])
        return Views(timestamp, count)


class Video:
    id: str
    name: str
    release_date: str
    views: list[Views]

    def __init__(self):
        self.id = ""
        self.name = ""
        self.release_date = ""
        self.views = []

    @staticmethod
    def parse(video_file: str) -> Video:
        video = Video()

        video.id = os.path.basename(video_file)
        with open(video_file) as f:
            video.name = f.readline().strip()
            video.release_date = f.readline().strip()

            video.views.clear()
            for line in f:
                if not line:
                    continue
                video.views.append(Views.parse(line))
        return video

    def write(self, video_file: str):
        self.views.sort(key=lambda views: views.timestamp)
        with open(video_file, "w") as f:
            f.write(f"{self.name}\n")
            f.write(f"{self.release_date}\n")
            for views in self.views:
                f.write(f"{views.timestamp},{views.count}\n")

    def should_continue_to_track(self):
        if not self.views:
            return True
        tracked_time_s = self.views[-1].timestamp - self.views[0].timestamp
        return tracked_time_s <= config.track_time_days * 24 * 60 * 60


class Channel:
    name: str
    playlist_id: str
    videos: List[Video]

    def __init__(self, name: str, playlist_id: str):
        self.name = name
        self.playlist_id = playlist_id
        self.videos = []

    def read_videos(self, channels_dir: str):
        channel_dir = os.path.join(channels_dir, self.name)

        if not os.path.isdir(channel_dir):
            os.makedirs(channel_dir, exist_ok=True)
            return

        for video_id in os.listdir(channel_dir):
            video_file = os.path.join(channel_dir, video_id)
            if not os.path.isfile(video_file):
                continue
            try:
                video = Video.parse(video_file)
                self.videos.append(video)
            except:
                logging.exception("Exception occured while parsing video from file " + video_file)
    
    def write_videos(self, channels_dir: str):
        channel_dir = os.path.join(channels_dir, self.name)
        os.makedirs(channel_dir, exist_ok=True)
        for video in self.videos:
            video_file = os.path.join(channel_dir, video.id)
            try:
                video.write(video_file)
            except:
                logging.exception("Exception occured while writing video to file " + video_file)


class DataframeRow(TypedDict):
    channel_name: str
    video_id: str
    video_name: str
    release_date: str
    timestamp: str
    view_count: int

def to_dataframe(channels: List[Channel]):
    rows: List[DataframeRow] = []

    for channel in channels:
        for video in channel.videos:
            for views in video.views:
                rows.append({
                    "channel_name": channel.name,
                    "video_id": video.id,
                    "video_name": video.name,
                    "release_date": video.release_date,
                    "timestamp": datetime.utcfromtimestamp(views.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    "view_count": views.count            
                })

    return pandas.DataFrame(rows)

def read_channels() -> List[Channel]:
    channels: List[Channel] = []
    channels_dir = os.path.join(config.out_dir, "channels")

    if not os.path.isdir(channels_dir):
        os.makedirs(channels_dir, exist_ok=True)

    for channel_name, playlist_id in config.playlists.items():
        channel = Channel(channel_name, playlist_id)
        channel.read_videos(channels_dir)
        channels.append(channel)
    return channels


def fetch_latest_video_ids(playlist_id: str) -> Set[str]:
    global num_requests
    num_requests += 1

    r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={ 
        "key": config.api_key,
        "part": "contentDetails",
        "playlistId": playlist_id
    })
    r.raise_for_status()

    body = r.json()
    newest_video_ids = set([item["contentDetails"]["videoId"] for item in body["items"]])

    return newest_video_ids

def fetch_video_details(video: Video) -> None:
    global num_requests
    num_requests += 1

    r = requests.get("https://www.googleapis.com/youtube/v3/videos", params={ 
        "key": config.api_key,
        "id": video.id,
        "part": "snippet"
    })
    r.raise_for_status()
    
    response = r.json()
    video.name = response["items"][0]["snippet"]["title"]
    video.release_date = response["items"][0]["snippet"]["publishedAt"]


def discover_new_videos(channel: Channel):
    try:
        newest_video_ids = fetch_latest_video_ids(channel.playlist_id)
        already_tracked_ids = set(v.id for v in channel.videos)
        new_ids = newest_video_ids - already_tracked_ids

        for new_id in new_ids:
            try:
                video = Video()
                video.id = new_id
                fetch_video_details(video)
                channel.videos.append(video)
                logging.info("New video in channel " + channel.name + ": " + video.name)
            except:
                logging.exception("Could not fetch details for new video " + new_id + " of " + channel.name)
    except:
        logging.exception("Failed to fetch newest videos for " + channel.name)


def track_videos(channel: Channel, bad_videos: Set[str]) -> None:
    for video in channel.videos:
        if video.id in bad_videos:
            continue
        
        if not video.should_continue_to_track():
            continue

        try:
            global num_requests
            num_requests += 1

            r = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
                "key": config.api_key,
                "id": video.id,
                "part": "statistics"
            })
            r.raise_for_status()
            response = r.json()

            view_count = int(response["items"][0]["statistics"]["viewCount"])
            timestamp = int(time.time())

            video.views.append(Views(timestamp, view_count))
        except:
            logging.exception("Failed to retrieve view count for video " + video.id)
            bad_videos.add(video.id)


def read_bad_videos() -> Set[str]:
    if not os.path.exists(config.bad_videos_file):
        return set()

    with open(config.bad_videos_file) as f:
        return set(f.readlines())

def write_bad_videos(bad_videos: Set[str]) -> None:
    with open(config.bad_videos_file, "w") as f:
        for bad_video_id in bad_videos:
            f.write(f"{bad_video_id}\n")

def main():
    global num_requests
    num_requests = 0

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    logging.info("Tracker started.")
    logging.info("Reading in existing data.")
    channels = read_channels()

    bad_videos = read_bad_videos()

    logging.info("Updating channels.")
    for channel in channels:
        discover_new_videos(channel)
        track_videos(channel, bad_videos)
        channel.write_videos(config.channels_dir)

    write_bad_videos(bad_videos)
        
    logging.info(f"Made {num_requests} requests.")
    
    logging.info("Creating Excel sheet.")
    df = to_dataframe(channels)
    df.to_excel(config.excel_file, index=False)

    

if __name__ == "__main__":
    main()