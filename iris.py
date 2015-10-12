from ci import mlp
from ci import helper
import copy
from itertools import izip
import matplotlib.pyplot as plt
import numpy as np

argmax = lambda array: max(izip(array, xrange(len(array))))[1]

pttNet = [mlp.randNet([4, 5, 3], type=mlp.SIGMOID), mlp.randNet([4, 10, 3], type=mlp.SIGMOID), mlp.randNet([4, 15, 3], type=mlp.SIGMOID), mlp.randNet([4, 5, 5, 3], type=mlp.SIGMOID)]
learningRate = [0.01, 0.05, 0.1, 0.2]
epoch = 100

f = open("iris.pat", "r")
fw = open("report/iris/report.txt", "w")
lines = f.readlines()

datas = []
for line in lines:
    words = line.split(" ")
    datas.append([float(word) for word in words])

datas = np.array(datas)

for i in range(0, 4):
    datas[:,i] = (datas[:,i] - np.min(datas[:,i]))/(np.max(datas[:,i])-np.min(datas[:,i]))

datas = datas.tolist()

floods = helper.crossvalidation(datas, 0.1, shuffer=True)
plt.ion()
plt.show()

m_cor = 0.0

for pn in pttNet:
    for lr in learningRate:
        s_cor = 0.0
        b_cor = 0.0

        for i in range(0, floods.state):
            train = floods.getTrain(i)
            test = floods.getTest(i)

            print "Net Structure " + str(pn.getLayer()) + " Learning Rate and Momentum " + str(lr) + " Flood " + str(i+1)
            fw.write("Net Structure " + str(pn.getLayer()) + " Learning Rate and Momentum " + str(lr) + " Flood " + str(i+1) + "\n")

            net = copy.copy(pn)
            bp = mlp.backpropagation(net, learning_rate=lr, momentum=lr)

            ers = []
            for e in range(0, epoch):
                er = 0
                for t in train:
                    er += bp.train(t[0:4], t[4:7])

                ers.append(er)
            plt.clf()
            plt.plot(ers)
            plt.draw()

            netName = str(net.getLayer()).replace(', ', '-').replace('[', '').replace(']', '')
            plt.savefig('report/iris/' + netName + '_' + str(lr) + '_' + str(i+1) + '.png')

            cor = 0.0
            n = len(test)
            for t in test:
                target = t[4:7]
                net.process(t[0:4])
                if argmax(net.getOutput())==argmax(target):
                    cor+=1.0

            ratio_cor = cor/n
            s_cor+=ratio_cor

            if ratio_cor>b_cor:
                b_cor = ratio_cor
                tmp_m_net = net
                tmp_m_lr = lr

            print "Ratio Correctly " + str(ratio_cor)
            fw.write("Ratio Correctly " + str(ratio_cor) + "\n")

        mean_cor = s_cor/floods.state
        if mean_cor>m_cor:
            m_cor = mean_cor
            m_flood = i
            m_net = net
            m_lr = lr
            mm_cor = b_cor

        print "Mean Correctly is " + str(mean_cor)
        print ""
        fw.write("Mean Correctly is " + str(mean_cor) + "\n\n")

print "Max Mean Correctly " + str(m_cor*100) + "% by Net Structure " + str(m_net.getLayer()) + " Learning Rate and Momentum " + str(m_lr)
fw.write("Max Mean Correctly " + str(m_cor*100) + "% by Net Structure " + str(m_net.getLayer()) + " Learning Rate and Momentum " + str(m_lr) + "\n")
