import numpy as np
from PIL import Image
import cv2
# Read 16-bit RGB565 image into array of uint16
with open('IMAGE.TXT','r') as f:
    rgb565array = np.genfromtxt(f, delimiter = ',').astype(np.uint16)
num=0
# Pick up image dimensions
h, w = rgb565array.shape
# Make a numpy array of matching shape, but allowing for 8-bit/channel for R, G and B
rgb888array = np.zeros([h,w,3], dtype=np.uint8)
#read the infrared gradient image which will be used to choose color in result image
scale=cv2.imread("infrared.png")
#find the highest and lowest temperature in file
top=0
bottom=0
for row in rgb565array:
    for i in row:
        if i>top:
            top = i
        if i<bottom:
            bottom = i


sep=670/(top-bottom) #separation of color between each degree in the image
new = []
row=0
#add appropriate colors for each value in the file
for rows in rgb565array:
    col=0
    row+=1
    for t in rows:
        val = (t-bottom)/(top-bottom)
        if bottom==0:
            bottom=1
        if top ==0:
            top=1
        cols=int(val*sep*top*bottom)
        if cols<0:
            cols*=-1
        col+=1
        usecolor=(scale[cols,0]) #color of that pixel
        rgb888array[row-1,col-1]= usecolor #get color of pixel

# Save result as PNG
try:
    Image.fromarray(rgb888array).save('image2.png')
    newimg=cv2.resize(rgb888array,(320,240))
    Image.fromarray(newimg).save('image2.png')
    print("Image successfully created as {}".format("image2.png"))
except:
    print("Unknown error occured")
