import numpy as np
from tensorflow import keras
import cv2
from custom_socket import CustomSocket
import json
import traceback

wtf_color_model = keras.models.load_model("model\wtf_color_det")
wtf_shape_model = keras.models.load_model("model\wtf_shape_det")
COLOR_LIST = ("blue", "red", "yellow", "purple", "green", "orange", "pink", "wine", "mint", "none")
SHAPE_LIST = ("circle", "hex", "pill", "pie", "none")


def get_center_list(f_w, f_h, nw, nh):
    l = []
    for h in range(nh):
        for w in range(nw):
            l += [(int(w / nw * f_w + f_w / nw / 2), int(h / nh * f_h + f_h / nh / 2))]

    return l


def get_start_point_list(f_w, f_h, nw, nh):
    l = []
    for h in range(nh):
        for w in range(nw):
            l += [(int(w / nw * f_w), int(h / nh * f_h))]

    return l


def draw_grid(pic, w, h, color, thickness):
    ph, pw, _ = pic.shape
    for i in range(1, h):
        cv2.line(pic, (0, int(ph * i / h)), (pw, int(ph * i / h)), color, thickness)
    for i in range(1, w):
        cv2.line(pic, (int(pw * i / w), 0), (int(pw * i / w), ph), color, thickness)


def draw_circle(pic, center_list, radius, color, thickness):
    for center in center_list:
        cv2.circle(pic, center, radius, color, thickness)


def draw_points(pic, center, d, color):
    cx, cy = center

    pic[cy, cx] = color
    pic[cy - d, cx] = color
    pic[cy + d, cx] = color
    pic[cy, cx - d] = color
    pic[cy, cx + d] = color


def get_color_data(pic, center, d):
    # dl = []
    cx, cy = center
    return ",".join(map(str, (*pic[cy, cx], *pic[cy - d, cx], *pic[cy + d, cx], *pic[cy, cx - d], *pic[cy, cx + d])))


def get_shape_data(pic_gray, start_point):
    sx, sy = start_point
    return ",".join(map(str, pic_gray[sy + 1:sy + SLOT_DIM - 1, sx + 1:sx + SLOT_DIM - 1].flatten()))


def get_color_data_list(pic, center, d):
    cx, cy = center
    return np.array([*pic[cy, cx], *pic[cy - d, cx], *pic[cy + d, cx], *pic[cy, cx - d], *pic[cy, cx + d]]).astype(
        "uint8")


def get_shape_data_list(pic_gray, start_point):
    sx, sy = start_point
    return np.array(((pic_gray[sy + 1:sy + SLOT_DIM - 1, sx + 1:sx + SLOT_DIM - 1] + 1) % 256).flatten()).astype(
        "uint8")


RESIZE_DIM = 240
TOPLEFT, BOTRIGHT = [126, 29], [520, 427]
SLOT_DIM = RESIZE_DIM // 6
pos_index = 0
n_slot = 1
label = 0

l = []
for i in range(10):
    try:
        ret, frame = cv2.VideoCapture(i).read()
        if not ret:
            continue
        l += [i]
    except:
        continue

print(l)

cap = cv2.VideoCapture(int(input("Cam index: ")))
f_w, f_h = cap.get(3), cap.get(4)

center_list = get_center_list(RESIZE_DIM, RESIZE_DIM, 6, 6)
start_point_list = get_start_point_list(RESIZE_DIM, RESIZE_DIM, 6, 6)

# print(center_list)


HOST = "localhost"
PORT = 10000
print(HOST)

server = CustomSocket(HOST, PORT)
server.startServer()

while True:
    # Wait for connection from client :}
    conn, addr = server.sock.accept()
    print("Client connected from", addr)

    while cap.isOpened():

        try:

            data = np.frombuffer(server.recvMsg(conn), dtype=np.uint8)[0]
            print(data)

            ret, frame = cap.read()
            frame_bgr = cv2.resize(frame[TOPLEFT[1]: BOTRIGHT[1], TOPLEFT[0]:BOTRIGHT[0]], (RESIZE_DIM, RESIZE_DIM))
            frame_show = np.copy(frame_bgr)
            frame_gray = cv2.cvtColor(frame_show, cv2.COLOR_BGR2GRAY)

            for i in range(RESIZE_DIM):
                for j in range(RESIZE_DIM):
                    b, g, r = map(int, frame_show[i, j])
                    # print((b+g+r/3))
                    m = (b + g + r) / 3

                    if m > 100 and ((b - m) ** 2 + (g - m) ** 2 + (r - m) ** 2) < 400:
                        frame_gray[i, j] = 255
                        # print("yes")
                    else:
                        frame_gray[i, j] = 0

            if not ret:
                print("Error")
                continue

            draw_grid(frame_show, 6, 6, (0, 0, 0), 1)

            for n in range(n_slot):
                draw_points(frame_show, center_list[(pos_index + n) % 36], 6, (0, 0, 0))

            frame_show = cv2.resize(frame_show, (480, 480))
            cv2.imshow("frame", frame_show)

            # sx, sy = center_list[pos_index]
            # cv2.imshow("frameg", frame_gray)
            # cv2.imshow("id_frame", frame_gray[sy + 1:sy + SLOT_DIM - 1, sx + 1:sx + SLOT_DIM - 1])

            key = cv2.waitKey(1)

            # color_l = get_color_data_list(frame_bgr, center_list[pos_index], 6)
            all_color_list = []
            for cen in center_list:
                all_color_list += [get_color_data_list(frame_bgr, cen, 6)]
            # print(all_color_list)
            color_res = np.argmax(wtf_color_model.predict(np.array(all_color_list), verbose=0), axis=1)
            print(color_res)

            all_shape_list = []
            for stp in start_point_list:
                all_shape_list += [get_shape_data_list(frame_gray, stp)]

            shape_res = np.argmax(wtf_shape_model.predict(np.array(all_shape_list), verbose=0), axis=1)
            print(shape_res)

            if data == 1:
                server.sendMsg(conn, json.dumps({"c": list(map(int, color_res))}))
            if data == 0:
                server.sendMsg(conn, json.dumps({"s": list(map(int, shape_res))}))


            if key == ord('q'):
                cap.release()
            elif key == ord('n'):
                pos_index = (pos_index + 1) % 36



        except Exception as e:
            traceback.print_exc()
            print(e)
            print("Connection Closed")
            break

    cv2.destroyAllWindows()
