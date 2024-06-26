import numpy as np
import cv2
import os

########## KNN CODE ############
def distance(v1, v2):
	# Eucledian 
	return np.sqrt(((v1-v2)**2).sum())

def knn(train, test, k=5):
	dist = []
	
	for i in range(train.shape[0]):
		# Get the vector and label
		ix = train[i, :-1]
		iy = train[i, -1]
		# Compute the distance from test point
		d = distance(test, ix)
		dist.append([d, iy])
	# Sort based on distance and get top k
	dk = sorted(dist, key=lambda x: x[0])[:k]
	# Retrieve only the labels
	labels = np.array(dk)[:, -1]
	
	# Get frequencies of each label
	output = np.unique(labels, return_counts=True)
	# Find max frequency and corresponding label
	index = np.argmax(output[1])
	return output[0][index]
################################

#  Init camera
cap=cv2.VideoCapture(0)

# Face Detetction
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
face_data=[]
dataset_path="D:/data python/face_rego/person_face/"
label=[]
class_id=0 # Labels for the given file
names={} # Mapping btw id - name

# Data preparation
for fx in os.listdir(dataset_path):
    if(fx.endswith('.npy')):

        # create a mapping btw class_id and name

        names[class_id]=fx[:-4]
        data_item=np.load(dataset_path+fx)
        print('loaded '+fx)
        face_data.append(data_item)
        print(data_item.shape)

        # create labels for the class
        target=class_id*np.ones((data_item.shape[0],))
        # print(target)
        
        class_id+=1
        label.append(target)

# face_data=np.asarray(face_data)
# print(face_data)    
# print(face_data.shape)
face_dataset = np.concatenate(face_data,axis=0)
face_labels = np.concatenate(label,axis=0).reshape((-1,1))
print(face_dataset.shape)
print(face_labels.shape)
# print(face_labels)

trainset=np.concatenate((face_dataset,face_labels),axis=1)
print(trainset.shape)
# print(trainset)

# Testing
while True:
    ret,frame=cap.read()
    if ret==False:
        break
    
    faces=face_cascade.detectMultiScale(frame,1.3,5)
    for face in faces:
        x,y,w,h=face

        # Get The Face ROI
        offset=10
        face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
        face_section=cv2.resize(face_section,(100,100))
        
        # predicted label (out)
        # knn=KNN(trainset,face_section.flatten,5)
        out=knn(trainset,face_section.flatten())

        # Display on screen the name and rectangle around it
        pred_name=names[int(out)]
        cv2.putText(frame,pred_name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(67,210,210),2)
    cv2.imshow('Faces',frame)

    keypressed=cv2.waitKey(1) & 0xFF
    if keypressed == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
