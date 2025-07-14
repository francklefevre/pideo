# Pideo: Automatic Video Player for Raspberry Pi
A Python application that turns a Raspberry Pi into an unattended video player. It selects videos from a designated directory (either randomly or via a playlist file), plays them on HDMI output, and can optionally publish playback events over MQTT.

## Features
- Random video selection from a `videos/` directory when no playlist is provided.
- Ordered playback based on `playlist.json` with optional looping.
- MQTT notifications on video start (video name and duration).
- Automatic error logging and recovery.
- Systemd service template for running on startup.

# Requirements
The following packages are required on the Raspberry Pi OS (or other Debian-based distributions). Replace with equivalent packages for your distribution if necessary.

* Python ≥ 3.6
* `ffmpeg` (provides *ffprobe* used to fetch video duration)
* A video player. The default command shipped in *param.json* uses `ffmpeg`, but you may switch to `omxplayer`, `vlc`, etc.
* `paho-mqtt` **(only if you want MQTT notifications)** – install via:

  ```bash
  # For system-wide install (Debian/Ubuntu/Raspberry Pi OS ≥ bookworm)
  pip3 install --break-system-packages paho-mqtt

  # or inside a virtual environment (recommended)
  python3 -m venv .venv
  source .venv/bin/activate
  pip install paho-mqtt
  ```

If the package is missing the script will continue to play videos, but MQTT notifications will be disabled and a warning will be logged.

## Installation
Clone this repository and install dependencies:
```bash
git clone <repository_url> pideo
cd pideo
sudo apt update
sudo apt install -y omxplayer ffmpeg python3-pip
pip3 install paho-mqtt
```

## Configuration
Copy and customize configuration examples:
```bash
cp param.json.example param.json
cp secret.json.example secret.json
```

Edit **param.json** (non-confidential parameters):
```json
{
  "mqtt_server": "mqtt.example.com",
  "mqtt_port": 1883,
  "mqtt_topic": "pideo/playback",
  "videos_dir": "videos",
  # Command template to use for playback. '{video_path}' will be replaced by the actual file path.
  "player_cmd": "ffmpeg -re -i '{video_path}' -f null -"
}
```

Edit **secret.json** (confidential parameters):
```json
{
  "mqtt_username": "your_user",
  "mqtt_password": "your_pass"
}
```

Place videos in the `videos/` directory. To define playback order, create `videos/playlist.json`:
```json
{
  "videos": ["intro.mp4", "ad.mp4", "demo.mkv"],
  "loop": true
}
```

## Usage
```bash
python3 pideo.py
```

## Systemd Service Setup
Install and enable the service to run on boot:
```bash
sudo cp pideo.service /etc/systemd/system/pideo.service
sudo systemctl daemon-reload
# Make the Pi boot to the console only (no graphical desktop)
sudo systemctl set-default multi-user.target
sudo systemctl enable pideo.service
sudo systemctl start pideo.service
```
Edit `/etc/systemd/system/pideo.service` to adjust paths if needed.

The provided service file explicitly `Conflicts=graphical.target`, ensuring that when the service is running the X-Window desktop will not start. Disabling the desktop frees GPU memory and CPU cycles for video playback.

## Logging and Error Handling
- Errors and exceptions are logged to `pideo.py.err.txt` (overwritten at each start).

## Development
Contributions are welcome. See **AGENTS_METHODS.md** for methodologies.
