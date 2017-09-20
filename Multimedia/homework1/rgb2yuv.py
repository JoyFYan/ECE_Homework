import cv2
import os
import numpy as np
from struct import *

V_PATH = 'video.mp4'
vcap =  cv2.VideoCapture(V_PATH)
fps = vcap.get(cv2.CAP_PROP_FPS)
size = (int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
        int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print 'fps:',fps,'size:',size

f = open('out_put1.yuv','wb')# 打开输出文件
WIDTH = 320
HEIGHT = 240
FPS_OUT = 15
# 变化矩阵
YUV_M = np.array([(0.299,0.587,0.114),(-0.169,-0.332,0.5),(0.5,-0.419,-0.0813)])
YUV_B = np.array([0,128,128])
FRAMES = 100 # 设置转换总帧数（未压缩文件太大）
fps_count = fps // FPS_OUT
f_count = 0
for f_num in xrange(FRAMES):
    success, frame = vcap.read()
    if f_count >= fps_count:
        f_count = 0
        continue
    else:
        f_count += 1
    if success != True:
        break
    resized = cv2.resize(frame,(WIDTH,HEIGHT))
    frame_size = int(HEIGHT * WIDTH * 1.5)
    out_put = np.zeros((frame_size),dtype = np.uint8)
    count = 0
    for i in xrange(HEIGHT):
        for j in xrange(WIDTH):
            ind = i * WIDTH + j
            temp = resized[i,j,:]
            temp[0] ,temp[2]= resized[i,j,:][2], resized[i,j,:][1]
            YUV = (np.dot(YUV_M, temp) + YUV_B)
            out_put[ind] = int(YUV[0])
            if (i % 2 == 0 and ind % 2 == 0):
                out_put[WIDTH * HEIGHT + count] = int(YUV[1])
                out_put[WIDTH * HEIGHT + WIDTH * HEIGHT/4 + count] = int(YUV[2])
                count += 1
    for b in out_put:
        f.write(pack("B", b))
f.close()
