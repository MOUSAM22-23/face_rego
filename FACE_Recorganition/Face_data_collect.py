import cv2
import numpy as np


face_data =[]
dataset_path ="D:/data python/face_rego/person_face/"
file_name = input("Enter the name of the person:")
skip = 0
#Init Camera

cap = cv2.VideoCapture(0)

#Face Detection

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")



while True :
    ret,frame = cap.read()
    
    if ret==False:
        break
        
        
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
        
    
    
    faces = face_cascade.detectMultiScale(frame,1.3,5)
    faces = sorted(faces,key=lambda f:f[2]*f[3])
    
    for face in faces[-1:]:
        x,y,w,h = face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        
        #Extract(Crop out the required face):Region of Interest
        
        
        
        offset =10
        face_section =frame[y-offset:y+h+offset,x-offset:x+w+offset]
        face_section = cv2.resize(face_section,(100,100))
        
        
        skip += 1
        if skip%10==0:
            face_data.append(face_section)
            print(len(face_data))
    
        
        
        
        cv2.imshow("Frame Section ",face_section)
  
        cv2.imshow("Frame",frame)
    
    
    #Story every 10th face later on
    
   
    
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed ==ord('q'):
        break
        
        
#Converth our face list array into numpy array
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0],-1))
print(face_data.shape)

#save this data into file system

np.save(dataset_path+file_name+'.npy',face_data)
print("Data successfully save at" +dataset_path+file_name+'.npy',face_data)
        
cap.release()
cv2.destroyAllWindows()
