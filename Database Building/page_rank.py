from neo4j import GraphDatabase

class rank:
    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    @staticmethod
    def set_rank(tx):
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
                      CALL gds.pageRank.write(
                        'MyGraph',
                        {
                        writeProperty:"page_rank",
                        nodeLabels: ['CONTENT'],
                        relationshipTypes: ['LINKS_TO'],
                        //relationshipWeightProperty: 'weight',
                        maxIterations:500
                      }) YIELD didConverge, ranIterations
                      RETURN didConverge, ranIterations
                      '''
                      )
        return result.single()

    @staticmethod
    def post_algo(tx):
        result=tx.run(
                      '''
                      CALL gds.graph.drop("MyGraph") YIELD graphName
                      '''
                      )
        return result.single()

    def set_page_rank(self):
        with self.driver.session(database=self.database) as session:            
            a=session.write_transaction(self.set_rank)
            print(a)
            session.write_transaction(self.post_algo)



        
def page_rank():
    db = rank("bolt://localhost:7687", "neo4j", "1111", 'category2')

    db.set_page_rank()

    db.close()

#page_rank()
    