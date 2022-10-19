'''
CO543 - IMAGE PROCESSING

Mini project - Sri Lankan Vehicle Number Plate Recognition System

Group F
E/17/284 : RATHNAYAKA R.L.D.A.S.
E/17/212 : MORAIS K.W.G.A.N.D. 
E/17/219 : NAWARATHNA K.G.I.S.
'''
# Import libraries
import cv2
import pytesseract
import argparse

# The location of the tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path of the image")
args = vars(ap.parse_args())

# Get the image in Grayscale
img = cv2.imread(args["image"])
cv2.imshow("Original image", img)
cv2.waitKey(0)


############
# Preprocess
############

# Convert to Grayscale Image
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Greyed image", gray_image)
cv2.waitKey(0)

# Canny Edge Detection filter
canny_edge = cv2.Canny(gray_image, 170, 200)
cv2.imshow("Canny edge image", canny_edge)
cv2.waitKey(0)


##########################
# Number plate recognition
##########################

# Find contours According to thge Edges
contours, new  = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]

# Find the Best contour 
i=8
for c in contours:
    perimeter = cv2.arcLength(c, True)

    # Approximates a polygonal curve(s) with the specified precision
    approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
    screenCnt = approx
    if len(approx) == 4: 
        screenCnt = approx

        #Set the boundaries
        x,y,w,h = cv2.boundingRect(c) 

        #Crop the image according to the contour
        new_img=img[y:y+h,x:x+w]

        # Save cropped contour
        cv2.imwrite('./croped/'+str(i)+'.png',new_img)
        
        i+=1
        break

# Draw selected contour on the image
cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("image with detected license plate", img)
cv2.waitKey(0)

# Show the cropperd license plate
cv2.imshow("cropped", cv2.imread('./croped/8.png'))

# Read the Licence plate number and extract the number
vehicle_plate = pytesseract.image_to_string('./croped/8.png', lang='eng')

cv2.waitKey(0)
cv2.destroyAllWindows()


###########################
# Licence Number Validation
###########################

number = list(vehicle_plate)
L = len(number)

print("\n##################################################")
print("Sri Lankan Vehicle Number Plate Recognition System")
print("##################################################\n")

# Function to check the validity of a number
def checkValidity(number):
    l = len(number)
    
    # Check if it has a valid length
    if (l < 5 or l > 7):
        return False

    else:
        firstPart = number[:l-4]
        lp = number[l-4:]
        lf = len(firstPart)
        
        
        # Check the all characters are in the last part are numeric
        if ((not lp[0].isnumeric()) or (not lp[1].isnumeric()) or (not lp[2].isnumeric()) or (not lp[3].isnumeric())):
            return False
         
        # Check whether the first part has valid lenght    
        elif (lf > 3):
            return False

        else:
            # If the first part is Numeric,
            # Check whether is it a valid number
            if (firstPart[0].isnumeric()):
                num =int("".join(firstPart))
                if (num >325):
                    return False

            else:
                # For the number which has alphebet characters
                # # Check whether is it a valid number
                if (lf < 2):
                    return False

                # For three character numbers
                elif (lf == 3):
                    validChars = ['A','B','C','D']
                    if (firstPart[0] not in validChars):
                        return False

                # For two character numbers
                elif(lf == 2):
                    validChars = ['E','F','G','H','J','K','L','N','P','Q','R','S','T','U','V','W','X','Y','Z']
                    if (firstPart[0] not in validChars):
                        return False
                
    # Return true for a valid number            
    return True

# Check the validity of the number
if(not checkValidity(number)):
    print("Vehicle Licence Plate: " + vehicle_plate)
    print("\n------------")
    print("The validity")
    print("============")
    print ("Number is not Valid in Sri Lanka\n")
else:
    print("Vehicle Licence Plate: " + "".join(number[:L-4]) + " - " + "".join(number[L-4:]))
    print("\n------------")
    print("The validity")
    print("============")
    print("Number is valid\n")
