import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import collections
import numpy as np
import serial as ser
import csv
import asyncio
from websockets.sync.client import connect

import asyncio
from websockets.sync.client import connect


from datetime import time

data=[]
t=[]
so=[]
co2=[]
pm=[]
t_read=0
so_read=0
co2_read=0
pm_read=0

def receiveLora():
    print("Connecting to localhost:8765:")
    with connect("ws://localhost:8765") as websocket:
        while(1)
            print("Waiting for message")
            try:
                data = websocket.recv()
                data_dict=json.loads(data)
                t_read= data_dict["utc_time"]
                so_read=float(data_dict["SO_ppm"])
                co2_read=float(data_dict["co2_ppm"])
                pm_read=float(data_dict["pm2.5"])
                break
            except:
                pass

def update(i):
    receiveLora()
    h_read=int(t[0:2])
    m_read=int(t[2:4])
    s_read=int(t[4:])
    t_read=time(h_read,m_read,s_read)

    #print(float(x.decode()))
    print("Updating plot")
    ylabel={0:"Sulfur Dioxide",1:"Carbon Dioxide",2:"PM2.5"}
    for i in range(0,2):
        data[i].popleft()
        if i==0:
            data[i].append( so_read )
        elif i==1:
            data[i].append( co2_read )
        elif i==2:
            data[i].append( pm_read )

        ax[i].cla()
        ax[i].set_xlabel('Time')
        ax[i].set_ylabel(ylabel[i])
        ax[i].set_title(ylabel[i] + " vs Time")
        ax[i].plot(t,data[i])

        ax[i].scatter(len(data[i])-1, data[i][-1])
        ax[i].text(len(data)-1, data[i][-1]+2, "{}".format(data[i][-1]))
        ax[i].set_ylim(0,max(data[i])+0.1*max(data[i])+0.0001)
        ax[i].set_xlim(t[0],t[0]+datetime.timedelta(seconds=60))

for i in range(0,3):
    data.append(collections.deque(np.zeros(30)))

fig,ax=plt.subplots(3,1)

print("Plotting...")

t=[]
c=[]
v=[]
p=[]

ani= FuncAnimation(fig,update,interval=1000)
plt.show()
