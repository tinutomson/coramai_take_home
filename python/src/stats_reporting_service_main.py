import zmq
import time
import logging

SOCKET_ADDRESS = "tcp://127.0.0.1:5555"

def main() -> None:
    logging.basicConfig(format='%(message)s', level=logging.INFO)

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(SOCKET_ADDRESS)
    class_frequency = {}

    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            logging.info(f"In the past 10s:")
            for cl in class_frequency:
                logging.info(f"Class {cl} detected {class_frequency[cl]} times")
            start_time = time.time()
            class_frequency = {}
        try:
            # Receive message (assuming it's a JSON message)
            message = socket.recv_json()

            # Update class frequency
            if "class" in message:
                class_frequency[message["class"]] = class_frequency.get(message["class"], 0) + 1

        except zmq.error.ContextTerminated:
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            break

    # Close the socket and context when done
    socket.close()
    context.term()

if __name__ == "__main__":
    main()
