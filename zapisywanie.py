import cv2
import numpy as np
import math
import copy
#Wczytywanie zdjęcia w zredukowanej skali kolorowej
licznik_nazwy=2
img=cv2.imread(f'do_sieci/Zbior_do_uczenia/{licznik_nazwy}u.jpg',cv2.IMREAD_REDUCED_COLOR_2)
img=cv2.resize(img,(800,1000))
img_ORG=copy.copy(img)
#operacja mające na celu lepiej odzielić kolor czarny 
board = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8)
board1=board*80
board2=board*12
img=cv2.subtract(img, board1)
img=cv2.multiply(img, board2)


#progowanie
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,th1 = cv2.threshold(grayImage,30,255,cv2.THRESH_BINARY_INV)


#Uzyskanie kontórów i narysowanie kontórów z przedziału w którym miesci sie M
contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
drawing = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
for Cont in range(len(contours)):
    approx = cv2.contourArea(contours[Cont])
    if approx>100 and approx<500 :
        cv2.drawContours(drawing, contours, Cont, (0,255,0), 1)
#cv2.imshow("okno",drawing)



#Zmienienie koloru na biało czarny a następnie ponowne progowanie 
Img_to_compare = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
ret,Img_to_compare = cv2.threshold(Img_to_compare,127,255,cv2.THRESH_BINARY)


#Wczytanie probnika
template = cv2.imread('M.png',cv2.IMREAD_GRAYSCALE)
ret,template = cv2.threshold(template,127,255,cv2.THRESH_BINARY)
# cv2.imshow("greyTemple",template)



#M filtration
drawing2 = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

contours,hierarchy = cv2.findContours(template,2,1)
cnt1 = contours[0]
contours2,hierarchy2 = cv2.findContours(Img_to_compare,2,1)
lista_matchy=[]
n=int(0)
for cnt2 in contours2:
    ret = cv2.matchShapes(cnt1,cnt2,1,244)
    if  ret<0.5:
        lista_matchy.append(ret)
        cv2.drawContours(drawing2, contours2, n, (0,255,0), 1)
    n+=1     
    

#Zmienienie koloru na biało czarny a następnie ponowne progowanie 
Img_to_compare2 = cv2.cvtColor(drawing2, cv2.COLOR_BGR2GRAY)
ret,Img_to_compare2 = cv2.threshold(Img_to_compare2,127,255,cv2.THRESH_BINARY)

