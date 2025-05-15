import os
import time
import yaml
import logging
import datetime
import ffmpeg
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("pyLapse")

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

rtsp_url = config["rtsp_url"]
interval = config.get("interval_seconds", 60)
duration_minutes = config.get("duration_minutes", 30)
output_dir = Path(config.get("output_dir", "snapshots"))
timelapse_config = config.get("timelapse", {})
timelapse_enabled = timelapse_config.get("enabled", False)
fps = timelapse_config.get("fps", 24)
timelapse_output = timelapse_config.get("output_file", "timelapse.mp4")

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Calculate number of snapshots
total_snapshots = int((duration_minutes * 60) / interval)

logger.info(f"Starting capture: {total_snapshots} snapshots every {interval} seconds")

def get_timestamped_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return output_dir / f"snapshot_{timestamp}.jpg"

def get_snapshot(filepath):
    try:
        (
            ffmpeg
            .input(rtsp_url, rtsp_transport='tcp', t=1)
            .output(str(filepath), vframes=1)
            .overwrite_output()
            .run(quiet=True)
        )
        logger.info(f"Captured snapshot: {filepath}")
    except ffmpeg.Error as e:
        logger.error(f"Failed to capture snapshot: {e.stderr.decode()}")

# Capture snapshots
for i in range(total_snapshots):
    filepath = get_timestamped_filename()
    get_snapshot(filepath)
    if i < total_snapshots - 1:
        time.sleep(interval)

# Create timelapse video
if timelapse_enabled:
    logger.info("Creating timelapse video...")
    try:
        (
            ffmpeg
            .input(str(output_dir / "snapshot_*.jpg"), pattern_type='glob', framerate=fps)
            .output(timelapse_output)
            .overwrite_output()
            .run(quiet=True)
        )
        logger.info(f"Timelapse video created: {timelapse_output}")
    except ffmpeg.Error as e:
        logger.error(f"Failed to create timelapse video: {e.stderr.decode()}")

logger.info("Done.")
