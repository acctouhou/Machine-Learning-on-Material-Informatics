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
from keras import regularizers
def data():
    
    num=int(1e5)
    g = 9.807 
    velocity = np.random.uniform(1, 100,[num,1])
    theta = np.random.uniform(0.01,m.pi/2,[num,1])
    height = ( velocity * np.sin(theta) )**2 / ( 2 * g )
    distance = velocity**2 * np.sin(2 * theta) / g
    x=np.hstack((velocity,theta))
    y=np.hstack((height,distance))
    from sklearn import preprocessing
    def norm(data):
        a= preprocessing.StandardScaler().fit(data)
        d=a.transform(data)
        m=a.mean_
        s=a.scale_
        v=a.var_
        return d,m,v,s
    x1,m1,v1,s1=norm(x.reshape(-1,2))
    y1,m2,v2,s2=norm(y.reshape(-1,2))
    index=np.arange(num)
    np.random.shuffle(index)
    x_train, y_train, x_test, y_test=x1[index[int(num*0.2):]],y1[index[int(num*0.2):]],x1[index[:int(num*0.2)]],y1[index[:int(num*0.2)]]
    return x_train, y_train, x_test, y_test
from hyperas import optim
from hyperas.distributions import choice, uniform
from hyperopt import Trials, STATUS_OK, tpe
from keras import optimizers

def create_model(x_train, y_train, x_test, y_test):
    d1={{choice([64,128,256,512,1024,2048])}}
    d2={{choice([64,128,256,512,1024,2048])}}
    d3={{choice([64,128,256,512,1024,2048])}}
    d4={{choice([64,128,256,512,1024,2048])}}
    act={{choice(['relu','sigmoid','tanh'])}}
    bn={{choice([0,1])}}
    c1={{uniform(0, 0.4)}}
    c2={{uniform(0, 0.4)}}
    c3={{uniform(0, 0.4)}}
    opt={{choice([optimizers.Adamax(),optimizers.RMSprop(),optimizers.Adam(),optimizers.SGD()])}}
    batch={{choice([64,128,256,512,1024,2048])}}
    model = Sequential()
    model.add(Dense(d1, activation=act, input_shape=(2,)))
    if bn==1:
        model.add(BatchNormalization())    
    #model.add(BatchNormalization())                                   BN
    #model.add(Dense(1024, activation='relu', kernel_regularizer=regularizers.l2(0.01)))       L2
    #model.add(Dropout(0.2))   
    model.add(Dense(d2, activation=act))
    model.add(Dropout(c1)) 
    if bn==1:
        model.add(BatchNormalization())
    model.add(Dense(d3, activation=act))
    model.add(Dropout(c2)) 
    if bn==1:
        model.add(BatchNormalization())
    model.add(Dense(d4, activation=act))
    model.add(Dropout(c3)) 
    if bn==1:
        model.add(BatchNormalization())
    model.add(Dense(2))
    
    import keras.backend as K

    model.compile(loss='mse',optimizer=opt)
    result =model.fit(x_train, y_train,
            validation_data=(x_test, y_test),
            epochs=100,batch_size=batch, verbose=0)
    return {'loss': result.history['val_loss'][-1], 'status': STATUS_OK, 'model': model}
gg=Trials()
best_run, best_model = optim.minimize(model=create_model,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=100,
                                          trials=gg)