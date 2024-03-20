import cv2
import mysql.connector
import zlib
from base64 import b64decode
import numpy as np

# Kết nối đến MySQL
conn = mysql.connector.connect(
    host="192.168.210.148",
    user="root",
    password="123456",
    database="camera"
)
cursor = conn.cursor()

while True:
    # Lấy dữ liệu từ database
    cursor.execute('SELECT * FROM camera_data ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()

    if result:
        # Giải nén dữ liệu
        compressed_data = result[1]
        decompressed_data = zlib.decompress(compressed_data)

        # Chuyển dữ liệu về khung hình
        frame = cv2.imdecode(np.frombuffer(decompressed_data, dtype=np.uint8), 1)

        # Hiển thị khung hình
        cv2.imshow('Camera Data', frame)

    # Thoát vòng lặp khi nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cv2.destroyAllWindows()
conn.close()