from neo4j import GraphDatabase

class get_cluster_class:

    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    
    @staticmethod
    def get_cluster_transaction(tx, seed_name, max_num):
        result=tx.run('''
                      match (seed:CONTENT { name: $seed_name })
                      match (n:CONTENT)<-[:LINKS_TO]-(seed)
                      where n.community=seed.community
                      with n
                      order by n.page_rank desc
                      return n.name limit $max_num
                      '''
                      , {"seed_name":seed_name, "max_num":max_num})
        return list(result.value())

  
    def get_cluster(self, seed, max_num):
        with self.driver.session(database=self.database) as session:
            a=session.read_transaction(self.get_cluster_transaction, seed, max_num)
            return a





def get_cluster_links(cluster_seed, max_num):
    db = get_cluster_class("bolt://localhost:7687", "neo4j", "1111", 'category2')

    
    links=db.get_cluster(cluster_seed, max_num)
      
   
    db.close()

    return links

#print(link_rec('Wikipedia', 25))
