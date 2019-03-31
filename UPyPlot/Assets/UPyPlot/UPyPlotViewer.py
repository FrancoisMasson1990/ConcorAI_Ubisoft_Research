#! /usr/bin/python
#--------------------------------#
# Plot viewer for visualizing Unity script variables in realtime
#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure("UPyPlot Window")
fig.set_facecolor((0.63, 0.63, 0.63))

ax1 = fig.add_subplot(3,1,1)
ax1.set_facecolor((0.87, 0.87, 0.87))

ax2 = fig.add_subplot(3,2,1)
ax2.set_facecolor((0.87, 0.87, 0.87))

ax3 = fig.add_subplot(3,3,1)
ax3.set_facecolor((0.87, 0.87, 0.87))

def animate(i):
    pollData = open("plotting_cache\plot.txt","r").read()
    try: #try to unpack the data in the file, if for any reason it fails then just drop everything and return to start a new cycle.
        dataArray = pollData.split('\n')[1:]
        dataMeta = pollData.split('\n')[0].split(',')
    except:
        return

    print(len(dataArray))

    time = []
    speed_x = []
    speed_y = []
    speed_z = []

    try: # try to display this axis, if the data is corrupt then just skip it this frame.
        ax1.plot(time,speed_x)
        ax2.plot(time,speed_y)
        ax3.plot(time,speed_z)
    except:
        pass


if __name__ == "__main__":

    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.tight_layout()
    plt.show()