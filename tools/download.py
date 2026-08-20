import tempfile
from pathlib import Path

import yt_dlp


def _normalize_time(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _ffmpeg_trim_args(start_time: str | None, stop_time: str | None) -> list[str]:
    start_time = _normalize_time(start_time)
    stop_time = _normalize_time(stop_time)

    # UIの旧デフォルト「0:00」「0:00」は切り出しなしとして扱う
    if start_time in {"0:00", "0", "00:00"} and stop_time in {None, "0:00", "0", "00:00"}:
        return []

    args = []
    if start_time:
        args.extend(["-ss", start_time])
    if stop_time:
        args.extend(["-to", stop_time])
    return args


def download_mp3(url: str, start_time: str = None, stop_time: str = None):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_paths = []
        ydl_opts = {
            "js_runtimes": {"node": {}},
            "noplaylist": True,
            "extractor_args": {"youtube": {"player_client": ["android"]}},
            "post_hooks": [output_paths.append],
            "format": "bestaudio/best",
            "outtmpl": f"{temp_dir}/%(title)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        postprocessor_args = _ffmpeg_trim_args(start_time, stop_time)
        if postprocessor_args:
            ydl_opts["postprocessor_args"] = {"ffmpeg": postprocessor_args}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        output_path = Path(output_paths[-1])
        return output_path.read_bytes(), output_path.name


def download_mp4(url: str, start_time: str = None, stop_time: str = None):
    with tempfile.TemporaryDirectory() as temp_dir:
        output_paths = []
        ydl_opts = {
            "js_runtimes": {"node": {}},
            "noplaylist": True,
            "extractor_args": {"youtube": {"player_client": ["android"]}},
            "post_hooks": [output_paths.append],
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "outtmpl": f"{temp_dir}/%(title)s.mp4",
        }

        postprocessor_args = _ffmpeg_trim_args(start_time, stop_time)
        if postprocessor_args:
            ydl_opts["postprocessor_args"] = {"ffmpeg": postprocessor_args}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        output_path = Path(output_paths[-1])
        return output_path.read_bytes(), output_path.name
