from neo4j import GraphDatabase
import subcat_api

class Category:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    @staticmethod
    def create_category_transaction(tx, category_string, parent, seed):
        result=tx.run("MATCH (b:CATEGORY{category : $parent}) "
                      "MATCH (seed:CATEGORY{category : $seed}) "
                      "MERGE (a:CATEGORY{category : $category}) "
                      "ON CREATE SET a.category = $category, a.category_text = $category_text "
                      "MERGE (a)<-[:SUBCAT_OF]-(b) "
                      "SET a.level=length(shortestPath((seed)-[:SUBCAT_OF*1..]->(a))) "
                      "RETURN a.category", {"category":category_string, "parent":parent, "seed":seed, "category_text":category_string.replace("Category:","")})
        return result.single()[0]

    @staticmethod
    def create_seed_transaction(tx, category_string):
        result=tx.run("MERGE (a:CATEGORY) "
                      "ON CREATE SET a.category = $category, a.level = $level, a.category_text = $category_text "
                      "RETURN a.category", {"category":category_string, "level": 0, "category_text":category_string.replace("Category:","")})
        return result.single()[0]

    def create_category_node(self, category_string, parent, seed):
        with self.driver.session() as session:
            a=session.write_transaction(self.create_category_transaction, category_string, parent, seed)
            print(a)

    def create_seed_node(self, catagory_string):
        with self.driver.session() as session:
            a=session.write_transaction(self.create_seed_transaction, catagory_string)
            print(a)

    def create_n_levels(self, parent, parent_level, additional_levels, current_level, seed):
        if current_level <= parent_level + additional_levels :
            categories=subcat_api.get_subcat(parent)
            for x in categories:
                self.create_category_node(x, parent, seed)
            for x in categories:
                self.create_n_levels(x, parent_level, additional_levels, current_level+1, seed)


if __name__ == "__main__":
    cat = Category("bolt://localhost:7687", "neo4j", "1111")
    seed="Category:Version control systems"
    cat.create_seed_node(seed)
    cat.create_n_levels(seed, 0, 7, 1, seed)
    cat.close()

#impliment the whole find stuff from level 3 down 2 levels ?