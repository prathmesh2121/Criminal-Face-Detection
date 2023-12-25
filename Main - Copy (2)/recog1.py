import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import exifread
import webbrowser

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

def get_image_location(image_path):
    with open(image_path, 'rb') as file:
        tags = exifread.process_file(file)
        lat_ref = tags.get('GPS GPSLatitudeRef')
        lon_ref = tags.get('GPS GPSLongitudeRef')
        lat = tags.get('GPS GPSLatitude')
        lon = tags.get('GPS GPSLongitude')

        if lat and lon and lat_ref and lon_ref:
            lat_deg = float(lat.values[0].num) / float(lat.values[0].den)
            lat_min = float(lat.values[1].num) / float(lat.values[1].den)
            lat_sec = float(lat.values[2].num) / float(lat.values[2].den)
            lon_deg = float(lon.values[0].num) / float(lon.values[0].den)
            lon_min = float(lon.values[1].num) / float(lon.values[1].den)
            lon_sec = float(lon.values[2].num) / float(lon.values[2].den)

            latitude = lat_deg + (lat_min / 60.0) + (lat_sec / 3600.0)
            longitude = lon_deg + (lon_min / 60.0) + (lon_sec / 3600.0)

            if lat_ref.values == 'S':
                latitude = -latitude
            if lon_ref.values == 'W':
                longitude = -longitude

            return latitude, longitude
        else:
            return None

def generate_google_maps_link(latitude, longitude):
    return f"https://www.google.com/maps/place/{latitude},{longitude}/@{latitude},{longitude},13z"

def show_location_on_google_maps(latitude, longitude):
    google_maps_link = generate_google_maps_link(latitude, longitude)
    webbrowser.open_new(google_maps_link)

def separate_and_recognize_faces():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        group_image = cv2.imread(file_path)
        if group_image is None:
            messagebox.showerror("Error", "Could not load the image. Please select a valid image file.")
            return
        
        gray = cv2.cvtColor(group_image, cv2.COLOR_BGR2GRAY)
        
        location = get_image_location(file_path)
        if location:
            lat, lon = location
            messagebox.showinfo("Image Location", f"Latitude: {lat}, Longitude: {lon}\n\nClick OK to open in Google Maps.")

            # Open Google Maps in the default web browser
            show_location_on_google_maps(lat, lon)
        
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

        # Display the image location here, after closing the image window
        if location:
            lat, lon = location
            messagebox.showinfo("Image Location", f"Latitude: {lat}, Longitude: {lon}")

window = tk.Tk()
window.title("Face Separation and Recognition")

select_button = tk.Button(window, text="Select Group Photo", command=separate_and_recognize_faces)
select_button.pack()

window.mainloop()
