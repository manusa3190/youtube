import yt_dlp

OUTPUT_DIR = "downloads"


def download_mp3(url: str, start_time: str = None, stop_time: str = None):
    output_paths = []
    ydl_opts = {
        "js_runtimes": {"node": {}},
        "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["android"]}},
        "post_hooks": [output_paths.append],
        "format": "bestaudio/best",
        "outtmpl": f"{OUTPUT_DIR}/%(title)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    # 時間指定がある場合はffmpegの引数を追加
    if start_time or stop_time:
        postprocessor_args = []
        if start_time:
            postprocessor_args.extend(["-ss", start_time])
        if stop_time:
            postprocessor_args.extend(["-to", stop_time])

        ydl_opts["postprocessor_args"] = {"ffmpeg": postprocessor_args}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return output_paths[-1]


def download_mp4(url: str, start_time: str = None, stop_time: str = None):
    output_paths = []
    ydl_opts = {
        "js_runtimes": {"node": {}},
        "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["android"]}},
        "post_hooks": [output_paths.append],
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": f"{OUTPUT_DIR}/%(title)s.mp4",
    }

    # 時間指定がある場合はffmpegの引数を追加
    if start_time or stop_time:
        postprocessor_args = []
        if start_time:
            postprocessor_args.extend(["-ss", start_time])
        if stop_time:
            postprocessor_args.extend(["-to", stop_time])

        ydl_opts["postprocessor_args"] = {"ffmpeg": postprocessor_args}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return output_paths[-1]