#Ze względu na obwód konturu
contours3, hierarchy = cv2.findContours(Img_to_compare2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
drawing4 = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

n=0
for contour in range(len(contours3)):
    perimeter = cv2.arcLength(contours3[contour],True)
    if perimeter>110 and perimeter<170:
        cv2.drawContours(drawing4, contours3, contour, (0,255,0), 1)

#Zmienienie koloru na biało czarny a następnie ponowne progowanie 
Img_to_compare3 = cv2.cvtColor(drawing4, cv2.COLOR_BGR2GRAY)
ret,Img_to_compare3 = cv2.threshold(Img_to_compare3,127,255,cv2.THRESH_BINARY)
#cv2.imshow("after M filtration",Img_to_compare4)

#Ze względu na prostokaty obwodzace
contours5, hierarchy = cv2.findContours(Img_to_compare3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
drawing5 = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
drawing6_Centers = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
Mid=[]
for contour in range(len(contours5)):
    rect = cv2.minAreaRect(contours5[contour])
    box = cv2.boxPoints(rect)
    #liczenie pola
    
    a=math.sqrt((box[0][0]-box[1][0])**2+(box[0][1]-box[1][1])**2)
    b=math.sqrt((box[1][0]-box[2][0])**2+(box[1][1]-box[2][1])**2)
    area=a*b
    slender=0
    if a>b:
        slender=b/a
    else:
        slender=a/b
    box = np.int0(box)
    if area>500 and slender>0.60:
        cv2.drawContours(drawing5,[box],0,(0,255,0),3)
        Mid_1=(box[0][0]+box[1][0]+box[2][0]+box[3][0])/4
        Mid_2=(box[0][1]+box[1][1]+box[2][1]+box[3][1])/4
        Mid.append([int(Mid_1),int(Mid_2)])
    
 #Zmienienie koloru na biało czarny a następnie ponowne progowanie 
Rectangles = cv2.cvtColor(drawing5, cv2.COLOR_BGR2GRAY)
ret,Rectangles = cv2.threshold(Rectangles,127,255,cv2.THRESH_BINARY)

#cv2.imshow("after all, rectangles",Rectangles )
#Wrysowanie znalezionych M
Marked_Ms=cv2.add(drawing5,img_ORG)
#cv2.imshow("working finder",Marked_Ms )

#Usunięcie punktow podwojonych i wyznaczenie obszarow do sprawdzania kolorow
ret,drawing6_Centers = cv2.threshold(drawing6_Centers,127,255,cv2.THRESH_BINARY)
radius=30
for srodek in Mid:
    cv2.circle(drawing6_Centers,(srodek[0],srodek[1]), radius, 255, -1)

##KLASYFIKATOR
contours6_circles, hierarchy = cv2.findContours(drawing6_Centers, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Znalezienie Srodkow
Mid=[]
for cont in contours6_circles:
    xval=0
    yval=0
    for point in cont:
        xval=xval+point[0][1]
        yval=yval+point[0][0]
    Mid_1=xval/len(cont)
    Mid_2=yval/len(cont)
    Mid.append([Mid_1,Mid_2])
    xval=0
    yval=0

#Utworzenie maski 
img_masked=img_ORG.copy()
img_masked[drawing6_Centers!=255]=0

cv2.imshow("ladnie odesparowane",img_masked)
img_masked_hsv=cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV)

#ROZDZIELANIE KOLORU
(H,_,_) = cv2.split(img_masked_hsv)  


#Patrzymy na H, oraz na punkty srodka i oceniamy kolor w około
Suma=0
n=licznik_nazwy*100
for point in Mid:
    zielony=0
    Ymax=int(point[0]+radius+2)
    Ymin=int(point[0]-radius-2)
    Xmax=int(point[1]+radius+2)
    Xmin=int(point[1]-radius-2)
    img=img_masked[Ymin:Ymax,Xmin:Xmax]
    #KOLOR ZIELONY H[Ymin:Ymax,Xmin:Xmax]
    n1 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<35)
    n2 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<41)
    number_of_green_pix=n2-n1
    
    
    #KOLOR NIEBIESKI 
    n1 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<100)
    n2 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<106)
    number_of_blue_pix=n2-n1
    #KOLOR ZOLTY (NAJGORSZY)
    n1 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<20)
    n2 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<26)
    number_of_yellow_pix=n2-n1     
    #KOLOR CZERWONY
    n1 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<175)
    n2 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<181)
    number_of_red_pix=n2-n1
    #KOLOR FIOLET
    n1 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<145)
    n2 = np.sum(H[Ymin:Ymax,Xmin:Xmax]<151)
    number_of_purple_pix=n2-n1  
    #PRZYPISANIE ETYKIET
    n+=1
    if number_of_green_pix>400:
        point.append("green")
        Suma+=20000
        cv2.imwrite(f"do_sieci/zielony/{n}.png",img )
        
    elif number_of_blue_pix>500:
        point.append("blue")
        Suma+=10000
        cv2.imwrite(f"do_sieci/niebieski/{n}.png",img )
        
    elif number_of_purple_pix>200:
        point.append("purple")
        Suma+=50000
        cv2.imwrite(f"do_sieci/fiolet/{n}.png",img )
        
    elif number_of_red_pix>200:
        point.append("red")
        Suma+=5000
        cv2.imwrite(f"do_sieci/czerwony/{n}.png",img )
        
    elif number_of_yellow_pix>400:
        point.append("yellow")
        Suma+=100000
        cv2.imwrite(f"do_sieci/zolty/{n}.png",img )
    else:
        point.append("grey")
        Suma+=1000
        cv2.imwrite(f"do_sieci/szary/{n}.png",img )
#EFEKT KLASYFIKACJI

img_classified=img_ORG.copy()
colors=[[0,255,0],[255,0,0],[230,230,250],[0,0,255],[130,0,75],[100,100,100]]
for point in Mid:
    
    if point[2]=="green":
        Kolor=colors[0]
    elif point[2]=="blue":
        Kolor=colors[1]
    elif point[2]=="yellow":
        Kolor=colors[2]
    elif point[2]=="red":
        Kolor=colors[3]
    elif point[2]=="purple":
        Kolor=colors[4]
    elif point[2]=="grey":
        Kolor=colors[5]
    img_classified=cv2.circle(img_classified, [int(point[1]),int(point[0])], radius,Kolor,4 )

#WYSWIETLENIE WYNIKOW
print(Suma)
cv2.imshow("gotowe",img_classified)
    
cv2.waitKey()
cv2.destroyAllWindows() 