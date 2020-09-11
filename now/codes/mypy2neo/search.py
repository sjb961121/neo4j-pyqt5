import py2neo
import os
import json
import copy
import sys
d = os.path.dirname(__file__)
print(d)
sys.path.append(os.path.dirname(d)) # 添加自己指定的搜索路径


def getFiles(path, prefix):
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) \
    for file in files if file.startswith(prefix)]

class search_return():
	"功能: 对数据库进行搜索操作\
	参数 search_name 为搜索名"
	def __init__(self,search_name):
		self.search_name = search_name
		self.graph = py2neo.Graph("http://localhost:7474",auth=("neo4j","961121"))


	def node(self):
		str1= "MATCH (n) WHERE id(n)=%d RETURN n"%(self.search_name)
		# str1 =  "MATCH(n{name:'%s'})RETURN n"%(self.search_name)
		return self.graph.run(str1).to_subgraph()

	def picture_path(self):
		path = os.path.dirname(os.path.dirname(d)) + "\\static\\pictures"
		return [os.path.abspath(os.path.join(root, file)) for root, dirs, files in os.walk(path) \
		    	for file in files if file.startswith(self.search_name)]

	def relationships(self,limit = 25):
		# str1 = "match(n{name: '%s'})-[r]-(b) RETURN r LIMIT %s"%(self.search_name,limit)
		str1 = "MATCH (n)-[r]-(b) WHERE id(n)=%d RETURN r LIMIT %s" % (self.search_name,limit)
		return self.graph.run(str1)

	def dict(self):
		a = str(self.node()) #fuck neo4j
		# b=self.node().labels
		if str(self.node().labels)==':Run':
			return self.dict_for_run()
		if self.node():
			dict_run=dict()
			dict_node=dict(self.node())
			str1="MATCH ()-[r]-b"
			dict_run['名称']=dict_node.pop('name')
			dict_run.update(dict_node)
			return dict_run
		else:
			return None


	def singleNode_json(self):
		node = self.node()
		a = str(node)  #fuck neo4j
		a = dict(node)
		a["id"] = node.identity
		a["label"]=str(node.labels)
		b=json.dumps({"nodes":[a],"links":[]})
		return b


	def dict_for_run(self):
		print('start')
		dict_run = dict()

		relation_dict=dict()

		a = str(self.node())  # fuck neo4j
		# dict_run.update(dict(self.node()))
		dict_node = dict(self.node())
		dict_run['名称'] = dict_node.pop('name')
		dict_run.update(dict_node)

		str1 = "MATCH (n)-[r]-(b) WHERE id(n)=%d AND type(r)<>'故障后运行方式' RETURN n,r,b" % (self.search_name)
		result = self.graph.run(str1).to_subgraph()
		# for node in result.nodes:
		# 	id = node.identity
		# 	if (id == self.search_name):
		# 		dict_search = dict(node)
		# 		dict_search['name'+str(node.labels)]=dict_search.pop('name')
		# 		dict_run.update(dict_search)
		# 		print(dict_run)
		# 	str2 = "MATCH (n)-[r]-() WHERE id(n)=%d RETURN count(r)" % (id)
		# 	node_result = self.graph.run(str2).evaluate()
		# 	print(node_result)

		for relation in result.relationships:
			str1="MATCH ()-[r]->() WHERE id(r)=%d RETURN type(r)"%(relation.identity)
			relation_result=self.graph.run(str1).evaluate()
			# print(relation_result)
			str1="MATCH (n)-[r]->(b) WHERE id(r)=%d RETURN b"%(relation.identity)
			node_result = self.graph.run(str1).to_subgraph()
			str1= "MATCH (n)-[r]-() WHERE id(n)=%d RETURN count(r)" % (node_result.identity)
			relation_count=self.graph.run(str1).evaluate()
			if (relation_count>1):
				# print(relation_result)
				dict_node = dict(node_result)
				dict_node_name=dict()
				if relation_result in relation_dict.keys():
					i=relation_dict[relation_result]
					relation_result=relation_result+str(i)
					relation_dict[relation_result]=i+1
				else:
					relation_dict[relation_result]=2

				dict_node.pop('name')
				# dict_node_name[relation_result] = dict_node.pop('name')
				# dict_run.update(dict_node_name)
				dict_run.update(dict_node)

				dict_ex=dict()

				str1 = "MATCH (n)-[r]->(b) WHERE id(n)=%d RETURN n,r,b"%(node_result.identity)
				ex_result=self.graph.run(str1).to_subgraph()
				for ex_relation in ex_result.relationships:
					str1 = "MATCH ()-[r]->() WHERE id(r)=%d RETURN type(r)" % (ex_relation.identity)
					ex_relation_result = self.graph.run(str1).evaluate()
					# if ex_relation_result in relation_dict.keys():
					# 	i = relation_dict[ex_relation_result]
					# 	ex_relation_result = ex_relation_result + str(i)
					# 	relation_dict[ex_relation_result] = i + 1
					# else:
					# 	relation_dict[ex_relation_result] = 2
					str1 = "MATCH (n)-[r]->(b) WHERE id(r)=%d RETURN b" % (ex_relation.identity)
					ex_node_result = self.graph.run(str1).to_subgraph()
					ex_dict_node = dict(ex_node_result)
					ex_dict_node_name=dict()
					ex_dict_node_name[ex_relation_result] = ex_dict_node.pop('name')
					dict_ex.update(ex_dict_node_name)
					dict_ex.update(ex_dict_node)
					# dict_run.update(ex_dict_node_name)
					# dict_run.update(ex_dict_node)
				string=str(dict_ex)
				string=string.replace('\'','').replace('{','').replace('}','')
				dict_node_name[relation_result] = string
				dict_run.update(dict_node_name)

			else:
				dict_node=dict(node_result)
				dict_node_name = dict()
				if relation_result in relation_dict.keys():
					i=relation_dict[relation_result]
					relation_result=relation_result+str(i)
					relation_dict[relation_result]=i+1
				else:
					relation_dict[relation_result]=2
				dict_node_name[relation_result] = dict_node.pop('name')
				dict_run.update(dict_node_name)
				dict_run.update(dict_node)

		print(dict_run)
		print('end')

		# return dict(self.node()) if self.node() else None
		return dict_run



	def json(self):
		links = []
		nodes = []
		nodes_set = set()
		links_set = set()

		for record in self.relationships():
			link = record.to_subgraph()
			a = str(link)   # fuck py2neo
			print('a',a)

			if link.start_node.identity not in nodes_set:
				dic = dict(link.start_node)
				dic['id'] = link.start_node.identity

				dic['label']=str(link.start_node.labels)

				nodes_set.add(link.start_node.identity)
				nodes.append(dic)
			if link.end_node.identity not in nodes_set:
				dic = dict(link.end_node)
				dic['id'] = link.end_node.identity

				dic['label'] = str(link.end_node.labels)

				nodes_set.add(link.end_node.identity)
				nodes.append(dic)

			if link.identity not in links_set:
				dic = dict(link)
				dic['relationships'] = type(link).__name__
				dic['id'] = link.identity
				dic['source'] = link.start_node.identity
				dic['target'] = link.end_node.identity
				links.append(dic)
				links_set.add(link.identity)

		print(str(self.node().labels))
		if (str(self.node().labels)==':TS' or str(self.node().labels)==':TL'):
			nodes=[]
			links=[]

		a = json.dumps({"nodes" : nodes,"links" : links})
		return a



if __name__ == '__main__':
	name = "美国"

	path = '../../static/data/json/search_return.json'
	dd = search_return(name)
	print(dd.json())
	print(dd.singleNode_json())
