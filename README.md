# 📷 pyLapse – RTSP Snapshot to Timelapse

A Python tool that captures periodic snapshots from an RTSP stream (e.g. IP camera), saves them with a timestamp, and optionally builds a timelapse video.

---

## 🛠 Features

- 🎥 Capture snapshots from RTSP streams using `ffmpeg`
- ⏱️ Configurable capture interval and total duration via a YAML config file
- 🗂️ Automatically creates snapshot output directories if they don’t exist
- 🎞️ Builds a timelapse video at the end with configurable frame rate
- 📓 Logs all actions using Python's `logging` module

---

## 📦 Requirements

- **Python 3.8 or later**
- **ffmpeg** must be installed and available in your system's PATH

---

## 🐍 Setup (Windows & Linux)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pyLapse.git
cd pyLapse
```

### 2. Create a virtual environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3.  Install dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

Create a configuration file named config.yaml in the project root:
```yaml
rtsp_url: "rtsp://your-camera-url"
interval_seconds: 60       # Time between snapshots
duration_minutes: 30       # Total run time
output_dir: "snapshots"    # Where to save images
timelapse:
  enabled: true
  fps: 24                  # Frames per second for the output video
  output_file: "timelapse.mp4"
```

## ▶️ Run the script
```bash
python capture_timelapse_images.py
```

## 🧪 Optional: Systemd service (Linux only)

You can configure this script to run automatically using a systemd service.

Create a file like /etc/systemd/system/pylapse.service:

```ini
[Unit]
Description=pyLapse RTSP Timelapse Capture
After=network.target

[Service]
Type = simple
WorkingDirectory=/path/to/pyLapse
ExecStart=/path/to/venv/bin/python capture_timelapse_images.py
Restart=on-failure
SyslogIdentifier=ehsSentinel
RestartSec=5
TimeoutStartSec=infinity


[Install]
WantedBy=multi-user.target
```

Then enable and start it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pylapse.service
sudo systemctl start pylapse.service
```

## ❗ ffmpeg installation
### Windows
Download from: https://ffmpeg.org/download.html
Unzip it and add the bin/ folder to your system PATH.

### Linux (Debian/Ubuntu):
```bash
sudo apt update && sudo apt install ffmpeg
```

## 📁 Output
Captured images will be saved to the configured output_dir, timestamped.
If timelapse is enabled, a video will be generated at the end using the captured frames.