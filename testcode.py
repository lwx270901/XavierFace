import os
image_dir = 'dataset/known'


images_list  = os.listdir(image_dir)
print(images_list)
known_face_encodings = []
known_face_names = []
for image in images_list:
    temp_arr = image.split(".")
    known_face_names.append(temp_arr[0])

print(known_face_names)