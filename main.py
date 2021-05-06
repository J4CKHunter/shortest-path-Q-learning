from tkinter import*
import random
from numpy import * 

startX = ""
startY = ""
endX = ""
endY = ""
root = Tk()
root.title('Q-Learnig ile Yol Planlaması')
root.geometry('800x800')
root.resizable(width = FALSE, height = FALSE)

buttonCount= 50
countNumber=0
#startpoint =1 endpoint = 2 path =0 obstacle= -1
obstacleMatrix = zeros((50, 50))
for i in range(buttonCount):
    for j in range(buttonCount):
        obstacleMatrix[i][j] = 0

for i in range(750):
    number1 =int(random.random()*50)
    number2 =int(random.random()*50)
    obstacleMatrix[number1][number2] = -1
    

def control():
    
    controlPanel = Tk()
    controlPanel.title('Kontrol paneli')
    controlPanel.geometry('400x400')
    controlPanel.resizable(width = FALSE, height = FALSE)
    T1 = Text(controlPanel, height = 1, width = 10)
    T2 = Text(controlPanel, height = 1, width = 10)
    l1 = Label(controlPanel, text = "Başlangıç noktasını seçiniz")
    l1.config(font =("Courier", 14))
    l2 = Label(controlPanel, text = "Bitiş noktasını seçiniz")
    l2.config(font =("Courier", 14))
    def getTextInput():
        result1=T1.get("1.0","end")
        mylist1 = result1.split(',')
        result2=T2.get("1.0","end")
        mylist2 = result2.split(',')
        startX = mylist1[0]
        startY = mylist1[1]
        endX = mylist2[0]
        endY = mylist2[1]
        print(startX+ startY)
        obstacleMatrix[int(startX)][int(startY)] = 1
        obstacleMatrix[int(endX)][int(endY)] = 2
        number=int(startX)+(int(startY)*50)
        numberAsıl=0
           
        print(number)
        for label in buttons:
            numberAsıl = numberAsıl +1
            if(numberAsıl== number):
                label.config(bg="blue")
        
        number=int(endX)+(int(endY)*50)
        numberAsıl=0
        for label in buttons:
            numberAsıl = numberAsıl +1
            if(numberAsıl== number):
                label.config(bg="green")
        
    b1 = Button(controlPanel, text = "Onayla",command=getTextInput ) 
    l1.pack()
    T1.pack()
    l2.pack()
    T2.pack()
    b1.pack()
    controlPanel.mainloop()

buttons = []
for i in range(buttonCount):
    for j in range(buttonCount):
        if(obstacleMatrix[i][j] == -1):
            label.config(bg="red")
        elif(obstacleMatrix[i][j] == 1):
            label.config(bg="blue")
        elif(obstacleMatrix[i][j] == 2):
            label.config(bg="green")
        var = StringVar()
        label = Label( root, textvariable=var)
        var.set(int(random.random()*10))
        label.place(x=0, y=0)
        buttons.append(label)
        label.place(relx=0.02+(0.02*j), rely=0.02+(0.02*i), anchor='se')
        
f = open("engel.txt", "w")    
for i in range (buttonCount):
            for j in range (buttonCount):
                if(obstacleMatrix[i][j] == -1):
                    f.write(str(i) + ", " + str(j) + ", " + "K" + "\n") # K Obstacle
                else:
                    f.write(str(i) + ", " + str(j) + ", " + "B" + "\n") # B Not Obstacle     

control()
root.maxsize(800, 800)
root.mainloop()
