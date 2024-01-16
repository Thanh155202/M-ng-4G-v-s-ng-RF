import cv2
import socket
import pickle
import struct
import zlib
import threading

# Khởi tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_ip = '172.20.10.3'  # Điền IP của máy chủ (máy tính thứ nhất)
port = 9999

# Hàm xử lý việc nhận dữ liệu
def receive_video():
    while True:
        data, addr = client_socket.recvfrom(64 * 1024)  # Tăng kích thước bộ nhớ đệm
        payload_size = struct.calcsize("Q")
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]

        try:
            msg_size = struct.unpack("Q", packed_msg_size)[0]
        except struct.error as e:
            print(f"Error unpacking message size: {e}")
            break

        while len(data) < msg_size:
            packet = client_socket.recvfrom(64 * 1024)  # Tăng kích thước bộ nhớ đệm
            data += packet[0]

        frame_data = data[:msg_size]
        data = data[msg_size:]

        try:
            frame_data = zlib.decompress(frame_data)  # Giải nén khung hình
            frame = pickle.loads(frame_data)
        except pickle.UnpicklingError as e:
            print(f"Error unpickling frame: {e}")
            break

        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

# Tạo một luồng mới cho việc nhận dữ liệu
receive_thread = threading.Thread(target=receive_video)
receive_thread.start()

# Main thread chờ nhận dữ liệu
while True:
    pass
