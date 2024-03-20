import time

import cv2
import socket
import pickle
import struct
import imutils
import zlib

# Khởi tạo camera của máy tính thứ nhất
vid = cv2.VideoCapture(0)  # 0 là camera mặc định của máy tính

# Khởi tạo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Bind và lắng nghe kết nối
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at:", socket_address)

while True:
  client_socket, addr = server_socket.accept()
  print('GOT CONNECTION FROM:', addr)

  if client_socket:
    while vid.isOpened():
      ret, frame = vid.read()
      start = time.perf_counter()

      frame = imutils.resize(frame, width=500) # Giảm kích thước khung hình
      a = pickle.dumps(frame)
      a = zlib.compress(a, 9) # Nén khung hình
      message = struct.pack("Q", len(a)) + a
      client_socket.sendall(message)

      end = time.perf_counter()
      total_time = end - start

      fps = (int)(1 / total_time)
      cv2.putText(img=frame, text=f'FPS {fps}', org=(0, 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1,
                  color=(0, 0, 255), thickness=2)
      cv2.imshow('TRANSMITTING VIDEO', frame)

      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        client_socket.close()
        vid.release()  # Giải phóng tài nguyên camera
        break
