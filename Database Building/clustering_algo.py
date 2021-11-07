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
    def set_weight_category(tx):
        result=tx.run(
                      "match (n:CONTENT)-[:BELONGS_TO]->(:CATEGORY)<-[:BELONGS_TO]-(m:CONTENT) "
                      "match paths=(n)-[r:LINKS_TO]-(m) "
                      "set r.weight=r.weight*1.8 "
                      )
        return result.single()

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
                        maxIterations:105,
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
            session.write_transaction(self.set_weight_baseline)
            session.write_transaction(self.set_weight_category)
            a=session.write_transaction(self.set_cluster)
            print(a)
            session.write_transaction(self.post_algo)



        
def create_clusters():
    db = clusters("bolt://localhost:7687", "neo4j", "1111", 'category2')

    db.create_clusters_db()

    db.close()

#create_clusters()
    