import face_recognition
import cv2

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# 这个例子处理更快速：
#   1. 缩放捕捉到的每帧到1/8
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640)  # set Width
video_capture.set(4, 480)  # set Height
#将图像加载到numpy数组中。如果您已经有一个numpy数组中的图像，可以跳过此步骤。
obama_image = face_recognition.load_image_file("obama.jpg")
#为图像中的每个面部获取面部编码。注意：查找面部的编码有点慢，所以如果需要可以将结果保存在数据库或缓存中
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]


biden_image = face_recognition.load_image_file("lyf.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "dzy",
    "lyf"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # 获取一帧视频
    ret, frame = video_capture.read()

    # 缩放帧到1/8
    small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

    # 将BGR颜色（使用OpenCV）的图像转换为RGB颜色（使用face_recognition）
    rgb_small_frame = small_frame[:, :, ::-1]

    # 在这个视频帧中循环遍历每个人脸
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 第一个参数是已知的面部编码列表，第二个参数是未知的单个面部编码
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 8
        right *= 8
        bottom *= 8
        left *= 8

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
