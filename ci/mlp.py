# -*- coding: utf-8 -*-

# ########################## Copyrights and license ############################
#                                                                              #
# Author: Bongtrop(Pongsakorn Sommalai) <bongtrop@gmail.com>                   #
# Date: Dec 20, 2014														   #
# Detail: Muti Layer Perceptron												   #
#                                                                              #
# ##############################################################################

import math
import random
import json
import copy

random.seed(0)

SIGMOID = 0
TANH = 1

def rand(a, b):
  return (b-a)*random.random() + a

def randNet(layer, type=SIGMOID):
  bias = []
  for l in range(0, len(layer)):
    bias.append([])
    for j in range(0, layer[l]):
      bias[l].append(rand(-0.2, 0.2))

  weight = []
  weight.append([])

  for l in range(1, len(layer)):
    weight.append([])
    for i in range(0, layer[l-1]):
      weight[l].append([])
      for j in range(0, layer[l]):
        weight[l][i].append(rand(-0.2, 0.2))

  return net(layer, weight, bias, type)

def json2net(filename):
  fr = open(filename, "r")
  ann = json.load(fr)
  layer = ann[0]
  weight = ann[1]
  bias = ann[2]
  type = ann[3]

  return net(layer, weight, bias, type)

class net:
  def __init__(self, layer, weight, bias, type=SIGMOID, filename=None):
    self.type = type
    self.layer = layer
    self.weight = weight
    self.bias = bias
    self.node = []
    for i in range(0, len(layer)):
      self.node.append([0]*layer[i])

  def _func(self, x):
    if self.type==SIGMOID:
      return 1/(1+math.exp(-x))
    else:
      return math.tanh(x)

  def process(self, input):
    if len(input)!=self.layer[0]:
      raise ValueError('wrong number of inputs')

    self.node[0] = input
    for l in range(1, len(self.layer)):
      self.node[l] = copy.deepcopy(self.bias[l])
      for i in range(0,self.layer[l]):
        for j in range(0,self.layer[l-1]):
          self.node[l][i] = self.node[l][i] + self.node[l-1][j] * self.weight[l][j][i]

        self.node[l][i] = self._func(self.node[l][i])

  def setWeight(self, l, j, i, w):
    self.weight[l][j][i] = w

  def getWeight(self, l, j, i):
    return self.weight[l][j][i]

  def setBias(self, l, i, b):
    self.bias[l][i] = b

  def getBias(self, l, i):
    return self.bias[l][i]

  def getNode(self, l, i):
    return self.node[l][i]

  def getLayer(self):
    return self.layer

  def getType(self):
    return self.type

  def getOutput(self):
    return [x for x in self.node[-1]]

  def save(self, filename):
    ann = [self.layer, self.weight, self.bias, self.type]
    fw = open(filename, "w")
    json.dump(ann, fw)

  def load(self, filename):
    fr = open(filename, "r")
    ann = json.load(fr)
    self.layer = ann[0]
    self.weight = ann[1]
    self.bias = ann[2]
    self.type = ann[3]

class backpropagation:
  def __init__(self, net, learning_rate=0.1, momentum=0.1):
    self.type = net.getType()
    self.net = net
    self.lr = learning_rate
    self.m = momentum
    self.layer = net.getLayer()
    self.lc = [[[0]*max(self.layer)]*max(self.layer)]*len(self.layer)

  def _dfunc(self, y):
    if self.type==SIGMOID:
      return y * (1.0 - y)
    else:
      return 1.0 - y**2

  def setLearningRate(self,x):
    self.lr = x

  def setMomentum(self, x):
    self.m = x

  def train(self, input, target):
    if len(target)!=self.layer[-1]:
      print len(target)
      print self.layer[-1]
      raise ValueError('Wrong number of target values')

    self.net.process(input)

    nlayer = len(self.layer)

    delta = []
    for i in range(0, nlayer):
      delta.append([0.0] * self.layer[i])

    for i in range(0,self.layer[nlayer-1]):
      node = self.net.getNode(nlayer-1, i)
      error = target[i] - node
      delta[nlayer-1][i] = self._dfunc(node) * error

    for l in range(nlayer-2, 0, -1):
      for i in range(0, self.layer[l]):
        error = 0.0
        for j in range(0, self.layer[l+1]):
          error = error + delta[l+1][j] * self.net.getWeight(l+1, i, j)

        delta[l][i] = self._dfunc(self.net.getNode(l,i)) * error

    for l in range(nlayer-2, -1, -1):
      for i in range(0, self.layer[l]):
        for j in range(0, self.layer[l+1]):
          change = delta[l+1][j] * self.net.getNode(l, i)
          w = self.net.getWeight(l+1, i, j) + self.lr * change + self.m * self.lc[l+1][i][j]
          self.net.setWeight(l+1, i, j, w)
          self.lc[l+1][i][j] = change

      for i in range(0, self.layer[l+1]):
        b = self.net.getBias(l+1, i) + delta[l+1][i]
        self.net.setBias(l+1, i, b)


    error = 0.0
    for i in range(0, len(target)):
      error = error + 0.5 * (target[i] - self.net.getNode(nlayer-1, i))**2

    return error
