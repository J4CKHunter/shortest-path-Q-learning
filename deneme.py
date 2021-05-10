import random
from numpy import *

#obstacleMatrix = [[1, 0, 1],[1, 1, 0]]

matrixWidth=3
QmatrixWidth=matrixWidth*matrixWidth
#  path =1 obstacle= 0
obstacleMatrix = zeros((matrixWidth, matrixWidth))
for i in range(matrixWidth):
    for j in range(matrixWidth):
        obstacleMatrix[i][j] = 1
        
obstacleCount= (int)((matrixWidth/100)*30)
for i in range(obstacleCount):
    number1 = int(random.random()*matrixWidth)
    number2 = int(random.random()*matrixWidth)
    obstacleMatrix[number1][number2] = 0

qmatrix = zeros((QmatrixWidth, QmatrixWidth))
for i in range(QmatrixWidth):
    for j in range(QmatrixWidth):
        qmatrix[i][j] = 0


for i in range(QmatrixWidth):
    for j in range(QmatrixWidth):
        y= (int)(i/matrixWidth)
        x= (i-(y*matrixWidth))
        if(obstacleMatrix[y][x] == 1):#Kendi bulunduğumuz yer
            qmatrix[i][i] = 1
            
        
        if(x<(matrixWidth-1)):
            if(obstacleMatrix[y][x+1] == 1 ):#Kendi bulunduğumuz yer x düzleminde bir sağı
                konum=(x)+(y+1)+((matrixWidth-1)*y)
                qmatrix[i][konum] = 1
         
        if(x>0):    
            if(obstacleMatrix[y][x-1] == 1 ):#Kendi bulunduğumuz yer x düzleminde bir solu
                konum=(x-1)+(y)+((matrixWidth-1)*y)
                qmatrix[i][konum] = 1
        
        if(y>0): 
            if(obstacleMatrix[y-1][x] == 1 ):#Kendi bulunduğumuz yer y düzleminde bir üstü
                konum=(x)+((y)-1)+((matrixWidth-1)*(y-1))
                qmatrix[i][konum] = 1
        
        if(y<(matrixWidth-1)):
            if(obstacleMatrix[y+1][x] == 1 ):#Kendi bulunduğumuz yer y düzleminde bir altı
                konum=(x)+((y)+matrixWidth)+((matrixWidth-1)*y)
                qmatrix[i][konum] = 1



print("obstacleMatrix")
for i in range(matrixWidth):
    for j in range(matrixWidth):
        print(obstacleMatrix[i][j], end="")
        print("  ",end="")
    print("\n")

print("Qmatrix")
for i in range(QmatrixWidth):
    for j in range(QmatrixWidth):
        print(qmatrix[i][j], end="")
        print("  ",end="")
    print("\n")
