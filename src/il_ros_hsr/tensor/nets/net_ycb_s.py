"""
    Network takes in a image and outputs (x,y,theta,z)
    Model for net3
        conv
        relu
        fc
        relu
        fc
        tanh
"""


import tensorflow as tf
from il_ros_hsr.tensor import inputdata
import random
from il_ros_hsr.tensor.tensornet import TensorNet
#from alan.p_grasp_align.options import Grasp_AlignOptions as options
import time
import datetime

class Net_YCB_S(TensorNet):

    def __init__(self, options,channels=3):
        self.dir = "./net6/"
        self.name = "ycb"
        self.channels = channels
        self.Options = options
        self.sess = tf.Session()
        
        self.x = tf.placeholder('float', shape=[None,103,125,self.channels])
        self.y_ = tf.placeholder("float", shape=[None, 3])


        self.w_conv1 = self.weight_variable([7, 7, self.channels, 5])
        self.b_conv1 = self.bias_variable([5])

        self.h_conv1 = tf.nn.relu(self.conv2d(self.x, self.w_conv1) + self.b_conv1)


        conv_num_nodes = self.reduce_shape(self.h_conv1.get_shape())
        fc1_num_nodes = 60
        
        self.w_fc1 = self.weight_variable([conv_num_nodes, fc1_num_nodes])
        # self.w_fc1 = self.weight_variable([1000, fc1_num_nodes])
        self.b_fc1 = self.bias_variable([fc1_num_nodes])

        self.h_conv_flat = tf.reshape(self.h_conv1, [-1, conv_num_nodes])
        self.h_fc1 = tf.nn.relu(tf.matmul(self.h_conv_flat, self.w_fc1) + self.b_fc1)

        self.w_fc2 = self.weight_variable([fc1_num_nodes, 3])
        self.b_fc2 = self.bias_variable([3])

        self.y_out = tf.tanh(tf.matmul(self.h_fc1, self.w_fc2) + self.b_fc2)

        self.loss = tf.reduce_mean(.5*tf.sqrt(tf.square(self.y_out - self.y_)))
 

        self.train_step = tf.train.MomentumOptimizer(.003, .9)
        self.train = self.train_step.minimize(self.loss)


