# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 22:24:49 2020

@author: Acc
"""

import numpy as np
import tensorflow as tf
from keras.layers import Input, Dense,Dropout,BatchNormalization
from keras.models import Model,Sequential
import matplotlib.pyplot as plt
import math as m
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
num=int(3e5)
g = 9.807 
velocity = np.random.uniform(1, 100,[num,1])
theta = np.random.uniform(0.01,m.pi/2,[num,1])
height = ( velocity * np.sin(theta) )**2 / ( 2 * g )
distance = velocity**2 * np.sin(2 * theta) / g
x=np.hstack((velocity,theta))
y=distance#np.hstack((height,distance))
y2=np.hstack((height,distance))
from sklearn import preprocessing
def norm(data):
    a= preprocessing.StandardScaler().fit(data)
    d=a.transform(data)
    m=a.mean_
    s=a.scale_
    v=a.var_
    return d,m,v,s
x,m1,v1,s1=norm(x.reshape(-1,2))
y,m2,v2,s2=norm(y.reshape(-1,1))
y2,_,_,_=norm(y2.reshape(-1,2))

model = Sequential()
model.add(Dense(1024, activation='relu', input_shape=(2,)))
model.add(Dense(256, activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(1))
model.compile(loss='mae',optimizer='adam')
import innvestigate
from tqdm import tqdm 


def pp(tk):
    xx=x[:15000]
    yy=y2[:15000]
    analyzer = innvestigate.create_analyzer("lrp.z",model)
    logg=[]
    for i in range(len(xx)):
        a = analyzer.analyze(xx[i].reshape(-1,2))
        logg.append(a)
    gg=np.array(logg).reshape(-1,2)
    d3,_,_,_=norm(gg.reshape(-1,2))

    fig,axes=plt.subplots(nrows=2,ncols=2,figsize=(8,8),dpi=200)
    axes[0,0].scatter(xx[:,0],xx[:,1],c=d3[:,0],s=0.9)
    axes[0,1].scatter(xx[:,0],xx[:,1],c=d3[:,1],s=0.9)
    
    axes[1,0].scatter(yy[:,0],yy[:,1],c=d3[:,0],s=0.9)
    axes[1,1].scatter(yy[:,0],yy[:,1],c=d3[:,1],s=0.9)
    plt.savefig('2NN_hist_%d.png'%(tk))
pp(0)
    
for tk in tqdm(range(2000)):
    f=(tk)*128
    e=(tk+1)*128
    model.train_on_batch(x[f:e],y[f:e])
    if tk%5==0:
        pp(tk+1)

    
    