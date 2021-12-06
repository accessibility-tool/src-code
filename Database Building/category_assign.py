import links_api
import time
from neo4j import GraphDatabase
import parallel_categories

class category_nodes:

    
    def __init__(self, uri, user, password,db):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database=db

    def close(self):
        self.driver.close()

    # @staticmethod
    # def create_category_transaction(tx, content_node, category_node):
    #     result=tx.run(
    #                   "MATCH (con:CONTENT{name : $content}) "
    #                   "MERGE (cat:CATEGORY{name : $category}) "
    #                   "ON CREATE SET cat.name = $category "
    #                   "MERGE (con)-[:BELONGS_TO]->(cat) "
    #                   "RETURN cat.name", {"content":content_node, "category":category_node})
    #     return result.single()[0]

    @staticmethod
    def create_category_transaction(tx, content_node, categories):
        result=tx.run(
                      "UNWIND $categories as category "
                      "MATCH (con:CONTENT{name : $content}) "
                      "WITH con, category "
                      "CALL { "
                      "WITH con, category "
                      "MERGE (cat:CATEGORY{name : category}) "
                      "ON CREATE SET cat.name = category "
                      "MERGE (con)-[:BELONGS_TO]->(cat) "
                      "RETURN cat.name as n} "
                      "RETURN COUNT(n)", {"content":content_node, "categories":categories})
        return result.single()[0]

    def create_category(self, seed, categories):
        with self.driver.session(database=self.database) as session:
            a=session.write_transaction(self.create_category_transaction, seed, categories)
            #print(a)

def create_expand_categories(seed, links=None):
    db = category_nodes("bolt://localhost:7687", "neo4j", "1111", 'category2')
    if links is None:
        links=links_api.get_links(title=seed)
        
    links.append(seed)

    #category_set=set()


    category_dict=parallel_categories.get_categories(links)
    for category_key in category_dict:
        #print(category_key, category_dict[category_key])
        db.create_category(category_key, category_dict[category_key])

    # for link in links:
    #     categories=get_page_categories.get_categories(link)
    #     db.create_category(link, categories)
        # for category in categories:
        #     category_set.add(category)
        #     db.create_category(link, category)



    db.close()

#create_expand_categories("Spectral lines")



