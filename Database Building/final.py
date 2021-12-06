import seed_expansion
import category_assign
import clustering_algo
import page_rank
import time

def final(seed):

    s1 = time.time()
    links=seed_expansion.create_expand_seed(seed, 50)
    print("Seed Expansion: %s seconds " % (time.time() - s1))

    s2 = time.time()
    category_assign.create_expand_categories(seed, links)
    print("Category Expansion: %s seconds " % (time.time() - s2))

    s3 = time.time()
    clustering_algo.create_clusters()
    print("Clustering: %s seconds " % (time.time() - s3))

    s4 = time.time()
    page_rank.page_rank()
    print("Page Rank: %s seconds " % (time.time() - s4))


# start_time = time.time()
# final("Regular language")
# print("Total: %s seconds " % (time.time() - start_time))

