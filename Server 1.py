import cv2
import socket
import pickle
import struct
import imutils
import zlib
import threading

# Khởi tạo camera của máy tính thứ nhất
vid = cv2.VideoCapture(0)  # 0 là camera mặc định của máy tính

# Khởi tạo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Bind và lắng nghe kết nối
server_socket.bind(socket_address)
print("Listening at:", socket_address)


# Hàm xử lý việc gửi dữ liệu
def send_video():
  while vid.isOpened():
    ret, frame = vid.read()

    # Chú ý: Chỉnh chỉ mục của hàm imutils.resize để giữ nguyên kích thước khung hình
    frame = imutils.resize(frame, width=frame.shape[1])

    a = pickle.dumps(frame)
    a = zlib.compress(a, 9)  # Nén khung hình
    message = struct.pack("Q", len(a)) + a
    server_socket.sendto(message, (host_ip, port))

    cv2.imshow('TRANSMITTING VIDEO', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
      vid.release()  # Giải phóng tài nguyên camera
      break


# Tạo một luồng mới cho việc gửi dữ liệu
send_thread = threading.Thread(target=send_video)
send_thread.start()

# Main thread chờ nhận dữ liệu
while True:
  pass
