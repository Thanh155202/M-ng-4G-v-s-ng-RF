import cv2
import socket
import pickle
import struct
import zlib

# Khởi tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '172.20.10.3'  # Điền IP của máy chủ (máy tính thứ nhất)
port = 9999
client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

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
    frame_data = zlib.decompress(frame_data) # Giải nén khung hình
    frame = pickle.loads(frame_data)
  except pickle.UnpicklingError as e:
    print(f"Error unpickling frame: {e}")
    break

  cv2.imshow("RECEIVING VIDEO", frame)
  key = cv2.waitKey(1) & 0xFF
  if key == ord('q'):
    break

client_socket.close()