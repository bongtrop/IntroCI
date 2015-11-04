
class value:
	def __init__(self, mfs, domain):
		self.mfs = mfs
		self.domain = domain
		self.y = [0] * len(domain)

	def getVal(self, x):
		assert (x>=min(self.domain) and x<=max(self.domain)), "out of domain"
		res = {}
		for mf in self.mfs:
			res[mf] = self.mfs[mf].getVal(x)

		return res

	def unionFunc(self, name, x):
		mf = self.mfs[name]
		i=0
		for d in self.domain:
			self.y[i] = max(self.y[i], min(mf.getVal(d), x))
			i+=1

	def getFunc(self):
		return self.y

	def getDomain(self):
		return self.domain

	def clear(self):
		self.y = [0] * len(self.domain)

class logic:
	CT = 0
	FTM = 1
	LTM = 2
	INF = 999999999.0

	def __init__(self, inputVal, outputVal, rules, defuzzifier=0):
		self.inputVal = inputVal
		self.outputVal = outputVal
		self.rules = rules
		self.defuzzifier = defuzzifier

	def cal(self, values):
		assert (len(values)==len(self.inputVal)), "input size not match"

		mfv = {}
		for v in values:
			mfv[v] = self.inputVal[v].getVal(values[v])

		for rule in self.rules:
			m = logic.INF
			for i in rule[0]:
				m = min(m, mfv[i][rule[0][i]])

			for o in rule[1]:
				self.outputVal[o].unionFunc(rule[1][o], m)

		res = {}
		for o in self.outputVal:
			domain = self.outputVal[o].getDomain()
			f = self.outputVal[o].getFunc()
			self.outputVal[o].clear()
			print f

			if (self.defuzzifier==logic.CT):
				first = sum([a * b for (a, b) in zip(domain, f)])
				second = sum(f)
				if second==0:
					res[o] = 0.0
				else:
					res[o] = first/second

			elif (self.defuzzifier==logic.FTM):
				i = f.index(max(f))
				res[o] = domain[i]

			else:
				i = len(f)-f[::-1].index(max(f))-1
				res[o] = domain[i]

		return res

def frange(start,stop, step=1.0):
	res = []
	while start < stop:
		res.append(start)
		start +=step
	return res
