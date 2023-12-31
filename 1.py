import cv2
import numpy as np
import os
import time  # to desplay frames automatically
#from os import listdir


# Lists to store various data
house_val1=[]  #it stores different house values collectively
house_on_burnt=[] #it stores burnt house values collectively
house_on_unburnt=[] #it stores unburnt house values collectively
priority_house_on_burnt=[] #it stores priority house on burnt grass collectively
priority_house_on_unburnt=[] #it stores priority house on unburnt collectively
rescue_ratio=[] #it stores rescue ratio as specified by the question
path=r'C:\Users\santo\Documents\GitHub\UAS_software\images' # please add your image folder path
image_list=[] #it stores all the input images for displaying at the end
processed_image_list=[] #it stores the processed images for displaying at the end
image_name_list=[] # #it stores the images names for displaying at the end


# Loop through images in the specified path
for images in os.listdir(path):
    #print(images)

    # Initialize variables for each image and applying mask
    house_val=[]  # ot stores house values temperarly which is further appended in a list(nested) for further calculation 
    image_name_list.append(images)
    img = cv2.imread(os.path.join(path,images)) #reading images
    image=img
    image_list.append(image)
    hsvFrame = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    #Defining color ranges for various colors, science input image contains only 4 sifferent shades therefore i am extraction each seperatly to use it for further processing
    #red color
    red_lower = np.array([120,50,50], np.uint8)  #lower value of red color , found by hit and trial
    red_upper = np.array([139,255,255], np.uint8) #upper value of red color , found by hit and trial
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    res_red = cv2.bitwise_and(image, image, 
                                mask = red_mask)  # applying bitwaise and operator to extact only required color

    #green color
    green_lower = np.array([0,150,0], np.uint8)
    green_upper = np.array([85,254,150], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    res_green = cv2.bitwise_and(image, image,
                                mask = green_mask)

    #blue color
    blue_lower = np.array([0, 200, 250], np.uint8)
    blue_upper = np.array([20, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
    res_blue = cv2.bitwise_and(image, image,
                                    mask = blue_mask)

    #brown color
    brown_lower=np.array([90,150,10], np.uint8)
    brown_upper=np.array([150,250,150], np.uint8)
    brown_mask=cv2.inRange(hsvFrame, brown_lower, brown_upper)
    res_brown=cv2.bitwise_and(image, image,
                                    mask = brown_mask)


    # Combining color channels for burnt and unburnt areas to get desired set of images
    #unburnt
    unburnt1=cv2.addWeighted(res_green,1,res_blue,1,0) # adding green layer and blue layer with 100% values and 0 gamma, 0 gamma so that image do not change at all
    unburnt2=cv2.addWeighted(unburnt1,1,res_red,1,0)
    unburnt3=cv2.addWeighted(res_green,1,res_red,1,0)

    #burnt
    burnt1=cv2.addWeighted(res_brown,1,res_blue,1,0)
    burnt2=cv2.addWeighted(burnt1,1,res_red,1,0)
    burnt3=cv2.addWeighted(res_brown,1,res_red,1,0)

    #cv2.imshow('img',image)
    # Converting images to different color spaces
    res_green1=cv2.cvtColor(res_green,cv2.COLOR_RGB2LAB) #just to show differnet areas differently
    res_brown1=cv2.cvtColor(res_brown,cv2.COLOR_RGB2HSV_FULL)
    #cv2.imshow('res_green1',res_green1)
    #cv2.imshow('res_brown1',res_brown1)
    out_show=cv2.addWeighted(res_green1,1,res_brown1,1,0)
    out_show1=cv2.addWeighted(res_blue,1,res_red,1,0)
    out_show2=cv2.addWeighted(out_show,1,out_show1,1,0)
    #cv2.imshow('out_show',out_show1)
    processed_image_list.append(out_show2)

    # Creating a list of images for analysis
    house_list=[res_blue,res_red,burnt2,unburnt2,burnt3,unburnt3,burnt1,unburnt1]
    
    house_count=0
    for i in house_list: #loop for finding edges
        house_count=0
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) #converting bgr to gray science its easy to find in gray than in color format

        edges = cv2.Canny(gray, 1, 1,apertureSize=7,L2gradient=False) # applying canny edger detector to detect edges

        contours1=cv2.blur(edges,(5,5),) #blurring image 
        contours, _ = cv2.findContours(contours1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Joining poins to create a closed shape

        for contour in contours:
            #print(cv2.arcLength(contour,True))
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            num_vertices = len(approx)
            #print(num_vertices)

            if num_vertices == 3:
                
                #print('triangle')
                house_count=house_count+1

        #print(house_count)
        house_val.append(house_count)
    house_val1.append(house_val)
#print('house_val1',house_val1)

for i in house_val1: #for calculating differnt rwequired values as stored earlier in list
    house_on_burnt.append(i[0]+i[1]-i[2])
    house_on_unburnt.append(i[0]+i[1]-i[3])
    priority_house_on_burnt.append(((i[0]-i[6])*2)+(i[1]-i[4]))
    priority_house_on_unburnt.append(((i[0]-i[7])*2)+(i[1]-i[5]))
    rescue_ratio.append((((i[0]-i[6])*2)+(i[1]-i[4]))/(((i[0]-i[7])*2)+(i[1]-i[5])))

print('The number of houses on the burnt grass (Hb) : ',house_on_burnt) #printing results
print('The number of houses on the green grass (Hg) : ',house_on_unburnt)
print('The total priority of houses on the burnt grass (Pb) : ',priority_house_on_burnt)
print('The total priority of houses on the green grass (Pg) : ',priority_house_on_unburnt)
print('rescue ratio of priority (Pr) : ',rescue_ratio)


for i in range(len(rescue_ratio)): #shorting rescue ratio values in descending order
    for j in range(i + 1, len(rescue_ratio)):

        if rescue_ratio[i] < rescue_ratio[j]:
            rescue_ratio[i], rescue_ratio[j] = rescue_ratio[j], rescue_ratio[i]
            image_name_list[i],image_name_list[j]=image_name_list[j],image_name_list[i]


print('rev_rescue_ratio : ',rescue_ratio)
print('Image name list : ',image_name_list)

for i in range (len(image_list)): # for displaying input image and processed image one by one
    cv2.imshow('Input Image',image_list[i])
    cv2.imshow("Processed Image",processed_image_list[i])
    time.sleep(3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #ser_choise=input("Press enter to visualise next result : ")


#cv2.imshow('edges',edges)
#cv2.imshow('unburnt1',unburnt1)
#cv2.imshow('burnt1',burnt1)
#cv2.imshow('unburnt2',unburnt2)
#cv2.imshow('burnt2',burnt2)
#cv2.imshow('unburnt3',unburnt3)
#cv2.imshow('burnt3',burnt3)
#cv2.imshow('hsv',cv2.cvtColor(image,cv2.COLOR_BGR2HLS))
#cv2.imshow('img',image)
#cv2.imshow('red',res_red)
#cv2.imshow("blue",res_blue)
#cv2.imshow('green',res_green)
#cv2.imshow("brown",res_brown)

cv2.waitKey(0)
cv2.destroyAllWindows()


#some of # were used duing development process
