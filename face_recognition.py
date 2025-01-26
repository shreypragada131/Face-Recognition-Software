from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from time import strftime
from datetime import datetime
import mysql.connector
import cv2
import os
import numpy as np

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x710+0+0") 
        self.root.title("Face Recognition System")
        
        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="darkblue")
        title_lbl.place(x=0, y=0, width=1530, height=45)
        
        try:
            # first image
            img_top = Image.open(r"college_images\face_detector1.jpg")
            img_top = img_top.resize((650, 700), Image.Resampling.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            
            f_lbl = Label(self.root, image=self.photoimg_top)
            f_lbl.place(x=0, y=55, width=650, height=700)
            
            # second image
            img_bottom = Image.open(r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
            img_bottom = img_bottom.resize((950, 700), Image.Resampling.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            
            f_lbl2 = Label(self.root, image=self.photoimg_bottom)
            f_lbl2.place(x=650, y=55, width=950, height=700)
            
            # button
            b1_1 = Button(f_lbl2, text="Face Recognition", command=self.face_recog, cursor="hand2", 
                         font=("times new roman", 18, "bold"), bg="darkblue", fg="white")
            b1_1.place(x=370, y=620, width=200, height=40)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading UI components: {str(e)}")
            
    #===================================Function====================================
    def mark_attendance(self,i,r,n,d):
        with open("Student.csv","r+",newline="\n") as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")
                 
    
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            
            coord = []
            
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100*(1-predict/300)))
                
                try:
                    conn = mysql.connector.connect(host="localhost", username="root", 
                                                password="$hreyPVIT131", database="face_recognizer")
                    my_cursor = conn.cursor()
                    
                    my_cursor.execute("SELECT Name, Roll, Dep, Student_id FROM student WHERE Student_id=" + str(id))
                    data = my_cursor.fetchone()
                    
                    if data:
                        n, r, d, i = data
                        
                        if confidence > 77:
                            cv2.putText(img, f"ID: {i}", (x, y-80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                            cv2.putText(img, f"Roll: {r}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                            cv2.putText(img, f"Name: {n}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                            cv2.putText(img, f"Department: {d}", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                            self.mark_attendance(i,r,n,d)
                        else:
                            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                            cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    
                    conn.close()
                except Exception as e:
                    print(f"Database error: {e}")
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                
                coord = [x, y, w, h]
            
            return coord
        
        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img
        
        try:
            # Get the absolute path to the haar cascade file
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            
            # Verify cascade file exists before loading
            if not os.path.exists(cascade_path):
                messagebox.showerror("Error", f"Cascade file not found at: {cascade_path}")
                return
                
            # Load the cascade classifier
            faceCascade = cv2.CascadeClassifier(cascade_path)
            
            # Verify the classifier was loaded properly
            if faceCascade.empty():
                messagebox.showerror("Error", "Failed to load cascade classifier")
                return
                
            # Load the face recognizer
            clf = cv2.face.LBPHFaceRecognizer_create()
            
            # Check if classifier.xml exists before loading
            if not os.path.exists("classifier.xml"):
                messagebox.showerror("Error", "classifier.xml not found")
                return
                
            clf.read("classifier.xml")
            
            # Initialize video capture
            video_cap = cv2.VideoCapture(0)
            if not video_cap.isOpened():
                messagebox.showerror("Error", "Cannot access webcam")
                return
            
            while True:
                ret, img = video_cap.read()
                if ret:
                    img = recognize(img, clf, faceCascade)
                    cv2.imshow("Welcome to Face Recognition", img)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            video_cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error in face recognition: {str(e)}")
            if 'video_cap' in locals():
                video_cap.release()
            cv2.destroyAllWindows()

def main():
    print(f"Looking for cascade file at: {cv2.data.haarcascades}")
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()

if __name__ == "__main__":
    main()