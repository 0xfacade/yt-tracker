from typing import Dict
import os

# Youtube Data API Key.
# Quota is 10.000 operation units per day.
# All requests we use only require 1 operational unit.
api_key: str = "AIzaSyB0CpxuDWOmiZKRLKICbCn6JQ2N5jTOcZ0"

# Directory where logs are kept.
# Structure:
# Channel Name 1
#   Video Id 1
#   Video Id 2
#   ..
# Channel Name 2
#   Video Id 3
#   ..
out_dir: str = "/home/ocius/data"
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
    "The Moon": "UUc4Rz_T9Sb1w5rqqo9pL1Og",
    "Blocktrainer": "UUG6KtMc5WYB-ppxwpaX5CFw",
    "BitBoy Crypto": "UUjemQfjaXAzA-95RKoy9n_g",
    "JRNY Crypto": "UU188KLMYLLGqVJZdYq7mYFw",
    "Coin Bureau": "UUqK_GSMbpiV8spgD3ZGloSw",
    # MDX Crypto
    "Ivan on Tech": "UUrYmtJBtLdtm2ov84ulV-yg",
    "Crypto Banter": "UUN9Nj4tjXbVTLYWN0EKly_Q",
    "Data Dash": "UUCatR7nWbYrkVXdxXb4cGXw",
    "Altcoin Daily": "UUbLhGKVY-bJPcawebgtNfbw",
    "Aantonop": "UUJWCJCWOxBYSi5DhCieLOLQ",
    "Benjamin Cowen": "UURvqjQPSeaWn-uEx-w0XOIg",
    "Anthony Pompliano": "UUevXpeL8cNyAnww-NqJ4m2w",
    "EllioTrades Crypto": "UUMtJYS0PrtiUwlk6zjGDEMA",
    "Box Mining": "UUxODjeUwZHk3p-7TU-IsDOA",
    "Altcoin Buzz": "UUGyqEtcGQQtXyUwvcy7Gmyg",
    "Digital Asset News": "UUJgHxpqfhWEEjYH9cLXqhIQ",
    "Lark Davis": "UUl2oCaw8hdR_kbqyqd2klIA",
    "Crypto Zombie": "UUiUnrCUGCJTCC7KjuW493Ww",
    "The Modern Investor": "UU-5HLi3buMzdxjdTdic3Aig",
    "TheChartGuys": "UUnqZ2hx679DqRi6khRUNw2g",
    "Hashoshi": "UUQNHKsYDGlWefzv9MAaOJGA",
    "InvestAnswers": "UUlgJyzwGs-GyaNxUHcLZrkg",
    "Bob Loukas": "UU0zGwzu0zzCImC1BwPuWyXQ",
    "Finematics": "UUh1ob28ceGdqohUnR7vBACA",
    "Dave Levine": "UUT4X1qiEPR0gsZYfze6JOyA",
    "Crazy4crypto": "UUNHXoNsyoBGVOS0EJarawvw",
    "UpOnlytv": "UU_Jt1VYHZO4Kc4cJQP5utdw",
    "Bankless": "UUAl9Ld79qaZxp9JzEOwd3aA",
    "Unchained Podcast": "UUWiiMnsnw5Isc2PP1to9nNw",
    "What Bitcoin Did": "UUzrWKkFIRS0kjZf7x24GdGg",
    "Millennial Money": "UUPi6sb9M-Kj-j-PKptcUNJQ",
    "MMCrypto": "UUBkGMys0mYl3Myxh3CTsASA",
    "Daap University": "UUY0xL8V6NzzFcwzHCgB8orQ",
    "Colin Talks Crypto": "UUnqJ2HjWhm7MbhgFHLUENfQ",
    "Alexander Lorenzo": "UUHQv-nQ2caXVvtTFa8WOJRA",
    "denome": "UU2IyN5ZpCnMYhCYQELBZczg",
    "Tyler S": "UUgBQ6YsN4oUTjbAvIwCFLog",
    "CryptoRUs": "UUI7M65p3A-D3P4v5qW8POxQ",
    "Satoshi Stacker": "UUGDjpwZV-bU-sLSnhInCfKQ",
    "Crypto Daily": "UU67AEEecqFEc92nVvcqKdhA",
    "Crypto Kirby Trading": "UUOaew10hdmtfa0MinTjOBqg",
    "Louis Thomas": "UUpceefaJ9vs4RYUTsO9Y3FA",
    "Crypto Casey": "UUi7RBPfTtRkVchV6qO8PUzg",
    "Conquer the markets": "UUN2WmKUchJpIcS1MupY-BuA",
    "99Bitcoins": "UUQQ_fGcMDxlKre3SEqEWrLA",
    "CryptoBusy": "UUBLftV9ZsgTxoMZWPfIUKGw",
    "Token Metrics": "UUH9MOLQ_KUpZ_cw8uLGUisA",
    "Data Dash": "UUCatR7nWbYrkVXdxXb4cGXw",
    "Crypto Capital Venture": "UUnMku7J_UtwlcSfZlIuQ3Kw",
}