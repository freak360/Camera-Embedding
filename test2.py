import ctypes
from ctypes import Structure, POINTER, c_uint16, c_int, c_char_p
import datetime
import numpy as np
import os
import cv2

# Define the VzFormat structure as specified by the SDK
class VzFormat(Structure):
    _fields_ = [
        ("width", c_uint16),
        ("height", c_uint16),
        ("framerate", c_uint16),
        ("format", c_uint16)  # The actual format code for MJPG or others
    ]

# Load the VizionSDK
vizion_sdk = ctypes.WinDLL('C:\\Users\\Falcon\\Downloads\\Projects\\Falcon Projects\\Camera Embedding\\VizionSDK.dll')

# Define function prototypes according to the SDK documentation
vizion_sdk.VcCreateVizionCamDevice.restype = POINTER(VzFormat)
vizion_sdk.VcOpen.restype = c_int
vizion_sdk.VcOpen.argtypes = [POINTER(VzFormat), c_int]
vizion_sdk.VcClose.restype = c_int
vizion_sdk.VcClose.argtypes = [POINTER(VzFormat)]
vizion_sdk.VcSetCaptureFormat.restype = c_int
vizion_sdk.VcSetCaptureFormat.argtypes = [POINTER(VzFormat), VzFormat]
vizion_sdk.VcGetRawImageCapture.restype = c_int
vizion_sdk.VcGetRawImageCapture.argtypes = [POINTER(VzFormat), POINTER(c_char_p), POINTER(c_int), c_uint16]



def record_video():
    # Initialize camera
    camera = vizion_sdk.VcCreateVizionCamDevice()
    if not camera or vizion_sdk.VcOpen(camera.contents, 0) != 0:
        print("Failed to open camera")
        return

    # Set the camera capture format
    format = VzFormat(width=3840, height=2160, framerate=30, format=1)  # MJPG assumed to be '4'
    if vizion_sdk.VcSetCaptureFormat(camera.contents, format) != 0:
        print("Failed to set capture format")
        vizion_sdk.VcClose(camera.contents)
        return

    # Directory setup
    video_directory = "recorded_videos"
    os.makedirs(video_directory, exist_ok=True)
    filename = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.avi'
    filepath = os.path.join(video_directory, filename)
    out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'MJPG'), 30, (3840, 2160))

    print("Recording... Press 'q' to stop.")
    while True:
        raw_data = ctypes.create_string_buffer(format.width * format.height * 3)  # Adjust buffer size
        data_size = ctypes.c_int()
        if vizion_sdk.VcGetRawImageCapture(camera.contents, ctypes.byref(raw_data), ctypes.byref(data_size), 2500) == 0:
            # Convert raw_data to a format suitable for display and recording
            # This part is illustrative and may require actual image processing depending on raw data format
            frame = np.frombuffer(raw_data.raw, dtype=np.uint8).reshape((format.height, format.width, 3))
            out.write(frame)
            cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()
    vizion_sdk.VcClose(camera.contents)
    print(f"Recording stopped. Video saved as {filename}")

if __name__ == "__main__":
    record_video()
