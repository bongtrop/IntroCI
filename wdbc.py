import copy
import math
import numpy as np

from ci import mlp
from ci import ga
from ci import helper

def fitness(code, dataset, layer):
    nhidden = int(code[0])
    hidden1 = int(code[1])
    hidden2 = int(code[2])

    weight = []
    weight.append([])

    c = 0
    for l in range(1, len(layer)):
        weight.append([])
        for i in range(0, layer[l-1]):
            weight[l].append([])
            for j in range(0, layer[l]):
                weight[l][i].append(code[c])
                c+=1

    bias = []
    for l in range(0, len(layer)):
        bias.append([])
        for j in range(0, layer[l]):
            bias[l].append(code[c])
            c+=1

    net = mlp.net(layer, weight, bias)
    cor = 0.0
    s = 0.0
    for d in dataset:
        target = d[0]
        inp = d[1:31]
        net.process(inp)
        if abs(target - net.getOutput()[0])<0.5:
            cor+=1.0

        s+=1.0

    return cor/s


f = open("wdbc.data", "r")
fw = open("report/wdbc2.txt", "a")
lines = f.readlines()

datas = []
for line in lines:
    words = line.split(",")
    datas.append([float(word) for word in words])

datas = np.array(datas)

for i in range(1, 31):
    datas[:,i] = (datas[:,i] - np.min(datas[:,i]))/(np.max(datas[:,i])-np.min(datas[:,i]))

datas = datas.tolist()

floods = helper.crossvalidation(datas, 0.1, shuffer=True)

pptNet = [[30, 4, 1], [30, 8, 1], [30, 16, 1], [30, 32, 1]]
mrs = [0.01, 0.05, 0.1]
crs = [0.1, 0.25, 0.5]

for pn in pptNet:
    for cr in crs:
        for mr in mrs:

            s_cor = 0
            for i in range(0, floods.state):
                train = floods.getTrain(i)
                test = floods.getTest(i)

                print "Net Structure " + str(pn) + " Mutation Rate " + str(mr) + " Crossover Rate " + str(cr) + " Flood " + str(i+1)
                fw.write("Net Structure " + str(pn) + " Mutation Rate " + str(mr) + " Crossover Rate " + str(cr) + " Flood " + str(i+1) + "\n")

                prototype_gene = []

                for nouse in range(pn[0]*pn[1] + pn[1]*pn[2] + pn[0] + pn[1] + pn[2]):
                    prototype_gene.append([-2.0, 2.0])

                g = ga.realga(prototype_gene, fitness, crossover_rate=cr, mutation_rate=mr, ngen=50)
                best, best_code = g.run(train, pn)

                cor = fitness(best_code, test, pn)
                s_cor+=cor

                print "Ratio Correctly " + str(cor)
                fw.write("Ratio Correctly " + str(cor) + "\n")

            print "Mean Correctly is " + str(s_cor/floods.state)
            print ""
            fw.write("Mean Correctly is " + str(s_cor/floods.state) + "\n\n")
