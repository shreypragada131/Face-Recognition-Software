from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2


class Developer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x710+0+0") 
        self.root.title("Face Recognition System")
        
        title_lbl=Label(self.root,text="DEVELOPER",font=("times new roman",35,"bold"),bg="white",fg="darkblue")
        title_lbl.place(x=0,y=0,width=1530,height=45)
        
        img_top=Image.open(r"C:\Users\pc\OneDrive\Desktop\Face_recognition_system\college_images\dev.jpg")
        img_top=img_top.resize((1530,720),Image.Resampling.LANCZOS)
        self.photoimg_top=ImageTk.PhotoImage(img_top)
        
        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=1530,height=720)
        
        # Frame
        main_frame=Frame(f_lbl,bd=2,bg="white")
        main_frame.place(x=1000,y=0,width=500,height=600)
        
        img_top1=Image.open(r"C:\Users\pc\OneDrive\Desktop\Face_recognition_system\college_images\shrey.JPG")
        img_top1=img_top1.resize((200,200),Image.Resampling.LANCZOS)
        self.photoimg_top1=ImageTk.PhotoImage(img_top1)
        
        f_lbl=Label(main_frame,image=self.photoimg_top1)
        f_lbl.place(x=300,y=0,width=200,height=200)
        
        # Developer Info
        dev_label=Label(main_frame,text="Hello my name is Shrey",font=("times new roman",20,"bold"),bg="white")
        dev_label.place(x=0,y=5)
        
        dev_label=Label(main_frame,text="I am full stack developer",font=("times new roman",20,"bold"),bg="white")
        dev_label.place(x=0,y=40)
        
        img_top2=Image.open(r"C:\Users\pc\OneDrive\Desktop\Face_recognition_system\college_images\KPIs-and-Agile-software-development-metrics-for-teams-1.jpg")
        img_top2=img_top2.resize((500,390),Image.Resampling.LANCZOS)
        self.photoimg_top2=ImageTk.PhotoImage(img_top2)
        
        f_lbl=Label(main_frame,image=self.photoimg_top2)
        f_lbl.place(x=0,y=210,width=500,height=390)
        
if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()