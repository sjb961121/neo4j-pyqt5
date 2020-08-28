import pandas as pd
import numpy as np
import py2neo
import os
import glob

def stringSolve(list1,list2,command,nodeName,className = 'p'):
	punc = ('(',')','{','}',':',',')
	str1 = command + punc[0] + className +punc[4] + nodeName + punc[2]  
	for (i,j) in zip(list1,list2):
		str1 += i + punc[4] + '\"' + str(j) + '\"' + punc[5]
	str1 = str1.strip(',')
	str1 += punc[3] + punc[1]
	return str1



def createNodes(title,data):
	graph = py2neo.Graph("http://localhost:7474",auth=("neo4j","961121"))
	try:
		for i in data:
			try:
				_class = i[(np.where(title == 'name')[0][0])].replace('-','')
			except:
				try:
					_class = i[title.index('name')].replace('-','')
				except:
					_class = 'untitled'
			str1 = stringSolve(title,i,'MERGE',_class)
			print(str1)
			print('-----------------------------------------')
			graph.run(str1)
	except Exception as e:
		print(e)
		return

def data2neo4j():
	d = os.path.dirname(__file__)
	excel_Paths = glob.glob(os.path.join(os.path.dirname(os.path.dirname(d)),'static','data','excel',"*.xlsx"))
	print(excel_Paths)
	for excel_Path in excel_Paths:
		df = pd.read_excel(excel_Path)
		title = df.columns.values
		data = df.values
		createNodes(title,data)

def drawRelations(p1,v1,p2,v2,r,directed = False):
	graph = py2neo.Graph("http://localhost:7474",auth=("neo4j","961121"))
	
	graph.run("MATCH(e),(f)\
		WHERE e.%s = '%s' AND f.%s = '%s'\
		MERGE(e)-[r:%s]->(f)\
		RETURN r"%(p1,v1,p2,v2,r))


 


if __name__ == '__main__':
	data2neo4j()
	a = [['日本'],['美国'],['俄罗斯']]
	createNodes(['name'],a)
	for i in a:
		drawRelations('name',i[0],'nation',i[0],'have')


