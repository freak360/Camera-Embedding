import ctypes
from ctypes import POINTER, Structure, c_uint16, c_int
import cv2
import datetime
import os
import numpy as np

# Define the VzFormat data structure
class VzFormat(Structure):
    _fields_ = [
        ("width", c_uint16),
        ("height", c_uint16),
        ("framerate", c_uint16),
        ("format", c_uint16)  # Adjust format code accordingly
    ]

# Load the VizionSDK DLL
vizion_sdk = ctypes.WinDLL('C:\\Users\\Falcon\\Downloads\\Projects\\Falcon Projects\\Camera Embedding\\VizionSDK.dll')

# Set up function prototypes
vizion_sdk.VcCreateVizionCamDevice.restype = POINTER(VzFormat)
vizion_sdk.VcOpen.restype = c_int
vizion_sdk.VcOpen.argtypes = [POINTER(VzFormat), c_int]
vizion_sdk.VcSetCaptureFormat.restype = c_int
vizion_sdk.VcSetCaptureFormat.argtypes = [POINTER(VzFormat), VzFormat]
vizion_sdk.VcClose.restype = c_int
vizion_sdk.VcClose.argtypes = [POINTER(VzFormat)]



# Function to simulate capture frame from SDK (this function is hypothetical)
def capture_frame(camera):
    # This function should interface with the SDK to capture a frame
    # For now, we simulate with a dummy numpy array
    return np.random.randint(0, 256, (camera.contents.height, camera.contents.width, 3), dtype=np.uint8)



def main():
    video_directory = "recorded_videos"
    os.makedirs(video_directory, exist_ok=True)

    camera = vizion_sdk.VcCreateVizionCamDevice()
    if not camera:
        print("Failed to create camera device")
        return

    # Add a check to ensure the camera is properly initialized
    if not camera.contents:
        print("Camera initialization failed, camera.contents is NULL")
        return

    if vizion_sdk.VcOpen(camera.contents, 0) != 0:
        print("Failed to open camera")
        return

    desired_format = VzFormat(width=3840, height=2160, framerate=30, format=1)
    if vizion_sdk.VcSetCaptureFormat(camera.contents, desired_format) != 0:
        print("Failed to set capture format")
        vizion_sdk.VcClose(camera.contents)
        return

    # Setup video writer using OpenCV
    filename = f"{video_directory}/{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.avi"
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(filename, fourcc, 30, (3840, 2160))

    print("Recording started...")
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < 5:
        frame = capture_frame(camera)
        out.write(frame)
    out.release()

    print(f"Recording stopped. Video saved as: {filename}")
    vizion_sdk.VcClose(camera.contents)
    print("Camera closed successfully")

if __name__ == "__main__":
    main()

