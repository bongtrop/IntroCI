import ci.helper as helper

a = helper.crossvalidation([[1,2,3,4,5],[2,2,3,4,5],[3,2,3,4,5],[4,2,3,4,5],[5,2,3,4,5]], 0.4)


print a.getAllSet()
print ""
print a.getTrain(0)
print a.getTrain(1)
print ""
print a.getTest(0)
print a.getTest(1)
