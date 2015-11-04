import ci.net as net
import ci.bp as bp

net = net.randNet([2,2,1])
b = bp.bp(net, 0.5, 0.1)

dataset = [[[0,0],[0]],[[0,1],[1]],[[1,0],[1]],[[1,1],[0]]]

for i in range(0, 10000):
  error = 0.0
  for d in dataset:
    inp = d[0]
    outp = d[1]
    error = error + b.backPropagate(inp, outp)

  #print error

net.process([0,0])
print net.getNode(2,0)

net.process([0,1])
print net.getNode(2,0)

net.process([1,0])
print net.getNode(2,0)

net.process([1,1])
print net.getNode(2,0)
