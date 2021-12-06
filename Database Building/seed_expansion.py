from neo4j import GraphDatabase
import links_api
import time
import parallel_api_connections
import parallel_api_views


class expand_seed:

    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    # @staticmethod
    # def create_connection_transaction(tx, seed, l):
    #     result=tx.run("MATCH (a:CONTENT{name : $seed}) "
    #                   "MATCH (b:CONTENT{name : $child}) "
    #                   "MERGE (a)-[:LINKS_TO]->(b) "
    #                   "RETURN b.name", {"child":l, "seed":seed})
    #     return result.single()[0]
    @staticmethod
    def create_connection_transaction(tx, links):
        result=tx.run("UNWIND keys($links) AS key "
                      "MATCH (n:CONTENT {name : key}) "
                      "WITH key,n "
                      "CALL { "
                      "WITH key,n "
                      "UNWIND $links[key] as item "
                      "MATCH (m:CONTENT {name : item}) "
                      "MERGE (n)-[:LINKS_TO]->(m) "
                      "RETURN count(*) as c } "
                      "RETURN n.name, c "
                      , {"links":links})
        #return result.single()[0]

    @staticmethod
    def create_content_transaction(tx, child_string, seed):
        result=tx.run(
                      "MATCH (seed:CONTENT{name : $seed}) "
                      "MERGE (a:CONTENT{name : $name}) "
                      "ON CREATE SET a.name = $name "
                      "MERGE (a)<-[:LINKS_TO]-(seed) "
                      "//SET a.level=length(shortestPath((seed)-[:LINKS_TO*1..]->(a))) "
                      , {"name":child_string, "seed":seed})
        return result.single()

    @staticmethod
    def create_seed_transaction(tx, name_string):
        result=tx.run("MERGE (a:CONTENT{ name: $name}) "
                      "ON CREATE SET a.name = $name, a.level = $level "
                      "RETURN a.name", {"name":name_string, "level": 0 })
        return result.single()[0]

    # def create_url_connection(self, seed, l):
    #     with self.driver.session(database=self.database) as session:
    #         a=session.write_transaction(self.create_connection_transaction, seed, l)
            #print(a)
    def create_url_connection(self, link_dict):
        with self.driver.session(database=self.database) as session:
            session.write_transaction(self.create_connection_transaction, link_dict)
            #print(a)

    def create_url_node(self, child_string, seed):
        with self.driver.session(database=self.database) as session:
            a=session.write_transaction(self.create_content_transaction, child_string, seed)
            #print(a)

    def create_url_seed_node(self, name_string):
        with self.driver.session(database=self.database) as session:
            a=session.write_transaction(self.create_seed_transaction, name_string)
            print(a)






def create_expand_seed(seed, max_nodes):
    db = expand_seed("bolt://localhost:7687", "neo4j", "1111", 'category2')

    s1 = time.time()
    db.create_url_seed_node(seed)
    links=links_api.get_links(title=seed)
    print("--Get Links: %s seconds" % (time.time() - s1))

    s2 = time.time()
    links=parallel_api_views.sort_links_with_views(links)
    if len(links)>max_nodes:
        links=links[0:max_nodes]
    print("--Sort Links: %s seconds" % (time.time() - s2))

    s3 = time.time()
    for link in links:
        db.create_url_node(seed=seed, child_string=link)
    print("--Create Nodes: %s seconds" % (time.time() - s3))

    s4 = time.time()
    lvl1_links=parallel_api_connections.parallel_api_connections(url_list=links)
    # for node in lvl1_links:
    #     for url in lvl1_links[node]:
    #         db.create_url_connection(node, url)
    db.create_url_connection(lvl1_links)
    print("--Get and Create Links: %s seconds" % (time.time() - s4))
   
    db.close()

    return links

#create_expand_seed("Spectral line")