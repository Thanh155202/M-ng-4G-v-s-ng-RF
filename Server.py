import cv2
import socket
import pickle
import struct

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
      a = pickle.dumps(frame)
      message = struct.pack("Q", len(a)) + a
      client_socket.sendall(message)

      cv2.imshow('TRANSMITTING VIDEO', frame)
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        client_socket.close()
        vid.release()  # Giải phóng tài nguyên camera
        break
