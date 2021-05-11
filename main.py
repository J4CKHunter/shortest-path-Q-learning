from tkinter import*
import random
from numpy import * 
from copy import deepcopy
startSatir = ""
startSutun = ""
endSatir = ""
endSutun = ""
root = Tk()
root.title('Q-Learnig ile Yol Planlaması')
root.geometry('800x800')
root.resizable(width = FALSE, height = FALSE)

# learning rate
ALPHA = 0.03
# discount factor
GAMMA = 0.95
# number of epochs for training
EPOCHS = 10000
# maximum number of steps per epoch
MAXIMUM_STEPS = 100
MOVES = ['L', 'U', 'R', 'D']

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
        startSatir = mylist1[0]
        startSutun = mylist1[1]
        endSatir = mylist2[0]
        endSutun = mylist2[1]
        obstacleMatrix[int(startSatir)][int(startSutun)] = 1
        obstacleMatrix[int(endSatir)][int(endSutun)] = 2
        number=int(startSutun)+1+(int(startSatir)*50)
        labelCount=0
        for label in buttons:
            labelCount = labelCount +1
            if(labelCount== number):
                label.config(bg="blue")
        
        number=int(endSutun)+1+(int(endSatir)*50)
        labelCount=0
        for label in buttons:
            labelCount = labelCount +1
            if(labelCount== number):
                label.config(bg="green")
    
    def startQlearning():
        file = open("matris.txt", "w")  
        class Maze:
            def __init__(self, q_table=None):
                self.maze = deepcopy(obstacleMatrix)
                self.final_state = self.get_position(2)  # position of the destination
                self.Q = q_table

            def get_position(self, symbol):
                for i in range(0, len(self.maze)):
                    for j in range(0, len(self.maze[i])):
                        if self.maze[i][j] == symbol:
                            return i, j

            def select_move(self, epsilon):
                """
                Selects the next move.
                It may be the one having the greatest Q value or a random one (allowing exploration of new paths)
                :param epsilon: exploration factor [0, 1]
                for values close to 1 it's more likely to choose a random action
                for values close to 0 it's more likely to choose the best move given by the Q table
                :return: next move (one of L, U, R, D)
                """
                if random.random() > 1 - epsilon:
                    return random.choice(self.get_possible_moves())
                else:
                    return self.get_best_q()

            def get_best_q(self):
                maximum = -float("inf")
                p = self.get_position(1)  # position of the agent
                best_moves = []
                for m in self.get_possible_moves():
                    if self.Q[p, m] == maximum:
                        best_moves.append(m)
                    if self.Q[p, m] > maximum:
                        maximum = self.Q[p, m]
                        best_moves = [m]
                return random.choice(best_moves)  # one of the best Q's for current state

            def get_reward(self):
                """
                Compute the reward for the current state
                :return: 1 if the agent has reached the final state, -1 otherwise
                """
                return -1 if self.get_position(1) != self.final_state else 1

            def get_possible_moves(self):
                """
                :return: list containing all the possible moves from the current state
                """
                p = self.get_position(1)
                moves = deepcopy(MOVES)

                # remove invalid moves
                if p[1] == 0 or self.maze[p[0]][p[1] - 1] == -1:
                    moves.remove('L')

                if p[0] == 0 or self.maze[p[0] - 1][p[1]] == -1:
                    moves.remove('U')

                if p[1] == len(self.maze[p[0]]) - 1 or self.maze[p[0]][p[1] + 1] == -1:
                    moves.remove('R')

                if p[0] == len(self.maze) - 1 or self.maze[p[0] + 1][p[1]] == -1:
                    moves.remove('D')

                return moves

            def update_maze(self, move):
                p = self.get_position(1)
                self.maze[p[0]][p[1]] = '0'  # old position of the agent

                # new position based on the move
                if move == 'U':
                    self.maze[p[0] - 1][p[1]] = 1

                if move == 'D':
                    self.maze[p[0] + 1][p[1]] = 1

                if move == 'L':
                    self.maze[p[0]][p[1] - 1] = 1

                if move == 'R':
                    self.maze[p[0]][p[1] + 1] = 1

            def training(self):
                """
                Performs training in order to find optimal values for the Q table
                """
                self.Q = {}
                for i in range(0, len(obstacleMatrix)):
                    for j in range(0, len(obstacleMatrix[i])):
                        for k in MOVES:
                            self.Q[(i, j), k] = 0

                epsilon = 1  # allow more exploration in the beginning of the training

                for _ in range(EPOCHS):
                    self.maze = deepcopy(obstacleMatrix)
                    s = self.get_position(1)
                    steps = 0
                    while (s != self.final_state) and steps < MAXIMUM_STEPS:
                        steps += 1
                        next_move = self.select_move(epsilon)
                        self.update_maze(next_move)

                        r = self.get_reward()
                        new_p = self.get_position(1)  # new position of the agent
                        best_q = self.get_best_q()

                        # update Q table using the TD learning rule
                        self.Q[s, next_move] += ALPHA * (r + GAMMA * self.Q[new_p, best_q] - self.Q[s, next_move])

                        s = self.get_position(1)
                        epsilon -= (epsilon * 0.001)  # decay the exploration factor

            def test(self):
                print("TEST")
                self.maze = deepcopy(obstacleMatrix)
                self.print_maze()
                s = self.get_position(1)
                steps = 0
                while s != self.final_state:
                    steps += 1
                    self.update_maze(self.select_move(epsilon=0))
                    s = self.get_position(1)
                    self.print_maze()
                print("Agent reached destination in %d steps" % steps)

            def print_maze(self):
                     
                for element in self.maze:
                    file.write(str(element))
                    print(element)
                file.write("\n")
                file.write("\n")    
                print()

           

        if __name__ == "__main__":
            maze = Maze()
            maze.training()
            maze.test()
        
    b1 = Button(controlPanel, text = "Onayla",command=getTextInput ) 
    b2 = Button(controlPanel, text = "start",command=startQlearning ) 
    l1.pack()
    T1.pack()
    l2.pack()
    T2.pack()
    b1.pack()
    b2.pack()
    controlPanel.mainloop()

buttons = []
for i in range(buttonCount):
    for j in range(buttonCount):
        var = StringVar()
        label = Label( root, textvariable=var)
        var.set(int(random.random()*10))
        if(obstacleMatrix[i][j] == -1):
            label.config(bg="red")
        elif(obstacleMatrix[i][j] == 1):
            label.config(bg="blue")
        elif(obstacleMatrix[i][j] == 2):
            label.config(bg="green")
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
root.mainloop()