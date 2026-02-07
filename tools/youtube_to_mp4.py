import yt_dlp
import sys
import argparse

def download_video(url: str, output_format: str = "mp4", start_time: str = None, stop_time: str = None):
    if output_format == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:  # mp4
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
        }

    # 時間指定がある場合はffmpegの引数を追加
    if start_time or stop_time:
        postprocessor_args = []
        if start_time:
            postprocessor_args.extend(["-ss", start_time])
        if stop_time:
            postprocessor_args.extend(["-to", stop_time])
        
        ydl_opts["postprocessor_args"] = {
            "ffmpeg": postprocessor_args
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTubeの動画をダウンロード")
    parser.add_argument("url", help="YouTubeのURL")
    parser.add_argument("--format", choices=["mp4", "mp3"], default="mp4", help="出力形式 (デフォルト: mp4)")
    parser.add_argument("--start", help="開始時間 (例: 0:05, 1:30)")
    parser.add_argument("--stop", help="終了時間 (例: 3:33, 5:00)")
    
    args = parser.parse_args()
    
    download_video(args.url, args.format, args.start, args.stop)