import cv2
import os
import argparse
from typing import Optional

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_file", type=str, required=True)
    parser.add_argument("--log_folder", type=str, required=True)
    return parser.parse_args()

def extract_frames(video_file: str, log_folder: str) -> None:
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print("Error opening video file")
        return

    fps: float = cap.get(cv2.CAP_PROP_FPS)
    total_frames: int = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    frame_interval: int = int(round(fps / 15))

    frame_count: int = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            log_file_path: str = os.path.join(log_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(log_file_path, frame)

        frame_count += 1

    cap.release()

    print(f"Frames extracted to {log_folder}")

def main() -> None:
    args = parse_args()
    extract_frames(args.video_file, args.log_folder)

if __name__ == "__main__":
    main()
