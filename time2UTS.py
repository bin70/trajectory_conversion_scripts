#!/usr/bin/python3
import numpy as np
import argparse

start = 1579166444385370
change_col = 8
parser = argparse.ArgumentParser()
parser.add_argument('--old', help='old traj path')
args = parser.parse_args()

# load label and id 前两列
label = np.loadtxt(args.old, usecols=[0,1], unpack=True, dtype=str)
label = np.transpose(label)

# load time 第10列
time = np.loadtxt(args.old, dtype=int, usecols=[9], unpack=True)
time = time+start
time = np.reshape(time, (time.shape[0], 1))

# load data 剩余
data = np.loadtxt(args.old, dtype=float, usecols=[2,3,4,5,6,7,8], unpack=True)
data = np.transpose(data)

# merge column
data = np.concatenate((label, data, time), axis=1) 
new = "GroundTruth_traj_with_unix_timestamp.txt"
np.savetxt(new, data, fmt="%s")

with open(new, 'r+') as f:
    content = f.read()        
    f.seek(0, 0) # start of the file
    f.write('# Date:2020/01/22\n# Data Format\n'
           +'# {iSAM_VERTEX, Frame Number, Position[x|y|z], Quaternion[qx|qy|qz|qw], Timestamp(us)}\n'
           +'# ===================================================================================================\n'
           + content)
