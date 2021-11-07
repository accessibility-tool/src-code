import seed_expansion
import category_assign
import clustering_algo
import time

def final(seed):
    seed_expansion.create_expand_seed(seed)
    category_assign.create_expand_categories(seed)
    clustering_algo.create_clusters()


start_time = time.time()
final("Chatbot")
print("Total: %s seconds " % (time.time() - start_time))