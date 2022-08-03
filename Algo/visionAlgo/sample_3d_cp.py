   #!/usr/bin/python3

# Copyright (C) 2020 pmdtechnologies ag
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.

"""This sample shows how to visualize the 3D data.

It uses Open3D (http://www.open3d.org/) to display the point cloud.
"""

import argparse

import roypy
import time
import queue
# from sample_camera_info import print_camera_info
from roypy_sample_utils import CameraOpener, add_camera_opener_options, select_use_case
#from roypy_platform_utils import PlatformHelper
import glob
import numpy as np
import open3d as o3d
import cv2
from scipy import stats
from PIL import Image
import math
import matplotlib.pyplot as plt
import pandas as pd
import os


place = 'SD/'
number = '5'
dst = 'data/2D/'+place+number
dst_binary = 'data/BINARY/'+place+number
dst_map = 'data/IMU1/'+place+number


def rm_all_files(dst):
    files = glob.glob('{}/*'.format(dst))
    for file in files:
        if os.path.isfile(file):
            os.remove(file)


clear_dst = False  # 为True时清除数据！！！
if clear_dst:
    print('!!!!!!!!!!!!!!!Remove all files in {}!!!!!!!!!!!!!!!!!!!!!'.format(dst))
    rm_all_files(dst)
    print('!!!!!!!!!!!!!!!Remove all files in {}!!!!!!!!!!!!!!!!!!!!!'.format(dst))
    rm_all_files(dst_binary)



# Lens parameters: 9
#     ('cx', 106.00597381591797)
#     ('cy', 87.65521240234375)
#     ('fx', 212.75160217285156)
#     ('fy', 212.75160217285156)
#     ('k1', 0.36301088333129883)
#     ('k2', -4.426482677459717)
#     ('k3', 7.897706508636475)
#     ('p1', 1.4385735466832732e-15)
#     ('p2', 2.1180871997723144e-15)




class MyListener(roypy.IDepthDataListener):
    def __init__(self, q):
        super(MyListener, self).__init__()
        self.queue = q
        self.figSetup = False
        self.firstTime = True


    def onNewData(self, data):
        pc = data.npoints ()
        #only select the three columns we're interested in
        px = pc[:,:,0]
        py = pc[:,:,1]
        pz = pc[:,:,2]
        stack1 = np.stack([px,py,pz], axis=-1)
        stack2 = stack1.reshape(-1, 3)

        self.queue.put(stack2)

        

def main ():
    #platformhelper = PlatformHelper()
    parser = argparse.ArgumentParser (usage = __doc__)
    add_camera_opener_options (parser)
    parser.add_argument ("--seconds", type=int, default=300, help="duration to capture data")
    options = parser.parse_args()
    opener = CameraOpener (options)
    cam = opener.open_camera ()
    #print_camera_info (cam)

    print("isConnected", cam.isConnected())
    print("getFrameRate", cam.getFrameRate())

    curUseCase = select_use_case(cam)

    # we will use this queue to synchronize the callback with the main
    # thread, as drawing should happen in the main thread
    q = queue.Queue()
    l = MyListener(q)
    cam.registerDataListener(l)

    print ("Setting use case : " + curUseCase)
    cam.setUseCase(curUseCase)
    n = 1
    map = np.memmap(dst_map + '/imu1.npy', dtype='float64', mode='r', shape=(9 * n + 1,))
    cam.startCapture()
    plt.ion()
    # create a loop that will run for a time (default 15 seconds)
    # process_event_queue (q, options.seconds)
    t_end = time.time() + options.seconds
    while time.time() < t_end:
        try:
            # try to retrieve an item from the queue.
            # this will block until an item can be retrieved
            # or the timeout of 1 second is hit
            if len(q.queue) == 0:
                item = q.get(True, 1)
            else:
                for i in range (0, len (q.queue)):
                    item = q.get(True, 1)
            t1 = time.time()
            item = item[np.all(item != 0, axis=1)]
            angle = map[0]

            t = map[-1]


            img,pcd_2d = pcd_to_binary_image(item,angle)
            m = len(pcd_2d[:,0])
            px = pcd_2d[0:m:6,0]
            py = pcd_2d[0:m:6, 1]
            # np.save('{}/{:.3f}.npy'.format(dst, t), pcd_2d)
            # cv2.imwrite('{}/{:.3f}.png'.format(dst_binary, t), img)


            plt.clf()
            plt.scatter(px,py)
            plt.pause(0.1)
            #print('max',max(item[:,0]))
            #print('min', min(item[:,0]))
            cv2.imshow('binary image', img)
            cv2.waitKey(1)
            t2 = time.time()
            print('cost time',t2-t1)

        except queue.Empty:
            # this will be thrown when the timeout is hit
            break

    cam.stopCapture()


def pcd_to_binary_image(data, angle):


    y = data[:, 1]
    x = data[:, 2][abs(y) < 0.01]
    z = data[:, 0][abs(y) < 0.01]   #降维



    img = np.zeros([100, 100])
    a1 = angle+87
    # theta = ((angle + 95) / 180) * np.pi #IMU测的欧拉角加个补偿，转成弧度
    theta = (a1 / 180) * np.pi #IMU测的欧拉角加个补偿，转成弧度


    x1 = (x * np.cos(theta) - z * np.sin(theta))     #坐标系转换
    z1 = (z * np.cos(theta) + x * np.sin(theta))
    pcd_x = x1[abs(x1) < 1]
    pcd_z = z1[abs(x1) < 1]

    #
    # plt.subplot(211)
    # plt.scatter(pcd_y, pcd_z)


    if np.any(pcd_x) :

        p = pcd_x
        q = pcd_z
        p -= min(p)
        q -= min(q)
        q += 1-max(q)

        # pcd_x -= min(pcd_x)
        # pcd_z -= min(pcd_z)
        # pcd_z += 1 - max(pcd_z)

        #
        # plt.subplot(212)
        # plt.scatter(p, q)
        # plt.show()

        for i in range(len(q)):
            if q[i] < 1 and q[i] > 0.01 and p[i] < 1 and p[i] > 0.01:
                p_int = int(100 * p[i])
                q_int = int(100 * q[i])
                img[q_int,p_int] = 1

        img = img * 255

        pcd_2d = np.zeros([len(p), 2])
        pcd_2d[:, 0] = pcd_x
        pcd_2d[:, 1] = -pcd_z

    else:
        pcd_2d = np.zeros((len(y),2))

    return img,pcd_2d






if __name__ == "__main__":

    main()
