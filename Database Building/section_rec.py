from neo4j import GraphDatabase
import section_links
import time

class get_cluster_class:

    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    # @staticmethod
    # def get_cluster_transaction(tx, seed_list, max_num, seed):
    #     result=tx.run('''
    #                   UNWIND $seed_list as seed
    #                   match (seed_node:CONTENT {name : seed})
    #                   with collect(distinct seed_node) as nodes
    #                   CALL gds.pageRank.stream(
    #                     {
    #                         nodeQuery:'unwind $nodes as node return id(node) AS id',
    #                         relationshipQuery:'MATCH (n:CONTENT)-[r:LINKS_TO]->(m:CONTENT) where n IN $nodes and m in $ nodes RETURN id(n) AS source, id(m) AS target, r.weight as weight',
    #                         parameters:{ nodes: nodes},
    #                         maxIterations: 200,
    #                         relationshipWeightProperty:'weight'
    #                     }
    #                   ) 
    #                   YIELD nodeId, score
    #                   RETURN gds.util.asNode(nodeId).name AS name
    #                   ORDER BY score DESC limit $max_num
    #                   '''
    #                   , {"seed_list":seed_list, "max_num":max_num, "page":seed})
    #     return list(result.value())

    
    @staticmethod
    def get_cluster_transaction(tx, seed_list, max_num, seed):
        result=tx.run('''
                      UNWIND $seed_list as seed
                      match (seed_node:CONTENT {name : seed})
                      with seed_node, seed
                      call { 
                        with seed_node, seed
                        match (n:CONTENT)
                        where n.community=seed_node.community
                        return collect(distinct n)+seed_node as node_list
                      }                
                      with collect(node_list) as nested, collect(seed_node) as seed_nodes
                      unwind nested as i
                      unwind i as j
                      with j, seed_nodes
                      where reduce(val=true, seed in seed_nodes|val and (j in seed_nodes or exists((j)-[:LINKS_TO*0..1]-(seed))))
                      with collect(distinct j) as nodes, seed_nodes
                      CALL gds.pageRank.stream(
                        {
                            nodeQuery:'unwind $nodes as node return id(node) AS id',
                            relationshipQuery:'MATCH (n:CONTENT)-[r:LINKS_TO]->(m:CONTENT) where n IN $nodes and m in $ nodes RETURN id(n) AS source, id(m) AS target, r.weight as weight',
                            parameters:{ nodes: nodes},
                            maxIterations: 200,
                            relationshipWeightProperty:'weight',
                            sourceNodes:seed_nodes
                        }
                      ) 
                      YIELD nodeId, score
                      RETURN gds.util.asNode(nodeId).name AS name
                      ORDER BY score DESC limit $max_num
                      '''
                      , {"seed_list":seed_list, "max_num":max_num})
        return list(result.value())

  
    def get_cluster(self, sec_links, max_num, seed):
        with self.driver.session(database=self.database) as session:
            a=session.read_transaction(self.get_cluster_transaction, sec_links, max_num, seed)
            return a




def get_rec(sec_links, max_num, seed):
    db = get_cluster_class("bolt://localhost:7687", "neo4j", "1111", 'category2')

    final_dic={}

    for x in sec_links:
        s1 = time.time()
        sec_links[x]=sec_links[x]+[seed]
        final_dic[x]=db.get_cluster(sec_links[x], max_num, seed)
        print("Section Time: %s seconds " % (time.time() - s1))
   
    db.close()

    return final_dic


# s1 = time.time()
# seed='United States'
# x=section_links.section_text(seed)
# print("API Time: %s seconds " % (time.time() - s1))
# print(len(x))
# s1 = time.time()
# t=get_rec(x, 15, seed)
# for i in t:
#     print(i,t[i])
# print("Total Section Time: %s seconds " % (time.time() - s1))

