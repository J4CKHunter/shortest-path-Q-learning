from tkinter import*
import random
from numpy import * 

  
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

for i in range(buttonCount):
    number1 =int(random.random()*50)
    number2 =int(random.random()*50)
    if(obstacleMatrix[number1][number2] == 0 ):
        obstacleMatrix[number1][number2] = 1
        break

for i in range(buttonCount):
    number1 =int(random.random()*50)
    number2 =int(random.random()*50)
    if(obstacleMatrix[number1][number2] == 0):
        obstacleMatrix[number1][number2] = 2
        break

buttons = []
for i in range(buttonCount):
    for j in range(buttonCount):
        countNumber = countNumber
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


root.maxsize(800, 800)
root.mainloop()