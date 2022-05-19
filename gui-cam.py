from fnmatch import translate
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
import easyocr
from translate import Translator

imgarray = []

def ShowFeed():
    
    ret, frame = root.cap.read()

    if ret:
        
        frame = cv2.flip(frame, 1)
       
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        videoImg = Image.fromarray(cv2image)        
        imgtk = ImageTk.PhotoImage(image = videoImg)

        root.cameraLabel.configure(image=imgtk)       
        root.cameraLabel.imgtk = imgtk

        root.cameraLabel.after(10, ShowFeed)
    else:        
        root.cameraLabel.configure(image='')



def Capture():
   
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    if destPath.get() != '':
        image_path = destPath.get()
   
    else:
        messagebox.showerror("Pilih Directory dulu!")

   
    imgName = image_path + '/' + image_name + ".jpg"

    # Capturing the frame
    ret, frame = root.cap.read()

    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)

    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image)

    imgarray.append(imgName)
    # Configuring the label to display the frame
    root.imageLabel.config(image=saved_image)
    root.imageLabel.photo = saved_image
    if success :
        messagebox.showinfo( title="Berhasil Disimpan!", message="Nama File :  " + imgName)



def StartCAM():
    
    root.cap = cv2.VideoCapture(0)
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)
    root.cameraLabel.config(text="")
    ShowFeed()

def FindDirect():
    
    destDirectory = filedialog.askdirectory(initialdir="Directorymu...")

    # Displaying the directory in the directory textbox
    destPath.set(destDirectory)

def Translating():
    
    imggray = cv2.imread(imgarray[-1])
    imggray = cv2.resize(imggray, None, fx=1, fy=1, )
    gray2 = cv2.cvtColor(imggray, cv2.COLOR_BGR2GRAY)
    adapptive = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,85,11)

    text = ''
    reader = easyocr.Reader(['en'])
    results = reader.readtext(gray2)

    for result in results:
        text += result[1] + ' '

    translator = Translator(to_lang='id', from_lang='en')
    resulttranslate = translator.translate(text)

    messagebox.showinfo(title="HASIL TRANSLATE", message= resulttranslate)

    cv2.imshow("gray", gray2)
    cv2.imshow("adaptive", adapptive)
    cv2.waitKey(0)
    

# Creating object of tk class
root = tk.Tk()



root.cap = cv2.VideoCapture(0)
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root.title("Text Recoginition")
root.geometry("1280x720")

root.resizable(width=False, height=False)
root.configure(background = "black")


destPath = StringVar()
imagePath = StringVar()

root.feedlabel = Label(root, bg="black", fg="white", text="Camera", font=('arial',20))
root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

root.saveLocationEntry = Entry(root, width=55, textvariable=destPath)
root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

root.browseButton = Button(root, width=10, text="BROWSE", command=FindDirect)
root.browseButton.grid(row=3, column=2, padx=10, pady=10)


root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="black", font=('times new roman',20), fg="white", width=20)
root.captureBTN.grid(row=4, column=1, padx=10, pady=10)


root.previewlabel = Label(bg="black", fg="white", text="Hasil Capture", font=('arial',20))
root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

root.imageLabel = Label(root, bg="black", borderwidth=3, relief="groove")
root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

# root.openImageEntry = Label(text="HASIL TRANSLATE DISINI",bg="black", fg="white", font=('times new roman',26))
root.openImageEntry = Button(root, text="Translate", command= Translating, bg="black", font=('times new roman',20), fg="white", width=20)
root.openImageEntry.grid(row=4, column=4, padx=10, pady=10 )

ShowFeed()
root.mainloop()