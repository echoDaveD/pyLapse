import ffmpeg
import time
import os
import logging
import datetime
import cv2
import yaml

# Setup logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load config from YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

RTSP_URL = config["rtsp_url"]
INTERVAL = config["interval_minutes"] * 60
DURATION = config["duration_minutes"] * 60
OUTPUT_DIR = config["output_dir"]
FPS = config.get("timelapse_fps", 10)
USE_UDP = config.get("use_udp", False)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_snapshot(output_path):
    """Use ffmpeg to pull one frame from RTSP stream"""
    try:
        input_kwargs = {"rtsp_transport": "udp"} if USE_UDP else {}
        (
            ffmpeg
            .input(RTSP_URL, **input_kwargs)
            .output(output_path, vframes=1)
            .overwrite_output()
            .run(quiet=True)
        )
        logger.info(f"Snapshot saved to {output_path}")
    except ffmpeg.Error as e:
        logger.error(f"Error capturing snapshot: {e.stderr.decode()}")

def create_timelapse(image_dir, output_file, fps):
    """Create a video from captured images"""
    images = sorted(
        [f for f in os.listdir(image_dir) if f.endswith(".jpg")],
        key=lambda x: os.path.getmtime(os.path.join(image_dir, x))
    )

    if not images:
        logger.warning("No images found for timelapse.")
        return

    first_frame = cv2.imread(os.path.join(image_dir, images[0]))
    height, width, _ = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for img in images:
        frame = cv2.imread(os.path.join(image_dir, img))
        out.write(frame)

    out.release()
    logger.info(f"Timelapse video saved to {output_file}")

# Main loop
start_time = time.time()
while (time.time() - start_time) < DURATION:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_file = os.path.join(OUTPUT_DIR, f"{timestamp}.jpg")
    get_snapshot(snapshot_file)
    time.sleep(INTERVAL)

# Generate timelapse
create_timelapse(OUTPUT_DIR, os.path.join(OUTPUT_DIR, "timelapse.mp4"), FPS)
