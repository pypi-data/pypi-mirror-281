from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass

from xiaomusic.utils import validate_proxy

LATEST_ASK_API = "https://userprofile.mina.mi.com/device_profile/v2/conversation?source=dialogu&hardware={hardware}&timestamp={timestamp}&limit=2"
COOKIE_TEMPLATE = "deviceId={device_id}; serviceToken={service_token}; userId={user_id}"

KEY_WORD_DICT = {
    "播放歌曲": "play",
    "放歌曲": "play",
    "下一首": "play_next",
    "单曲循环": "set_play_type_one",
    "全部循环": "set_play_type_all",
    "随机播放": "random_play",
    "关机": "stop",
    "停止播放": "stop",
    "分钟后关机": "stop_after_minute",
    "播放列表": "play_music_list",
    "刷新列表": "gen_music_list",
    "set_volume#": "set_volume",
    "get_volume#": "get_volume",
}

# 命令参数在前面
KEY_WORD_ARG_BEFORE_DICT = {
    "分钟后关机": True,
}

# 匹配优先级
KEY_MATCH_ORDER = [
    "set_volume#",
    "get_volume#",
    "分钟后关机",
    "播放歌曲",
    "放歌曲",
    "下一首",
    "单曲循环",
    "全部循环",
    "随机播放",
    "关机",
    "停止播放",
    "刷新列表",
    "播放列表",
]

SUPPORT_MUSIC_TYPE = [
    ".mp3",
    ".flac",
    ".wav",
    ".ape",
]


@dataclass
class Config:
    hardware: str = os.getenv("MI_HARDWARE", "L07A")
    account: str = os.getenv("MI_USER", "")
    password: str = os.getenv("MI_PASS", "")
    mi_did: str = os.getenv("MI_DID", "")
    cookie: str = ""
    verbose: bool = os.getenv("XIAOMUSIC_VERBOSE", "").lower() == "true"
    music_path: str = os.getenv("XIAOMUSIC_MUSIC_PATH", "music")
    conf_path: str = os.getenv("XIAOMUSIC_CONF_PATH", None)
    hostname: str = os.getenv("XIAOMUSIC_HOSTNAME", "192.168.2.5")
    port: int = int(os.getenv("XIAOMUSIC_PORT", "8090"))
    proxy: str | None = os.getenv("XIAOMUSIC_PROXY", None)
    search_prefix: str = os.getenv(
        "XIAOMUSIC_SEARCH", "ytsearch:"
    )  # "bilisearch:" or "ytsearch:"
    ffmpeg_location: str = os.getenv("XIAOMUSIC_FFMPEG_LOCATION", "./ffmpeg/bin")
    active_cmd: str = os.getenv("XIAOMUSIC_ACTIVE_CMD", "play,random_play")
    exclude_dirs: str = os.getenv("XIAOMUSIC_EXCLUDE_DIRS", "@eaDir")
    music_path_depth: int = int(os.getenv("XIAOMUSIC_MUSIC_PATH_DEPTH", "10"))
    disable_httpauth: bool = (
        os.getenv("XIAOMUSIC_DISABLE_HTTPAUTH", "true").lower() == "true"
    )
    httpauth_username: str = os.getenv("XIAOMUSIC_HTTPAUTH_USERNAME", "admin")
    httpauth_password: str = os.getenv("XIAOMUSIC_HTTPAUTH_PASSWORD", "admin")
    music_list_url: str = os.getenv("XIAOMUSIC_MUSIC_LIST_URL", "")
    music_list_json: str = os.getenv("XIAOMUSIC_MUSIC_LIST_JSON", "")

    def __post_init__(self) -> None:
        if self.proxy:
            validate_proxy(self.proxy)

    @classmethod
    def from_options(cls, options: argparse.Namespace) -> Config:
        config = {}
        if options.config:
            config = cls.read_from_file(options.config)
        for key, value in vars(options).items():
            if value is not None and key in cls.__dataclass_fields__:
                config[key] = value
        return cls(**config)

    @classmethod
    def read_from_file(cls, config_path: str) -> dict:
        result = {}
        with open(config_path, "rb") as f:
            config = json.load(f)
            for key, value in config.items():
                if value is not None and key in cls.__dataclass_fields__:
                    result[key] = value
        return result
