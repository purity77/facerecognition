print("Initialing...")
import os
import time
import pickle
import face_recognition

time_start = time.time()
path = os.getcwd() + '/images'
os.chdir(path)
images_file = os.listdir('.')
know_names = []
know_paths = []
know_encodings = []
print("Reading files from directory...")
for each in images_file:
    name = os.path.splitext(each)[0]
    know_names.append(name)
    image_path = path + '/' + each
    know_paths.append(image_path)
print("Starting encoding!")
# print(know_names)
# print(know_paths)
count = 1
for each_path in know_paths:
    img = face_recognition.load_image_file(each_path)
    # locate face and detection_method
    print("Encoding the %d picture..." % count)
    # boxes = face_recognition.face_locations(img,model = 'cnn')#hog faster,and cnn more accurate
    encoding = face_recognition.face_encodings(img)[0]
    # encoding = face_recognition.face_encodings(img,boxes)
    know_encodings.append(encoding)
    count = count + 1
# 原文中采用字典存储，写入了一个文件，我把它俩分开了
print("Finished encodings,Writing pickle file...")
# dump images encodings in to face_encodings.pkl file
pickle_encoding_file = open('../face_encodings.pkl', 'wb')
pickle.dump(know_encodings, pickle_encoding_file)
pickle_encoding_file.close()

# dump images names in to face_names.pkl file
pickle_name_file = open('../face_names.pkl', 'wb')
pickle.dump(know_names, pickle_name_file)
pickle_name_file.close()
time_end = time.time()
time_take = time_end - time_start
print("It takes %s seconds!" % time_take)
print("All images pretreatment finished!")
