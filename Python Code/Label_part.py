#! /usr/bin/python
#--------------------------------#
# Plot viewer for visualizing Unity script variables in realtime
#--------------------------------#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import json
from pandas.io.json import json_normalize
import math

if __name__ == "__main__":

    #Data = "./Data/record.json"
    Data = "./Data_Save/neutral.json"
    # Load the file 
    json_data = json.loads(open(Data).read())

    # Panda conversion
    df = pd.DataFrame.from_dict(json_normalize(json_data), orient='columns')

    key_ = ["time","speed.x","speed.y","speed.z","label"]
    #key_time = ["Time"]
    for j in key_:
        df[j] = 0.0

    for j in range(1,len(df)):
        df["time"][j] = (df["timestamp"][j] - df["timestamp"][j-1]) + df["time"][j-1]

    for j in range(len(df)):
        if (df["angles.x"][j]) > 180 :
            df["angles.x"][j] = df["angles.x"][j] - 360
        #if (df["angles.y"][j]) > 90 :
        #    df["angles.y"][j] = df["angles.y"][j] - 180
        if (df["angles.z"][j]) > 180 :
            df["angles.z"][j] = df["angles.z"][j] - 360
    
    ## Speed
    for j in range(1,len(df)):
        df["speed.x"][j] = np.abs((df["angles.x"][j] - df["angles.x"][j-1]))/ (df["time"][j] - df["time"][j-1])
        df["speed.y"][j] = np.abs((df["angles.y"][j] - df["angles.y"][j-1]))/ (df["time"][j] - df["time"][j-1])
        df["speed.z"][j] = np.abs((df["angles.z"][j] - df["angles.z"][j-1]))/ (df["time"][j] - df["time"][j-1])

    
    df_copy = df[df.columns[12:16]]
    number = np.linspace(0,39,40)
    col_names = []
    for col in number :
        col_names.append(str(int(col)))

    #col_names =  ['0','1','2','3','4','5','6','7','8','9','']
    my_df  = pd.DataFrame(columns = col_names)

    # sampling every 80 mesures corresponding to 2 sec to answer
    sampling = 40
    for ii in range(int(df_copy.shape[0]/sampling)):
        my_df.loc[len(my_df)] = df_copy["speed.y"][0:40]
    
    count = 0
    for j in range(0,len(my_df)):
        for l in col_names:
            my_df[l][j] = df_copy["speed.y"][count]
            count = count + 1

    my_df["label"] = 0
    
    ### CSV export

    ### yes is x speed
    ### no is y speed

    my_df.to_csv("Neutral_no_data.csv",encoding='utf-8', index=False)

    #fig = plt.figure("Head Movement")
    #fig.set_facecolor((1.0, 1.0, 1.0))

    #ax1 = fig.add_subplot(1,1,1)

    #ax1.plot(df['time'], df['angles.y'],'r-')
    #ax1.set(xlabel='time', ylabel='Speed x (degrés/sec)',title='Test 01')
    #ax1.grid()
    #plt.show()

    """    

    my_df  = pd.DataFrame(columns = col_names)

    # sampling every 10 mesures
    sampling = 10
    for ii in range(int(df_copy.shape[0]/sampling)):
        my_df.loc[len(my_df)] = df_copy["speed.y"][0:10]
    
    count = 0
    for j in range(0,len(my_df)):
        for l in col_names:
            my_df[l][j] = df_copy["speed.y"][count]
            count = count + 1

    my_df["label"] = 0
    ### CSV export

    my_df.to_csv("SpeedY_Esther_Epicerie.csv",encoding='utf-8', index=False)

    my_df  = pd.DataFrame(columns = col_names)

    # sampling every 10 mesures
    sampling = 10
    for ii in range(int(df_copy.shape[0]/sampling)):
        my_df.loc[len(my_df)] = df_copy["speed.z"][0:10]
    
    count = 0
    for j in range(0,len(my_df)):
        for l in col_names:
            my_df[l][j] = df_copy["speed.z"][count]
            count = count + 1
            
    my_df["label"] = 0
    ### CSV export

    my_df.to_csv("SpeedZ_Esther_Epicerie.csv",encoding='utf-8', index=False)

    fig = plt.figure("Head Movement")
    fig.set_facecolor((1.0, 1.0, 1.0))

    ax1 = fig.add_subplot(3,1,1)
    ax2 = fig.add_subplot(3,1,2)
    ax3 = fig.add_subplot(3,1,3)

    ax1.plot(df['time'], df['speed.x'],'r-')
    ax1.plot(df['time'], df['angles.x'],'r.')
    ax1.set(xlabel='time', ylabel='Speed x (degrés/sec)',title='Test 01')
    ax1.grid()

    ax2.plot(df['time'], df['speed.y'],'g-')
    ax2.plot(df['time'], df['angles.y'],'g.')
    ax2.set(xlabel='time', ylabel='Speed y (degrés/sec)',title='Test 01')
    ax2.grid()

    ax3.plot(df['time'], df['speed.z'],'b-')
    ax3.plot(df['time'], df['angles.z'],'b.')
    ax3.set(xlabel='time', ylabel='Speed z (degrés/sec)',title='Test 01')
    ax3.grid()

    plt.tight_layout()
    #plt.show()"""