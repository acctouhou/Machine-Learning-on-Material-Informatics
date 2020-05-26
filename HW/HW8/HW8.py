# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:05:28 2020

@author: Acc
"""
import matplotlib.pyplot as plt
import numpy as np 
def islands(img):
        i=0
        for x in range(len(img)):
            for y in range(len(img[0])):
                if img[x][y] == 1:
                    size=dfs(img,x,y,0)
                    i+=1
                    print('island:%d  size:%d'%(i,size+1))
        
def dfs(img, i, j,count):
    dirs = [[-1, 0], [0, 1], [0, -1], [1, 0]]
    img[i][j] = 0
    for dir in dirs:
        nx, ny = i + dir[0], j + dir[1]
        if nx >= 0 and ny >= 0 and nx < len(img) and ny < len(img[0]):
            if img[nx][ny] == 1:
                count=dfs(img,nx,ny,count+1)
    return count
img=np.random.randn(10,10)
th=0
img[img>th]=1
img[img<th]=0
islands(img)
#%%
#big o test   
import time
def islands(img):
        i=0
        for x in range(len(img)):
            for y in range(len(img[0])):
                if img[x][y] == 1:
                    size=dfs(img,x,y,0)
                    i+=1
                    #print('island:%d  size:%d'%(i,size+1))
        
def dfs(img, i, j,count):
    dirs = [[-1, 0], [0, 1], [0, -1], [1, 0]]
    img[i][j] = 0
    for dir in dirs:
        nx, ny = i + dir[0], j + dir[1]
        if nx >= 0 and ny >= 0 and nx < len(img) and ny < len(img[0]):
            if img[nx][ny] == 1:
                count=dfs(img,nx,ny,count+1)
    return count
log=[]
for i in range(1,8):
    i=10**i
    img=np.random.randn(int(i**0.5),int(i**0.5))
    th=0
    img[img>th]=1
    img[img<th]=0
    s0=time.time()
    
    islands(img)
    log.append(time.time()-s0)
log=np.array(log)
#%%
fig,axes=plt.subplots(nrows=1,ncols=2,figsize=(12,6),dpi=100)
n=[]
for i in range(1,8):
    n.append(10**i)
n=np.array(n)
axes[0].plot(n,log)
axes[1].plot(n,n/log)
axes[0].set_xlabel('N')
axes[1].set_xlabel('N')
axes[0].set_ylabel('Time')
axes[1].set_ylabel('N / Time')