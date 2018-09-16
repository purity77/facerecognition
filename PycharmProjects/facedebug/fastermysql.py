#!/home/pray/anaconda2/envs/py3/bin/python3.6
import face_recognition
import cv2
import pickle
from multiprocessing import Pool
import pymysql
import prettytable
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# 这个例子处理更快速：
#   1. 缩放捕捉到的每帧到1/8
#   2. Only detect faces in every other frame of video.

video_capture = cv2.VideoCapture(0)
video_capture.set(3, 480)  # set Width
video_capture.set(4, 480)  # set Height
#将图像加载到numpy数组中。如果您已经有一个numpy数组中的图像，可以跳过此步骤。
#为图像中的每个面部获取面部编码。注意：查找面部的编码有点慢，所以如果需要可以将结果保存在数据库或缓存中


#data包括已知的人脸名字以及编码
data = pickle.loads(open('encodings.pkl', "rb").read())

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []



def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:qq, 密码:qq12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
    #db = pymysql.connect(host="127.0.0.1",port=3306,user="qq",password="qq1020.",db="facerecognition")
    db = pymysql.connect("localhost", "root", "qq1020", "facerecognition")

    print('连接上了!')
    return db

def createtable(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 如果存在表Sutdent先删除
    #cursor.execute("DROP TABLE IF EXISTS student")
    #sql = """CREATE TABLE student (id VARCHAR(12) NOT NULL,name CHAR(8),attend INT )"""
    cursor.execute("DROP TABLE IF EXISTS dayattend")
    sql = """CREATE TABLE dayattend (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,name VARCHAR(8),attend VARCHAR(12)) """
    # 创建Sutdent表
    cursor.execute(sql)

def insertdb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 提前插入data【name】
    # sql = """INSERT INTO student
    #      VALUES ('001', 'CZQ', 70),
    #             ('002', 'LHQ', 80),
    #             ('003', 'MQ', 90),
    #             ('004', 'WH', 80),
    #             ('005', 'HP', 70),
    #             ('006', 'YF', 66),
    #             ('007', 'TEST', 100)"""
    #sql = "INSERT INTO Student(ID, Name, Grade) \
    #    VALUES ('%s', '%s', '%d')" % \
    #    ('001', 'HP', 60)

    for name in set(data["names"]):
        initattend='0'
        sql = """INSERT INTO dayattend(name,attend) VALUES (%s, %s)"""
        try:
            # 执行sql语句
            cursor.execute(sql,(name,initattend))
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            print('插入数据失败!')
            db.rollback()

def querydb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    #sql = "SELECT * FROM Student \
    #    WHERE Grade > '%d'" % (80)
    sql = "SELECT * FROM dayattend"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        #获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            ID = row[0]
            Name = row[1]
            Attend = row[2]
            # 打印结果
            print("ID: %s, Name: %s, Attend: %s" %(ID,Name,Attend))
        # table = prettytable(cursor)
        # print(table)
    except:
        print("Error: unable to fecth data")

def deletedb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 删除语句
    for names in face_names:
        if(names):
            sql = "DELETE FROM dayattend WHERE name = '%s'"
            try:
               # 执行SQL语句
               cursor.execute(sql,(name))
               # 提交修改
               db.commit()
            except:
                print('删除数据失败!')
                # 发生错误时回滚
                db.rollback()

def updatedb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 更新语句
    for names in set(face_names):
        print('names is '+names)
        if(names):
            sql = "UPDATE dayattend SET attend ='1' WHERE name = '%s'" %(names)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                print('更新数据失败!')
                # 发生错误时回滚
                db.rollback()

def closedb(db):
    db.close()

# Display the results
def display():
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


process_this_frame = True
while True:
    # 获取一帧视频
    ret, frame = video_capture.read()

    # 缩放帧到1/8
    small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

    # 将BGR颜色（使用OpenCV）的图像转换为RGB颜色（使用face_recognition）
    rgb_small_frame = small_frame[:, :, ::-1]
    # Hit 'q' on the keyboard to quit!
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame,model='hog')
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        #face_names = []
        for face_encoding in face_encodings:
            # 第一个参数是已知的面部编码列表，第二个参数是未知的单个面部编码
            matches = face_recognition.compare_faces(data["encodings"], face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                #通过建立一个简单的matchedIdxs列表确定True值在matches中的索引位置，初始化counts字典，键为人的名字，值是投票数量
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
               # first_match_index = matches.index(True)
               # name = known_face_names[first_match_index]
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    print(counts)
                name = max(counts, key=counts.get)
                print(name)
            face_names.append(name)


    po=Pool(3)
    po.apply_async(display(),())
    po.close()
    po.join()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

process_this_frame = not process_this_frame


# Release handle to the webcamqq
video_capture.release()
cv2.destroyAllWindows()
print(face_names)
# q
db= connectdb()
createtable(db)
insertdb(db)
print("\n插入data中的名字数据")
querydb(db)
updatedb(db)
print("\n出勤学生attend为1")
querydb(db)
closedb(db)
# def main():
#     db = connectdb()    # 连接MySQL数据库
#
#     createtable(db)     # 创建表
#     insertdb(db)        # 插入数据
#     print('\n插入数据后:')
#     querydb(db)
#     deletedb(db)        # 删除数据
#     print('\n删除数据后:')
#     querydb(db)
#     updatedb(db)        # 更新数据
#     print('\n更新数据后:')
#     querydb(db)
#
#     closedb(db)         # 关闭数据库
#
# if __name__ == '__main__':
#     main()