import os
import cv2
import argparse
import numpy as np
import zmq
import time
import logging

from utils import classify_image

SOCKET_ADDRESS="tcp://127.0.0.1:5555"

def process_unprocessed_files(log_folder: str, context: zmq.Context) -> None:
    if not os.path.exists(log_folder):
        logging.error(f"Error: Log folder '{log_folder}' does not exist.")
        return

    socket = context.socket(zmq.PUSH)
    socket.connect(SOCKET_ADDRESS)

    files = os.listdir(log_folder)

    while True:
        start_time = time.time()
        processed_count = 0
        for file_name in files:
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:
                throughput = processed_count / elapsed_time
                logging.info(f"Throughput: {throughput:.2f} files/second")
                start_time = time.time()
                processed_count = 0

            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    file_path = os.path.join(log_folder, file_name)
                    img = cv2.imread(file_path)
                    img_resized = cv2.resize(img, (640, 360))
                    processed_img = np.array(img_resized, dtype=np.uint8)

                    result = classify_image(processed_img)

                    message = {'file_name': file_name, 'class': result}
                    socket.send_json(message)
                    processed_count += 1
                except Exception as e:
                    logging.error(f"Error: processing {file_name}")
                finally:    # No retries
                    try:
                        os.remove(file_path)
                    except:
                        pass

    # Close the socket
    socket.close()
    context.term()

def main() -> None:
    parser = argparse.ArgumentParser(description="Process unprocessed image files in a log folder.")
    parser.add_argument("--log_folder", required=True, type=str, help="Path to the log folder")
    args = parser.parse_args()

    context = zmq.Context()
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    process_unprocessed_files(args.log_folder, context)

if __name__ == "__main__":
    main()
