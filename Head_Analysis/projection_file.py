"""
@2D_projection yaw/pitch/roll
@Francois Masson

"""

import numpy as np 
import pandas as pd 
import math
import sys 
import json
from pandas.io.json import json_normalize
from transformations.transformations import euler_from_quaternion, quaternion_from_euler
import matplotlib.pyplot as plt


def conversion(orientation_list):
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    return roll,pitch,yaw

def data_frame(src):
    # Load the file 
    json_data = json.loads(open(src).read())

    #Allow to deconstruct the nested dictionnary

    df = pd.DataFrame.from_dict(json_normalize(json_data), orient='columns')
    key_ = ["Roll","Pitch","Yaw","Time","Speed Roll","Speed Pitch","Speed Yaw"]
    #key_time = ["Time"]
    for j in key_:
        df[j] = 0.0
    
    for j in range(1,len(df)):
        df["Time"][j] = (df["timestamp"][j] - df["timestamp"][j-1]) + df["Time"][j-1]
    
    # Conversion from quaternion to Euler 
    for j in range(len(df)):
        orientation_list = [df['rotation.x'][j], df['rotation.y'][j], df['rotation.z'][j], df['rotation.w'][j]]
        roll,pitch,yaw = conversion(orientation_list)
        [df['Roll'][j], df['Pitch'][j], df['Yaw'][j]]=[roll,pitch,yaw]
    
    df['Roll'] = df['Roll']*180/math.pi
    df['Pitch'] = df['Pitch']*180/math.pi
    df['Yaw']= df['Yaw']*180/math.pi

    ## Speed
    for j in range(1,len(df)):
        df["Speed Roll"][j] = (df["Roll"][j] - df["Roll"][j-1])/ (df["Time"][j] - df["Time"][j-1])
        df["Speed Yaw"][j] = (df["Yaw"][j] - df["Yaw"][j-1])/ (df["Time"][j] - df["Time"][j-1])
        df["Speed Pitch"][j] = (df["Pitch"][j] - df["Pitch"][j-1])/ (df["Time"][j] - df["Time"][j-1])

    return df