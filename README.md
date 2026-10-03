# YouTube Media Player & Downloader

A Python command-line media application that uses `yt-dlp` to search YouTube content and provides options to stream or download selected audio and video through the MPV media player.

## Features

- Search YouTube directly from the terminal
- Display the top 5 search results
- Interactive result selection
- Audio streaming through MPV
- Video streaming through MPV
- Audio downloading
- Video downloading with MP4 merging
- Automatic `downloads/` directory creation
- Input validation and exception handling
- Cross-platform MPV path configuration

## Technologies

- Python
- yt-dlp
- MPV
- subprocess
- CLI / terminal interface

## Project Structure

```text
youtube-media-player/
├── main.py
├── requirements.txt
├── README.md
└── downloads/
```

Downloaded files are saved inside `downloads/`.

## Requirements

- Python 3.9+
- MPV media player
- Internet connection
- `yt-dlp`

For video downloads, a working FFmpeg installation may also be required by the selected formats.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd youtube-media-player
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## MPV Configuration

The application first looks for MPV using the `MPV_PATH` environment variable and then falls back to the system PATH.

### Linux / Arch

If MPV is installed and available in PATH:

```bash
sudo pacman -S mpv
```

Then run:

```bash
python main.py
```

You can verify MPV with:

```bash
which mpv
```

### Windows

Install MPV and either add it to PATH or set:

```powershell
$env:MPV_PATH="C:\Program Files\mpv\mpv.exe"
```

Then:

```powershell
python main.py
```

## Usage

Run:

```bash
python main.py
```

The program asks for a search query:

```text
Enter song/video name: interstellar soundtrack
```

It displays search results:

```text
Results:

1. Interstellar - Main Theme
2. Interstellar Soundtrack
3. ...
```

Select a result:

```text
Enter song number: 1
```

Then choose:

```text
1. Download
2. Stream
```

Finally choose:

```text
1. Audio
2. Video
```

## Application Workflow

```text
User Search Query
       |
       v
YouTube Search via yt-dlp
       |
       v
Display Top 5 Results
       |
       v
User Selects Media
       |
       +-------------------+
       |                   |
       v                   v
    Stream              Download
       |                   |
       v                   v
Extract Stream         Select Format
       |                   |
       v                   v
      MPV              Save to downloads/
```

## Error Handling

The application handles common runtime problems such as:

- Empty search queries
- Invalid menu selections
- No search results
- Missing MPV installation
- Missing stream URLs
- Download failures
- Interrupted execution

## Resume-Relevant Skills

This project demonstrates:

- Python application development
- Third-party API/library integration
- Command-line interface design
- Media format selection
- Subprocess management
- File and directory handling
- Input validation
- Exception handling
- External application integration

## Notes

This project is intended for educational and personal use. Users are responsible for complying with applicable copyright laws and the terms of the services they access.

## Future Improvements

Possible extensions:

- Add a graphical user interface
- Add playlists and queue management
- Add configurable download quality
- Add progress bars
- Add logging
- Add configuration file support
- Add command-line arguments with `argparse`
- Add metadata and thumbnail handling
