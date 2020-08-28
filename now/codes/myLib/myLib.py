import os

def getParentPath(num):
	path = os.path.dirname(__file__)
	for i in range(num):
		path = os.path.dirname(path)
	return path


print(getParentPath(0))
print(getParentPath(1))