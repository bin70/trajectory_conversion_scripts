#!/usr/bin/env python3
# encoding: utf-8

import os
import numpy as np
import argparse

def quaternion_to_rotation_matrix(quat):
    q = quat.copy()
    n = np.dot(q, q)
    if n < np.finfo(q.dtype).eps:
        return np.identity(4)
    q = q * np.sqrt(2.0 / n)
    q = np.outer(q, q)
    rot_matrix = np.array(
        [[1.0 - q[2, 2] - q[3, 3], q[1, 2] + q[3, 0], q[1, 3] - q[2, 0], 0.0],
         [q[1, 2] - q[3, 0], 1.0 - q[1, 1] - q[3, 3], q[2, 3] + q[1, 0], 0.0],
         [q[1, 3] + q[2, 0], q[2, 3] - q[1, 0], 1.0 - q[1, 1] - q[2, 2], 0.0],
         [0.0, 0.0, 0.0, 1.0]],
        dtype=q.dtype)
    return rot_matrix.T

def get_transform(line):
    position = np.array([0,1,2], dtype=float) # 默认是int，必须指定float
    for i in range(2,5): # 2,3,4
        position[i-2] = float(line.split(' ')[i]) 

    orientation = np.array([0,1,2,3], dtype=float)
    for i in range(5,8):
        orientation[i-4] = float(line.split(' ')[i])
    orientation[0] = float(line.split(' ')[8])

    T = quaternion_to_rotation_matrix(orientation)
    
    for i in range(0,3):
        T[i, 3] = position[i]
    
    return T[0:3, :]

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--input_file", type=str, default='./traj_with_timestamp.txt', help="轨迹文件路径")
parser.add_argument("-o", "--output_path", type=str, default='.', help="转换结果保存路径")
parser.add_argument("-k", "--skip_lines", type=int, default=3, help="需跳过的文件头行数")
parser.add_argument("-b", "--begin_line", type=int, default=0, help="开始转换的行数")
parser.add_argument("-e", "--end_line", type=int, default=3, help="结束转换的行数")
parser.add_argument("-g", "--mapping_gap", type=int, default=2, help="建图时的位姿间隔")
args = parser.parse_args()

cnt = 0
cnt2 = 0
# output_file = os.path.join(args.output_path, str(args.begin_line)+"_"+str(args.end_line)+".txt")
output_file = os.path.join(args.output_path, "poses.txt")

if os.path.exists(output_file) == True:
    print "文件" + output_file + "已存在!"
    exit()

for line in open(args.input_file, "r"):
    if cnt >= args.skip_lines: 
        id = int(line.split(' ')[1])
        if id > args.end_line:
            break
        cnt2 = cnt2 + 1
        if id >= args.begin_line:
            T = get_transform(line)
            new_line = np.reshape(T, [1, 12])
            with open(output_file, "a") as out_file:
                np.savetxt(out_file, new_line, delimiter=' ')
    cnt = cnt + 1

print "Done!"
print "Save " + str(cnt2) + " lines to " + output_file + "."
