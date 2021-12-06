from neo4j import GraphDatabase

class link_rec_class:

    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    
    @staticmethod
    def get_links_transaction(tx, seed_name, max_num):
        result=tx.run('''
                      match (seed:CONTENT { name: $seed_name })
                      match (n:CONTENT)<-[:LINKS_TO]-(seed)
                      with n
                      order by n.page_rank desc
                      return n.name limit $max_num
                      '''
                      , {"seed_name":seed_name, "max_num":max_num})
        return list(result.value())

  
    def get_links(self, seed, max_num):
        with self.driver.session(database=self.database) as session:
            a=session.read_transaction(self.get_links_transaction, seed, max_num)
            return a





def link_rec(seed, max_num):
    db = link_rec_class("bolt://localhost:7687", "neo4j", "1111", 'category2')

    
    links=db.get_links(seed, max_num)
      
   
    db.close()

    return links

#print(link_rec('Wikipedia', 25))
