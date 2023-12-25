import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import csv


model = cv2.face.LBPHFaceRecognizer_create()
model.read('trained_model.yml')


face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')


label_map = {}


for folder in os.listdir('criminal_images'):
    if os.path.isdir(os.path.join('criminal_images', folder)):
        
        label = len(label_map)
        label_map[label] = folder


criminal_details = {}
with open('criminal_details.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        criminal_details[row['CID']] = row


def separate_and_recognize_faces():
    
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        
        group_image = cv2.imread(file_path)
        gray = cv2.cvtColor(group_image, cv2.COLOR_BGR2GRAY)

        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]

            
            label, confidence = model.predict(face_roi)

            if confidence < 100:
                recognized_person = label_map.get(label, 'Unknown')
                criminal_info = criminal_details.get(recognized_person)
                if criminal_info:
                    name = criminal_info['Name']
                    dob = criminal_info['DOB']
                    age = criminal_info['Age']
                    last_location = criminal_info['Last Location']
                    crimes = criminal_info['Crimes']
                    info_text = f"Name: {name}\nDOB: {dob}\nAge: {age}\nLast Location: {last_location}\nCrimes: {crimes}"
                    messagebox.showinfo("Criminal Information", info_text)
            else:
                recognized_person = 'Unknown'

            
            cv2.rectangle(group_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(group_image, recognized_person, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        
        cv2.imshow('Group Photo', group_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



window = tk.Tk()
window.title("Face Separation and Recognition")


select_button = tk.Button(window, text="Select Group Photo", command=separate_and_recognize_faces)
select_button.pack()


window.mainloop()
