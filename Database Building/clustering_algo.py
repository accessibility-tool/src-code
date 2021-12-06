from neo4j import GraphDatabase

class clusters:
    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    @staticmethod
    def set_weight_baseline(tx):
        result=tx.run(
                      "match paths=(n)-[r:LINKS_TO]-(m) "
                      "set r.weight=1 "
                      )
        return result.single()

    @staticmethod
    def set_weight_category(tx, param):
        result=tx.run(
                      "match (n:CONTENT)-[:BELONGS_TO]->(:CATEGORY)<-[:BELONGS_TO]-(m:CONTENT) "
                      "match paths=(n)-[r:LINKS_TO]-(m) "
                      "set r.weight=r.weight+$param ", param=param
                      )
        return result.single()

    # @staticmethod
    # def set_weight_category(tx, param):
    #     result=tx.run(
    #                   "match (n:CONTENT)-[:BELONGS_TO]->(:CATEGORY)<-[:BELONGS_TO]-(m:CONTENT) "
    #                   "match paths=(n)-[r:LINKS_TO]-(m) "
    #                   "set r.weight=r.weight+$param ", param=param
    #                   )
    #     return result.single()

    @staticmethod
    def set_cluster(tx):
        result=tx.run('''
                      CALL gds.graph.create(
                        "MyGraph",
                        "CONTENT",
                        {
                            LINKS_TO: {
                                type: 'LINKS_TO',
                                orientation: 'undirected',
                                aggregation: 'NONE'
                            }
                        },
                        {
                            relationshipProperties: 'weight'
                        }
                      ) YIELD nodeCount
                      CALL gds.louvain.write(
                        'MyGraph',
                        {
                        writeProperty:"community",
                        nodeLabels: ['CONTENT'],
                        relationshipTypes: ['LINKS_TO'],
                        relationshipWeightProperty: 'weight',
                        maxLevels:100,
                        maxIterations:100,
                        tolerance:0.000005,
                        includeIntermediateCommunities:TRUE
                      }) YIELD communityCount,
                      ranLevels,
                      modularity,
                      modularities,
                      communityDistribution
                      RETURN communityCount,
                      modularity
                      '''
                      )
        return result.single()

    @staticmethod
    def post_algo(tx):
        result=tx.run(
                      '''
                      CALL gds.graph.drop("MyGraph") YIELD graphName
                      match (n:CONTENT)
                      set n.community=n.community[0]
                      '''
                      )
        return result.single()

    def create_clusters_db(self):
        with self.driver.session(database=self.database) as session:            
            param=1.0
            max_mod=-1.5
            modularity=0
            while modularity>max_mod and modularity-max_mod>=0.01:
                max_mod=modularity
                session.write_transaction(self.set_weight_baseline)
                session.write_transaction(self.set_weight_category, param)
                a=session.write_transaction(self.set_cluster)
                session.write_transaction(self.post_algo)
                modularity=a[1]
                print(modularity)
                param=param + 0.1

            param=param-0.2
            session.write_transaction(self.set_weight_baseline)
            session.write_transaction(self.set_weight_category, param)
            a=session.write_transaction(self.set_cluster)
            modularity=a[1]
            print(modularity)
            session.write_transaction(self.post_algo)



        
def create_clusters():
    db = clusters("bolt://localhost:7687", "neo4j", "1111", 'category2')

    db.create_clusters_db()

    db.close()

#create_clusters()
    