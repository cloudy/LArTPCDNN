from DLTools.ModelWrapper import *

from keras.layers.merge import concatenate
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation
from keras.layers import  BatchNormalization,Dropout,Flatten, Input
from keras.models import model_from_json

class FullyConnectedClassification(ModelWrapper):
    def __init__(self, Name, input_shape, width=0, depth=0, BatchSize=2048,
                 N_classes=100, init=0, BatchNormalization=False, Dropout=False,
                 NoClassificationLayer=False,
                 activation='relu',**kwargs):

        super(FullyConnectedClassification, self).__init__(Name,**kwargs)

        self.width=width
        self.depth=depth
        self.input_shape=input_shape
        self.N_classes=N_classes
        self.init=init

        self.Dropout=Dropout

        self.BatchSize=BatchSize
        self.BatchNormalization=BatchNormalization
        self.Activation=activation
        self.NoClassificationLayer=NoClassificationLayer
        
        self.MetaData.update({ "width":self.width,
                               "depth":self.depth,
                               "Dropout":self.Dropout,
                               "BatchNormalization":BatchNormalization,
                               "input_shape":self.input_shape,
                               "N_classes":self.N_classes,
                               "init":self.init})
    def Build(self):
        input=Input(self.input_shape[1:])
        modelT = Flatten(input_shape=self.input_shape)(input)

#        model.add(Dense(self.width,init=self.init))
        modelT = (Activation('relu')(modelT))

        for i in xrange(0,self.depth):
            if self.BatchNormalization:
                modelT=BatchNormalization()(modelT)

            modelT=Dense(self.width,kernel_initializer=self.init)(modelT)
            modelT=Activation(self.Activation)(modelT)

            if self.Dropout:
                modelT=Dropout(self.Dropout)(modelT)

        if not self.NoClassificationLayer:
            modelT=Dense(self.N_classes, activation='softmax',kernel_initializer=self.init)(modelT)

        self.inputT=input
        self.modelT=modelT
        
        self.Model=Model(input,modelT)

class MergerModel(ModelWrapper):
    def __init__(self, Name, Models, N_Classes, init, **kwargs):
        super(MergerModel, self).__init__(Name,**kwargs)
        self.Models=Models
        self.N_Classes=N_Classes
        self.init=init
        
    def Build(self):

        MModels=[]
        MInputs=[]
        for m in self.Models:
            MModels.append(m.modelT)
            MInputs.append(m.inputT)
        if len(self.Models)>0:
            print "Merged Models"
            modelT=concatenate(MModels)#(modelT)
            
        modelT=Dense(self.N_Classes, activation='softmax',kernel_initializer=self.init)(modelT)
        

        self.modelT=modelT
        
        self.Model=Model(MInputs,modelT)

class Model2DViewsTo3D(ModelWrapper):
    def __init__(self, Name, View1, View2, width=0, depth=0, BatchSize=2048, N_Classes,
                 init=0, BatchNormalization=False, Dropout=False, **kwargs):
        super(MergerModel, self).__init__(Name,**kwargs)
        
        
        self.width=width
        self.depth=depth
        self.init=init
        
        self.Dropout=Dropout
        self.BatchSize=BatchSize
        self.BatchNormalization=BatchNormalization
        
        self.input1_shape = View1.shape
        self.input2_shape = View2.shape
        self.N_Classes = N_Classes
        
        self.MetaData.update({ "width":self.width,
                               "depth":self.depth,
                               "Dropout":self.Dropout,
                               "BatchNormalization":BatchNormalization,
                               "input1_shape":self.input1_shape,
                               "input2_shape":self.input2_shape,
                               "N_classes":self.N_classes,
                               "init":self.init})

    def Build(self):
        input1=Input(self.input1_shape)
        input2=Input(self.input2_shape)
        input1 = Flatten(input_shape=self.input1_shape)(input1)
        input2 = Flatten(input_shape=self.input2_shape)(input2)
        modelT = concatenate([input1, input2])
        
        #model.add(Dense(self.width,init=self.init))
        modelT = (Activation('relu')(modelT))

        for i in xrange(0,self.depth):
            if self.BatchNormalization:
                modelT=BatchNormalization()(modelT)

            modelT=Dense(self.width,kernel_initializer=self.init)(modelT)
            modelT=Activation(self.Activation)(modelT)

            if self.Dropout:
                modelT=Dropout(self.Dropout)(modelT)

        if not self.NoClassificationLayer:
            modelT=Dense(self.N_classes, activation='softmax',kernel_initializer=self.init)(modelT)
        
        self.Model=Model(input,modelT)
