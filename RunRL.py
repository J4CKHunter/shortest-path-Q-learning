from collections import defaultdict
import time
import Functions
from GridWorld import GridWorld
from QLearning import QLearning
from matplotlib import pylab
from pylab import *
from tkinter import*
from numpy import *


if __name__ == "__main__":
    def control():
        controlPanel = Tk()
        controlPanel.title('Kontrol paneli')
        controlPanel.geometry('400x400')
        controlPanel.resizable(width=FALSE, height=FALSE)
        T1 = Text(controlPanel, height=1, width=10)
        T2 = Text(controlPanel, height=1, width=10)
        l1 = Label(controlPanel, text="Başlangıç noktasını seçiniz")
        l1.config(font=("Courier", 14))
        l2 = Label(controlPanel, text="Bitiş noktasını seçiniz")
        l2.config(font=("Courier", 14))

        def getTextInput():
            result1 = T1.get("1.0", "end")
            mylist1 = result1.split(',')
            result2 = T2.get("1.0", "end")
            mylist2 = result2.split(',')
            startSatir = mylist1[0]
            startSutun = mylist1[1]
            endSatir = mylist2[0]
            endSutun = mylist2[1]
            controlPanel.destroy()
            
            
            
            
            grid_world = GridWorld(50,50,int(startSutun),int(startSatir),int(endSutun),int(endSatir))
            Functions.create_random_obstacles(grid_world, 0.3)
            grid_world.scan_grid_and_generate_graph()
            grid_world.print_graph()
            grid_world.create_grid_ui(grid_world.m, grid_world.n, (grid_world.start_x, grid_world.start_y),
                                    (grid_world.end_x, grid_world.end_y), grid_world.obstacles)
            grid_world.print_grid()

            QL = QLearning(list(range(4)))

            scores, episodes, steps = [], [], []
            list_x = []
            list_y = []

            number_of_episodes = 10
            for episode in range(number_of_episodes):
                step = 0
                score = 0
                state = grid_world.reset()
                grid_world.is_visited = [[0] * grid_world.m for temp in range(grid_world.n)]
                list_x.clear()
                list_y.clear()
                while True:
                    grid_world.render()

                    action = QL.get_action(str(state))
                    next_state, reward, done = grid_world.step(action)

                    QL.learn(str(state), action, reward, str(next_state))
                    if reward != 0:
                        print("<state:{0} , action:{1} , reward:{2} , next_state:{3}>".format(
                            str(state), str(action), str(reward), str(next_state)))
                        list_x.append(state[0])
                        list_y.append((state[1]))

                    grid_world.is_visited[state[0]][state[1]] += 1
                    state = next_state
                    score += reward
                    step += 1

                    if done:
                        scores.append(score)
                        episodes.append(episode)
                        steps.append(step)

                        pylab.clf()

                        pylab.plot(episodes, scores, 'b')
                        pylab.title("Episode via Cost")
                        pylab.xlabel("Episodes")
                        pylab.ylabel("Costs")
                        pylab.savefig("./EpisodeViaCosts.png")

                        pylab.clf()

                        pylab.plot(episodes, steps, 'b')
                        pylab.title("Episode via Step")
                        pylab.xlabel("Episodes")
                        pylab.ylabel("Steps")
                        pylab.savefig("./EpisodeViaStep.png")

                        print("x list")
                        print(list_x)
                        print("y list")
                        print(list_y)

                        break

            print(QL.q_table)
            grid_world.print_final_route(list_x,list_y)
            
            
            
        b1 = Button(controlPanel, text="Onayla", command=getTextInput)
        l1.pack()
        T1.pack()
        l2.pack()
        T2.pack()
        b1.pack()
        controlPanel.mainloop()
    control()
   
