import numpy as np
import cv2

# Set preview resolution
h = 800
v = 600

# Set scale factor to resize frames
scale_factor = 0.5  # You can adjust this value based on your preference

# Set up cameras
caps = []
for i in range(4):
    cap = cv2.VideoCapture(i)
    cap.set(3, h)
    cap.set(4, v)
    cap.set(10, 0.5)

    # Test for each camera
    if not cap.isOpened():
        print(f'Camera {i} not found')
    else:
        print(f'Camera {i} found')
        caps.append(cap)

while True:
    frames = []
    for cap in caps:
        ret, frame = cap.read()

        if ret:
            # Resize each frame with the specified scale factor
            frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

            frames.append(frame)

    combined_frame = np.hstack(frames)

    cv2.imshow('Combined View', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
for cap in caps:
    cap.release()

cv2.destroyAllWindows()