from tkinter import*
import random
from numpy import * 

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
    Fact = """12,13"""
    b1 = Button(controlPanel, text = "Onayla", )
    l1.pack()
    T1.pack()
    l2.pack()
    T2.pack()
    b1.pack()
    T1.insert(END, Fact)
    T2.insert(END, Fact)
    controlPanel.mainloop()
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

control()
root.maxsize(800, 800)
root.mainloop()
