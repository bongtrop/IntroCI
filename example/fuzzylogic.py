from ci.fuzzy.logic import *
import ci.fuzzy.mf as mf

mfs1 = {"small": mf.down(10.0, 25.0), "medium": mf.tri(20.0, 30.0), "big": mf.up(25.0, 40.0)}
mfs2 = {"low": mf.down(0.0, 0.5), "medium": mf.tri(0.0, 1.0), "high": mf.up(0.0, 1.0)}

inputVal = {"breast": value(mfs1, frange(0, 51, 1)), "waistline": value(mfs1, frange(0, 51, 1)), "ass": value(mfs1, frange(0, 51, 1))}
outputVal = {"sexy": value(mfs2, frange(0.0, 1.05, 0.05))}
rules = []
rules.append([{"breast": "small",	"waistline": "small",	"ass": "small"},	{"sexy": "low"}])
rules.append([{"breast": "small",	"waistline": "small",	"ass": "medium"},	{"sexy": "medium"}])
rules.append([{"breast": "small",	"waistline": "small",	"ass": "big"},	{"sexy": "medium"}])
rules.append([{"breast": "medium",	"waistline": "small",	"ass": "small"},	{"sexy": "medium"}])
rules.append([{"breast": "medium",	"waistline": "small",	"ass": "medium"},	{"sexy": "high"}])
rules.append([{"breast": "medium",	"waistline": "small",	"ass": "big"},	{"sexy": "high"}])
rules.append([{"breast": "big",	"waistline": "small",	"ass": "small"},	{"sexy": "medium"}])
rules.append([{"breast": "big",	"waistline": "small",	"ass": "medium"},	{"sexy": "high"}])
rules.append([{"breast": "big",	"waistline": "small",	"ass": "big"},	{"sexy": "high"}])
rules.append([{"breast": "small",	"waistline": "medium",	"ass": "small"},	{"sexy": "low"}])
rules.append([{"breast": "small",	"waistline": "medium",	"ass": "medium"},	{"sexy": "low"}])
rules.append([{"breast": "small",	"waistline": "medium",	"ass": "big"},	{"sexy": "medium"}])
rules.append([{"breast": "medium",	"waistline": "medium",	"ass": "small"},	{"sexy": "low"}])
rules.append([{"breast": "medium",	"waistline": "medium",	"ass": "medium"},	{"sexy": "low"}])
rules.append([{"breast": "medium",	"waistline": "medium",	"ass": "big"},	{"sexy": "medium"}])
rules.append([{"breast": "big",	"waistline": "medium",	"ass": "small"},	{"sexy": "medium"}])
rules.append([{"breast": "big",	"waistline": "medium",	"ass": "medium"},	{"sexy": "high"}])
rules.append([{"breast": "big",	"waistline": "medium",	"ass": "big"},	{"sexy": "high"}])
rules.append([{"breast": "small",	"waistline": "big",	"ass": "small"},	{"sexy": "low"}])
rules.append([{"breast": "small",	"waistline": "big",	"ass": "medium"},	{"sexy": "low"}])
rules.append([{"breast": "small",	"waistline": "big",	"ass": "big"},	{"sexy": "low"}])
rules.append([{"breast": "medium",	"waistline": "big",	"ass": "small"},	{"sexy": "low"}])
rules.append([{"breast": "medium",	"waistline": "big",	"ass": "medium"},	{"sexy": "low"}])
rules.append([{"breast": "medium",	"waistline": "big",	"ass": "big"},	{"sexy": "low"}])
rules.append([{"breast": "big",	"waistline": "big",	"ass": "small"},	{"sexy": "low"}])
rules.append([{"breast": "big",	"waistline": "big",	"ass": "medium"},	{"sexy": "low"}])
rules.append([{"breast": "big",	"waistline": "big",	"ass": "big"},	{"sexy": "low"}])

l = logic(inputVal, outputVal, rules)
print l.cal({"breast": 36.0, "waistline": 36.0, "ass": 36.0})
