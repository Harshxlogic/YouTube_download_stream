import os
import shutil
import subprocess
import yt_dlp

# Set MPV_PATH to your MPV executable if MPV is not in PATH.
# Windows example:
# MPV_PATH = r"C:\Program Files\mpv\mpv.exe"
# Linux/macOS: use "mpv" when installed through PATH.
MPV_PATH = os.environ.get("MPV_PATH", "mpv")


def find_mpv():
    """Return a usable MPV command/path."""
    if os.path.isfile(MPV_PATH):
        return MPV_PATH

    if shutil.which(MPV_PATH):
        return MPV_PATH

    raise FileNotFoundError(
        "MPV was not found. Install MPV or set the MPV_PATH environment variable."
    )


def search_videos(query, count=5):
    """Search YouTube and return lightweight result information."""
    options = {
        "quiet": True,
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            f"ytsearch{count}:{query}",
            download=False,
        )

    return info.get("entries", [])


def choose_result(results):
    """Display results and let the user choose one."""
    print("\nResults:\n")

    for i, video in enumerate(results, 1):
        print(f"{i}. {video.get('title', 'Unknown title')}")

    while True:
        try:
            choice = int(input("\nEnter song number: "))

            if 1 <= choice <= len(results):
                return results[choice - 1]

            print("Invalid choice.")

        except ValueError:
            print("Enter a number.")


def choose_mode():
    """Choose between download and stream."""
    print("\n1. Download")
    print("2. Stream")

    while True:
        mode = input("Choose: ").strip()

        if mode in ("1", "2"):
            return mode

        print("Choose 1 or 2.")


def choose_media_type():
    """Choose audio or video."""
    print("\n1. Audio")
    print("2. Video")

    while True:
        media_type = input("Choose: ").strip()

        if media_type in ("1", "2"):
            return media_type

        print("Choose 1 or 2.")


def stream_media(video, media_type):
    """Extract a playable stream and launch it with MPV."""
    mpv = find_mpv()

    format_selector = (
        "bestaudio/best"
        if media_type == "1"
        else "bestvideo+bestaudio/best"
    )

    options = {
        "quiet": False,
        "format": format_selector,
    }

    print("\nGetting stream...")

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            video["url"],
            download=False,
        )

    if media_type == "1":
        stream_url = info.get("url")

        if not stream_url:
            raise RuntimeError("No audio stream was found.")

        print("Starting audio stream...")

        subprocess.run(
            [mpv, "--no-video", stream_url],
            check=False,
        )

    else:
        # Prefer the URLs selected by yt-dlp when available.
        requested_formats = info.get("requested_formats")

        if requested_formats:
            video_url = None
            audio_url = None

            for fmt in requested_formats:
                if fmt.get("vcodec") != "none":
                    video_url = fmt.get("url")
                if fmt.get("acodec") != "none":
                    audio_url = fmt.get("url")

            if video_url and audio_url:
                print("Starting video stream...")

                subprocess.run(
                    [
                        mpv,
                        video_url,
                        "--audio-file=" + audio_url,
                    ],
                    check=False,
                )
                return

        stream_url = info.get("url")

        if not stream_url:
            raise RuntimeError("No video stream was found.")

        print("Starting video stream...")

        subprocess.run(
            [mpv, stream_url],
            check=False,
        )


def download_media(video, media_type):
    """Download selected media to the downloads directory."""
    os.makedirs("downloads", exist_ok=True)

    if media_type == "1":
        options = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
        }
    else:
        options = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
        }

    print("\nDownloading...")

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video["url"]])

    print("\nDownload complete!")


def main():
    print("=" * 50)
    print("YouTube Media Player & Downloader")
    print("=" * 50)

    query = input("\nEnter song/video name: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    try:
        results = search_videos(query)

        if not results:
            print("No results found.")
            return

        selected = choose_result(results)

        print(f"\nSelected: {selected.get('title', 'Unknown title')}")

        mode = choose_mode()
        media_type = choose_media_type()

        if mode == "2":
            stream_media(selected, media_type)
        else:
            download_media(selected, media_type)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
