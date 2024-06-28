# NovitecCameraAPIWinPy

``NovitecCameraAPIWinPy`` is a Python API for the Novitec Camera API in C++ (Windows only).

With ``NovitecCameraAPIWinPy``, you can:

- Control the camera
- Capture images

Documentation
-------------------
See [documentation](https://kkoma-dev.github.io/NovitecCameraAPIWinPy).

Quick Start
-------------------

```sh
pip install NovitecCameraAPIWinPy
```

```sh
import sys

from NovitecCameraAPIWinPy import NovitecCamera
import numpy as np
import cv2

cv2.namedWindow("image", flags=cv2.WINDOW_NORMAL)
cv2.resizeWindow(winname="image", width=512, height=270)

# Create an instance of the NovitecCamera class
novitec_camera = NovitecCamera()

# Discover available devices
novitec_camera.discover()

# Connect to the device using its serial number
serial_number = "S3XS0001"  # Example serial number
ret = novitec_camera.connect_by_serial_number(serial_number)
if ret.errCode != 0:
    print(f"Connection failed for the device with serial number {serial_number}: {ret.errMessage}")
    sys.exit()
else:
    print(f"Connection successful for the device with serial number {serial_number}")

# Start streaming
ret = novitec_camera.start()
if ret.errCode != 0:
    print(f"Failed to start streaming: {ret.errMessage}")
    sys.exit()

# Capture and display images in a loop until 'q' is pressed
while cv2.waitKey(1) & 0xFF != ord('q'):
    ret, image = novitec_camera.get_image()

    if ret.errCode == 0:
        try:
            if image.payloadType == 1:  # Raw image
                cv_img = np.frombuffer(image.data, dtype=np.uint8).reshape((image.height, image.width))
                cv_img_color = cv2.cvtColor(cv_img, cv2.COLOR_BayerBG2BGR)
                cv2.imshow("image", cv_img_color)
            elif image.payloadType == 5:  # JPEG image
                data_pointer = cast(image.data, POINTER(c_ubyte))
                jpeg_data = np.ctypeslib.as_array(data_pointer, shape=(image.dataSize,))
                cvimgColor = cv2.imdecode(jpeg_data, cv2.IMREAD_COLOR)
                if cvimgColor is not None:
                    cv2.imshow("image", cvimgColor)
                else:
                    print("Error: Could not decode the image.")
        except Exception as e:
            print(f"Exception occurred: {e}")

# Destroy all OpenCV windows
cv2.destroyAllWindows()

# Stop streaming
ret = novitec_camera.stop()
if ret.errCode != 0:
    print(f"Failed to stop streaming: {ret.errMessage}")

# Disconnect the camera
ret = novitec_camera.disconnect()
if ret.errCode != 0:
    print(f"Failed to disconnect the device: {ret.errMessage}")
else:
    print("Disconnected successfully")
```
