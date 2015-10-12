import random
import math

def chunks(l, n):
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]

class crossvalidation:
	def __init__(self, datas, ratio = 0.1, shuffer = False):
		if shuffer:
			random.shuffle(datas)

		l = int(math.ceil(len(datas) * ratio))

		if int(len(datas) * ratio)==0:
			raise ValueError("Wrong ratio cant chunks more")

		self.set = chunks(datas, l)
		self.ratio = ratio
		self.shuffer = shuffer
		self.state = int(1.0/ratio)

	def getAllSet(self):
		return self.set

	def getTrain(self, state):
		if state>=self.state:
			raise ValueError('Wrong state max state is ' + str(self.state-1))

		res = self.set[0:state]
		if state+1 < self.state:
			res += self.set[state+1:]

		result = []
		for r in res:
			result+=r

		return result

	def getTest(self, state):
		if state>=self.state:
			raise ValueError('Wrong state max state is ' + str(self.state-1))

		return self.set[state]
