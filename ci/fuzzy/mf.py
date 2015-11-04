class base:
	def getVal(self, x):
		raise NotImplementedError()

class up(base):
	def __init__(self, a, b):
		assert all([isinstance(val, float) for val in (a, b)]), "need float value"
		self.a = a
		self.b = b

	def getVal(self, x):
		assert isinstance(x, float)
		if x < self.a:
			return 0.0
		if x < self.b:
			return (x - self.a) / (self.b - self.a)
		return 1.0

class down(base):
	def __init__(self, a, b):
		assert all([isinstance(val, float) for val in (a, b)]), "need float value"
		self.a = a
		self.b = b

	def getVal(self, x):
		assert isinstance(x, float)
		u = up(self.a, self.b)
		return 1. - u.getVal(x)

class tri(base):
	def __init__(self, a, b):
		assert all([isinstance(val, float) for val in (a, b)]), "need float value"
		self.a = a
		self.b = b

	def getVal(self, x):
		assert isinstance(x, float)
		m = (self.a + self.b) / 2.
		first = (x - self.a) / (m - self.a)
		second = (self.b - x) / (self.b - m)
		return max(min(first, second), 0.)

class trap(base):
	def __init__(self, a, b, c, d):
		assert all([isinstance(val, float) for val in (a, b, c, d)]), "need float value"
		self.a = a
		self.b = b
		self.c = c
		self.d = d

	def getVal(self, x):
		assert isinstance(x, float)
		first = (x - self.a) / (self.b - self.a)
		second = (self.d - x) / (self.d - self.c)
		return max(min(first, 1., second), 0.)
