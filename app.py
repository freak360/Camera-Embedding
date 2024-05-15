import cv2
import datetime
import os
import time

video_directory = "recorded_videos"
os.makedirs(video_directory, exist_ok=True)

def initialize_camera():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # '0' for webcam and '1' for external cam
    if not cap.isOpened():
        print("Error: Could not open camera")
        return None

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    cap.set(cv2.CAP_PROP_FPS, 30)

    print("Configured camera settings:")
    print("Resolution: {}x{}".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("FPS set to: {}".format(cap.get(cv2.CAP_PROP_FPS)))

    return cap

def record_video(camera):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    now = datetime.datetime.now()
    filename = f"{video_directory}/{now.strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]}.avi"
    out = cv2.VideoWriter(filename, fourcc, 30, (3840, 2160), True)

    if camera is None:
        return

    print("Recording started. Press 'q' to stop.")
    start_time = time.time()
    frame_count = 0

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Can't receive frame. Exiting ...")
                break
            out.write(frame)
            cv2.imshow('Frame', frame)
            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        elapsed_time = time.time() - start_time
        actual_fps = frame_count / elapsed_time
        print("Elapsed time: {:.2f} seconds, Frame count: {}, Actual FPS: {:.2f}".format(elapsed_time, frame_count, actual_fps))
        out.release()
        camera.release()
        cv2.destroyAllWindows()
        print("Recording stopped. Video saved as:", filename)


def main():
    camera = initialize_camera()
    if camera:
        record_video(camera)


if __name__ == "__main__":
    main()
