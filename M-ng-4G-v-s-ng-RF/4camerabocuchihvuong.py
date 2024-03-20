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

    # Combine frames into a diamond layout
    if len(frames) == 4:
        # Define the dimensions of the combined frame
        combined_width = max(frame.shape[1] for frame in frames) * 2
        combined_height = max(frame.shape[0] for frame in frames) * 2

        combined_frame = np.zeros((combined_height, combined_width, 3), dtype=np.uint8)

        # Place each frame in the diamond layout
        combined_frame[0:frames[0].shape[0], 0:frames[0].shape[1]] = frames[0]  # Top-left
        combined_frame[0:frames[1].shape[0], combined_width // 2:combined_width // 2 + frames[1].shape[1]] = frames[1]  # Top-right
        combined_frame[combined_height // 2:combined_height // 2 + frames[2].shape[0], 0:frames[2].shape[1]] = frames[2]  # Bottom-left
        combined_frame[combined_height // 2:combined_height // 2 + frames[3].shape[0], combined_width // 2:combined_width // 2 + frames[3].shape[1]] = frames[3]  # Bottom-right

        cv2.imshow('Combined View', combined_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
for cap in caps:
    cap.release()

cv2.destroyAllWindows()