import cv2
import socket
import pickle
import struct
import zlib
import time

# Khởi tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.17.35.20'  # Điền IP của máy chủ (máy tính thứ nhất)
port = 9999
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

# Biến để đếm số khung hình trong một giây
fps_counter = 0
start_time = time.time()

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]

    try:
        msg_size = struct.unpack("Q", packed_msg_size)[0]
    except struct.error as e:
        print(f"Error unpacking message size: {e}")
        break

    while len(data) < msg_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    frame_data = data[:msg_size]
    data = data[msg_size:]

    try:
        frame_data = zlib.decompress(frame_data)  # Giải nén khung hình
        frame = pickle.loads(frame_data)
        fps_counter += 1
    except pickle.UnpicklingError as e:
        print(f"Error unpickling frame: {e}")
        break

    # Resize khung hình để phù hợp với kích thước màn hình của máy khách
    frame = cv2.resize(frame, (800, 600))

    # Hiển thị FPS bằng putText
    cv2.putText(img=frame, text=f'FPS: {fps_counter}', org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=(0, 0, 255), thickness=2)

    cv2.imshow("RECEIVING VIDEO", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    # Tính toán và hiển thị FPS mỗi giây
    elapsed_time = time.time() - start_time
    if elapsed_time >= 1.0:
        print("FPS:", fps_counter)
        fps_counter = 0
        start_time = time.time()

client_socket.close()
